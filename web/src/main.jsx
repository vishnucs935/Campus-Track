import React, {useState, useEffect} from 'react';
import {createRoot} from 'react-dom/client';
import './style.css';

function Desk() {
  const [issues, setIssues] = useState([]);
  const [filter, setFilter] = useState('Open');
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');

  async function refresh() {
    setBusy(true);
    setError('');
    try {
      const response = await fetch('/api/issues');
      if (!response.ok) throw Error();
      setIssues(await response.json());
    } catch {
      setError('Could not load reports. Check that Django is running and refresh.');
    } finally { setBusy(false); }
  }
  useEffect(() => { refresh(); }, []);

  async function resolve(id) {
    setBusy(true);
    setError('');
    try {
      const response = await fetch('/api/issues/' + id + '/resolve', {
        method: 'POST', headers: {'Content-Type':'application/json'}, body: '{}'
      });
      if (!response.ok) throw Error();
      setIssues(items => items.map(i => i.id === id ? {...i, resolved:true} : i));
    } catch {
      setError('Could not resolve this report. Refresh to check its status.');
    } finally { setBusy(false); }
  }
  const visible = issues.filter(i => i.resolved === (filter === 'Resolved'));
  return <><header><span>Campus services</span><h1>Maintenance desk</h1></header>
    <nav aria-label="Report filters">{['Open','Resolved'].map(f =>
      <button key={f} aria-pressed={filter === f} onClick={() => setFilter(f)}>
        {f} · {issues.filter(i => i.resolved === (f === 'Resolved')).length}</button>)}
      <button className="refresh" disabled={busy} onClick={refresh}>Refresh</button></nav>
    {error && <p role="alert">{error}</p>}
    {busy && <p role="status">Updating reports…</p>}
    {!busy && !error && !visible.length && <p>No {filter.toLowerCase()} reports.</p>}
    {visible.map(i => <article key={i.id}><div><small>Report #{i.id} · {i.location}</small>
      <h2>{i.title}</h2></div>{!i.resolved && <button disabled={busy}
      onClick={() => resolve(i.id)}>Mark resolved</button>}</article>)}</>;
}
createRoot(document.querySelector('#root')).render(<Desk/>);
