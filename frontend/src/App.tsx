import {useEffect,useState} from "react";

const API="http://127.0.0.1:8001";

type Result={columns:string[];rows:Record<string,any>[];row_count:number;truncated:boolean};
type Answer={question:string;sql:string;results:Result;explanation:string};

export default function App(){
 const [question,setQuestion]=useState("Show average score by course");
 const [answer,setAnswer]=useState<Answer|null>(null);
 const [schema,setSchema]=useState<any>(null);
 const [status,setStatus]=useState("Checking backend...");
 const [busy,setBusy]=useState(false);
 const [error,setError]=useState("");
 const [mode,setMode]=useState("ask");
 const [dashboard,setDashboard]=useState<any>(null);
 const [analysis,setAnalysis]=useState<any>(null);

 useEffect(()=>{fetch(API+"/health").then(r=>r.json()).then(()=>setStatus("Backend online")).catch(()=>setStatus("Backend offline"));},[]);

 async function run(){
  setBusy(true);setError("");setAnswer(null);setDashboard(null);setAnalysis(null);
  try{
   const endpoint=mode==="ask"?"/ask":mode==="analysis"?"/analyze":"/dashboard";
   const body=mode==="ask"?{question,limit:20}:mode==="analysis"?{question,limit:20}:{prompt:question,limit:20};
   const r=await fetch(API+endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
   const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Request failed");
   if(mode==="ask")setAnswer(data); else if(mode==="analysis")setAnalysis(data); else setDashboard(data);
  }catch(e:any){setError(e.message)}finally{setBusy(false)}
 }
 async function loadSchema(){try{const r=await fetch(API+"/schema");setSchema(await r.json())}catch(e:any){setError(e.message)}}

 return <div className="page">
  <header><div><div className="brand">SQL<span>Mind</span></div><p>AI-powered read-only database analytics</p></div><div className="status">{status}</div></header>
  <main>
   <section className="hero"><h1>Ask your database anything.</h1><p>Natural language → safe SQL → results → insights.</p></section>
   <section className="card">
    <div className="modes">{["ask","analysis","dashboard"].map(m=><button className={mode===m?"active":""} onClick={()=>setMode(m)} key={m}>{m==="ask"?"Ask":m==="analysis"?"Smart Analysis":"Dashboard"}</button>)}</div>
    <textarea value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask a question about the database..."/>
    <div className="actions"><button className="primary" disabled={busy} onClick={run}>{busy?"Running...":"Run SQLMind"}</button><button onClick={loadSchema}>View Schema</button></div>
    {error&&<div className="error">{error}</div>}
   </section>

   {schema&&<section className="card"><h2>Database Schema</h2>{schema.tables?.map((t:any)=><div className="schema" key={t.name}><b>{t.name}</b><span>{t.columns.map((c:any)=>c.name+" : "+c.type).join("  |  ")}</span></div>)}</section>}

   {answer&&<section className="card"><h2>Generated SQL</h2><pre>{answer.sql}</pre><h2>Results ({answer.results.row_count})</h2><table><thead><tr>{answer.results.columns.map(c=><th key={c}>{c}</th>)}</tr></thead><tbody>{answer.results.rows.map((row,i)=><tr key={i}>{answer.results.columns.map(c=><td key={c}>{String(row[c])}</td>)}</tr>)}</tbody></table><h2>AI Explanation</h2><p>{answer.explanation}</p></section>}

   {analysis&&<section className="card"><h2>Smart Analysis</h2><p>{analysis.insight}</p>{analysis.steps?.map((s:any)=><div className="result" key={s.step}><b>{s.step}</b><pre>{s.sql}</pre><table><thead><tr>{s.results.columns.map((c:string)=><th key={c}>{c}</th>)}</tr></thead><tbody>{s.results.rows.map((row:any,i:number)=><tr key={i}>{s.results.columns.map((c:string)=><td key={c}>{String(row[c])}</td>)}</tr>)}</tbody></table></div>)}</section>}

   {dashboard&&<section className="card"><h2>{dashboard.title}</h2><p>{dashboard.insight}</p><div className="grid">{dashboard.widgets?.map((w:any)=><div className="widget" key={w.title}><h3>{w.title}</h3><pre>{w.sql}</pre>{w.results.rows?.map((r:any,i:number)=><div className="metric" key={i}>{Object.entries(r).map(([k,v])=><span key={k}><b>{k}</b> {String(v)}</span>)}</div>)}</div>)}</div></section>}
  </main>
 </div>
}