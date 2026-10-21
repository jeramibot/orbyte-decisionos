import {defineConfig, devices} from '@playwright/test';
export default defineConfig({testDir:'./tests/e2e',fullyParallel:false,workers:1,timeout:45000,expect:{timeout:10000},reporter:'list',use:{baseURL:'http://127.0.0.1:3001',trace:'retain-on-failure',...devices['Desktop Chrome']},webServer:[
 {command:'../.venv/bin/python ../scripts/test_server.py',url:'http://127.0.0.1:8001/api/health',reuseExistingServer:false,timeout:30000},
 {command:'node node_modules/next/dist/bin/next dev --webpack --hostname 127.0.0.1 --port 3001',url:'http://127.0.0.1:3001',reuseExistingServer:false,timeout:60000,env:{BACKEND_URL:'http://127.0.0.1:8001',NEXT_TELEMETRY_DISABLED:'1',WATCHPACK_POLLING:'true'}}
]});
