"""Contract fixtures only. These are not recorded or genuine simulation reports."""
import json
import httpx
import pytest
from backend.adapters.mirofish import MiroFishAdapter, MiroFishConfig, SimulationError, structure_report
from backend.schemas.contracts import ScenarioRequest
from backend.services.scenarios import build_scenario
from backend.services.worker import process
from backend.models.entities import SimulationRun
from backend.api.app import create_app
from fastapi.testclient import TestClient

SCENARIO = build_scenario(ScenarioRequest(), {"synthetic": True})


def make(handler, **kwargs):
    return MiroFishAdapter(MiroFishConfig(allow_external=True, poll_interval=0, **kwargs), httpx.MockTransport(handler))


@pytest.mark.asyncio
@pytest.mark.parametrize('status,code', [(401,'CREDENTIALS'),(403,'CREDENTIALS'),(429,'RATE_LIMITED'),(503,'UPSTREAM_HTTP')])
async def test_service_errors(status, code):
    adapter = make(lambda r: httpx.Response(status, json={'error':'never expose provider internals'}))
    with pytest.raises(SimulationError) as exc:
        await adapter.get_simulation_status('sim_test')
    assert exc.value.code == code
    assert 'provider internals' not in str(exc.value)
    await adapter.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('response', [{'success':True}, {'status':'ok'}, {'success':True,'data':[]}, {'success':'true','data':{}}])
async def test_malformed_envelope(response):
    adapter = make(lambda r: httpx.Response(200, json=response))
    with pytest.raises(SimulationError) as exc:
        await adapter.get_simulation_status('sim_test')
    assert exc.value.code == 'INVALID_RESPONSE'
    await adapter.close()


@pytest.mark.asyncio
async def test_disabled_never_sends_network_request():
    def fail(request):
        raise AssertionError('Network must not be called')
    adapter = MiroFishAdapter(MiroFishConfig(), httpx.MockTransport(fail))
    with pytest.raises(SimulationError, match='disabled'):
        await adapter.create_scenario(SCENARIO)
    await adapter.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('error,code', [(httpx.ReadTimeout('timed out'),'TIMEOUT'),(httpx.ConnectError('offline'),'UNAVAILABLE')])
async def test_transport_errors(error, code):
    def handler(request): raise error
    adapter = make(handler)
    with pytest.raises(SimulationError) as exc:
        await adapter.get_simulation_status('sim_test')
    assert exc.value.code == code
    await adapter.close()


@pytest.mark.asyncio
async def test_incomplete_report():
    adapter = make(lambda r:httpx.Response(200,json={'success':True,'data':{'status':'completed','markdown_content':''}}))
    with pytest.raises(SimulationError) as exc: await adapter.get_simulation_report('sim_test')
    assert exc.value.code == 'INCOMPLETE_REPORT'
    await adapter.close()


def fixture_transport(request):
    path=request.url.path
    data={
        '/api/graph/ontology/generate':{'project_id':'proj_test'},
        '/api/graph/build':{'task_id':'task_graph'},
        '/api/graph/task/task_graph':{'status':'completed'},
        '/api/graph/project/proj_test':{'graph_id':'graph_test'},
        '/api/simulation/create':{'simulation_id':'sim_test'},
        '/api/simulation/prepare':{'task_id':'task_prepare','status':'preparing'},
        '/api/simulation/prepare/status':{'status':'ready'},
        '/api/simulation/start':{'runner_status':'running'},
        '/api/simulation/sim_test/run-status':{'runner_status':'completed'},
        '/api/report/generate':{'task_id':'task_report'},
        '/api/report/generate/status':{'status':'completed'},
        '/api/report/by-simulation/sim_test':{'report_id':'report_test','simulation_id':'sim_test','status':'completed',
            'markdown_content':'# TEST FIXTURE ONLY\n## Risks\n- Test-only risk\n## Mitigations\n- Test-only response'},
        '/api/simulation/stop':{'runner_status':'stopped'},
    }[path]
    if path=='/api/simulation/start':
        body=json.loads(request.content)
        assert body['max_rounds']==2 and body['platform']=='twitter' and body['force'] is False
    if path=='/api/graph/ontology/generate':
        assert b'synthetic-scenario.txt' in request.content
    return httpx.Response(200,json={'success':True,'data':data})


@pytest.mark.asyncio
async def test_full_contract_lifecycle_not_a_genuine_run():
    adapter=make(fixture_transport)
    updates=[]
    result,provenance,elapsed=await adapter.run(SCENARIO,updates.append,lambda:False)
    assert result['source_run_id']=='sim_test'
    assert result['risks']==['Test-only risk']
    assert result['stakeholder_reactions']==[]
    assert provenance['report_id']=='report_test' and elapsed>=0
    assert [x['stage'] for x in updates]==['BUILDING_GRAPH','PREPARING_AGENTS','SIMULATING','GENERATING_REPORT']
    await adapter.close()


@pytest.mark.asyncio
async def test_total_job_timeout():
    def handler(request):
        if '/task/' in request.url.path:
            return httpx.Response(200,json={'success':True,'data':{'status':'processing'}})
        return fixture_transport(request)
    adapter=make(handler,job_timeout=.01)
    with pytest.raises(SimulationError) as exc: await adapter.run(SCENARIO,lambda p:None,lambda:False)
    assert exc.value.code=='TIMEOUT'
    await adapter.close()


@pytest.mark.asyncio
async def test_cancel_calls_stop_after_simulation_created():
    calls=[];updates=[]
    def handler(request):
        calls.append(request.url.path)
        return fixture_transport(request)
    adapter=make(handler)
    with pytest.raises(SimulationError) as exc:
        await adapter.run(SCENARIO,updates.append,lambda:any(p['stage']=='PREPARING_AGENTS' for p in updates))
    assert exc.value.code=='CANCELLED'
    assert '/api/simulation/stop' in calls and '/api/simulation/start' not in calls
    await adapter.close()


def test_remote_url_and_path_identifiers_rejected():
    with pytest.raises(ValueError): MiroFishAdapter(MiroFishConfig(base_url='https://example.org'))
    with pytest.raises(SimulationError): MiroFishAdapter.identifier({'id':'../../secrets'},'id')


@pytest.mark.asyncio
async def test_worker_persists_failure_without_report(tmp_path, monkeypatch):
    app=create_app(f'sqlite:///{tmp_path}/worker.db')
    monkeypatch.setenv('MIROFISH_ALLOW_EXTERNAL','true')
    monkeypatch.setenv('MIROFISH_BASE_URL','http://127.0.0.1:5001')
    with TestClient(app) as client:
        run=client.post('/api/simulations',headers={'X-Demo-User':'owner-demo'},json={}).json()
    adapter=make(lambda r:httpx.Response(429,json={}))
    await process(app.state.sessions,run['id'],adapter)
    with app.state.sessions() as db:
        stored=db.get(SimulationRun,run['id'])
        assert stored.status=='RATE_LIMITED' and stored.report is None and stored.token_usage is None
    await adapter.close()
