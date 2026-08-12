import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import { FileItem, getFile, patchFile, shareFile } from '../api/files';
import { ErrorAlert } from '../components/ErrorAlert';
import { VisibilityBadge } from '../components/VisibilityBadge';
import { formatBytes } from '../utils/formatBytes';
import { formatDate } from '../utils/formatDate';

export function FileDetailsPage() {
  const { id } = useParams();
  const [file, setFile] = useState<FileItem | null>(null);
  const [error, setError] = useState('');
  const [shareUrl, setShareUrl] = useState('');

  useEffect(() => {
    if (id) getFile(id).then((response) => setFile(response.file)).catch((err: Error) => setError(err.message));
  }, [id]);

  async function makePublic() {
    if (!file || !id) return;
    if (file.visibility === 'private' && !confirm('This file will be accessible to anyone who has the share link.')) {
      return;
    }
    const response = await patchFile(id, { visibility: file.visibility === 'public' ? 'private' : 'public' });
    setFile(response.file);
  }

  async function createShare() {
    if (!file || !id) return;
    const response = await shareFile(id);
    setShareUrl(response.share.url);
  }

  if (error) return <ErrorAlert message={error} />;
  if (!file) return <p>Loading file details…</p>;

  return (
    <section>
      <Link to="/">← Back to dashboard</Link>
      <h1>{file.original_filename}</h1>
      <VisibilityBadge visibility={file.visibility} />
      <dl className="details">
        <dt>Type</dt>
        <dd>{file.detected_file_type}</dd>
        <dt>MIME</dt>
        <dd>{file.mime_type}</dd>
        <dt>Size</dt>
        <dd>{formatBytes(file.size_bytes)}</dd>
        <dt>Checksum</dt>
        <dd>{file.checksum}</dd>
        <dt>Created</dt>
        <dd>{formatDate(file.created_at)}</dd>
        <dt>Updated</dt>
        <dd>{formatDate(file.updated_at)}</dd>
      </dl>
      <div className="actions">
        <a className="button" href={`/api/files/${file.id}/download`}>Download</a>
        <button onClick={() => void makePublic()}>{file.visibility === 'public' ? 'Make private' : 'Make public'}</button>
        <button onClick={() => void createShare()} disabled={file.visibility !== 'public'}>Generate share link</button>
      </div>
      {shareUrl && <p className="success">Share link: {shareUrl}</p>}
    </section>
  );
}
