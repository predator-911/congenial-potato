import { useEffect, useState } from 'react';

import { FileItem, listFiles } from '../api/files';
import { EmptyState } from '../components/EmptyState';
import { FileTable } from '../components/FileTable';
import { formatBytes } from '../utils/formatBytes';

export function DashboardPage() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [usage, setUsage] = useState(0);
  const [search, setSearch] = useState('');
  const [visibility, setVisibility] = useState('');
  const [type, setType] = useState('');
  const [sort, setSort] = useState('date');
  const [direction, setDirection] = useState('desc');

  const load = () =>
    listFiles({ search, visibility, type, sort, direction }).then((response) => {
      setFiles(response.items);
      setUsage(response.storage_usage_bytes);
    });

  useEffect(() => {
    void load();
  }, []);

  const publicCount = files.filter((file) => file.visibility === 'public').length;

  return (
    <>
      <section className="hero">
        <h1>Your secure vault</h1>
        <div className="stats">
          <b>{files.length}</b> files <b>{formatBytes(usage)}</b> used <b>{publicCount}</b> public{' '}
          <b>{files.length - publicCount}</b> private
        </div>
      </section>
      <section className="toolbar">
        <input placeholder="Search filenames" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select value={visibility} onChange={(event) => setVisibility(event.target.value)} aria-label="Visibility filter">
          <option value="">All visibility</option>
          <option value="private">Private</option>
          <option value="public">Public</option>
        </select>
        <select value={type} onChange={(event) => setType(event.target.value)} aria-label="File type filter">
          <option value="">All types</option>
          <option value="pdf">PDF</option>
          <option value="png">PNG</option>
          <option value="jpeg">JPEG</option>
          <option value="txt">TXT</option>
          <option value="csv">CSV</option>
          <option value="docx">DOCX</option>
        </select>
        <select value={sort} onChange={(event) => setSort(event.target.value)} aria-label="Sort by">
          <option value="date">Date</option>
          <option value="name">Name</option>
          <option value="size">Size</option>
        </select>
        <select value={direction} onChange={(event) => setDirection(event.target.value)} aria-label="Sort direction">
          <option value="desc">Descending</option>
          <option value="asc">Ascending</option>
        </select>
        <button onClick={load}>Apply</button>
      </section>
      {files.length ? <FileTable files={files} onChanged={load} /> : <EmptyState />}
    </>
  );
}
