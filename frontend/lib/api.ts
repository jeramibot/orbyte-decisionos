export async function api<T>(path:string, actor:string, method='GET', body?:unknown, key?:string):Promise<T> {
  const response = await fetch(`/api${path}`, { method, headers: { 'Content-Type':'application/json', 'X-Demo-User':actor, ...(key?{'Idempotency-Key':key}:{}) }, body:body === undefined ? undefined : JSON.stringify(body), cache:'no-store' });
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Check the input values and try again.');
  return data;
}
export const money = (sen:number) => `RM${(sen / 100).toLocaleString('en-MY', {minimumFractionDigits:2,maximumFractionDigits:2})}`;
export const date = (value:string) => new Date(value).toLocaleString('en-MY', {day:'numeric',month:'short',hour:'2-digit',minute:'2-digit',timeZone:'Asia/Kuala_Lumpur'});
export const human = (value:string) => value.toLowerCase().replaceAll('_',' ');
