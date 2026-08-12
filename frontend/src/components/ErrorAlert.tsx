export function ErrorAlert({message}:{message?:string}){return message?<div role="alert" className="error">{message}</div>:null}
