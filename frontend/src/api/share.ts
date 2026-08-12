import {api} from './client'; export const publicMeta=(token:string)=>api<any>(`/share/${token}`);
