import {api} from './client'; export type User={id:string;email:string;created_at:string};
export const login=(email:string,password:string)=>api<{user:User}>('/auth/login',{method:'POST',body:JSON.stringify({email,password})});
export const register=(email:string,password:string)=>api<{user:User}>('/auth/register',{method:'POST',body:JSON.stringify({email,password})});
export const me=()=>api<{user:User}>('/auth/me'); export const logout=()=>api<void>('/auth/logout',{method:'POST'});
