import { Link } from 'react-router-dom';

import { deleteFile, FileItem, patchFile, revokeShare, shareFile } from '../api/files';
import { formatBytes } from '../utils/formatBytes';
import { formatDate } from '../utils/formatDate';
import { VisibilityBadge } from './VisibilityBadge';

export function FileTable({ files, onChanged }: { files: FileItem[]; onChanged: () => void }) {
  async function makePublic(file: FileItem) {
    if (
      file.visibility === 'private' &&
      !confirm('This file will be accessible to anyone who has the share link.')
    ) {
      return;
    }
    await patchFile(file.id, { visibility: file.visibility === 'public' ? 'private' : 'public' });
    onChanged();
  }

  async function rename(file: FileItem) {
    const name = prompt('New filename', file.original_filename);
    if (name) {
      await patchFile(file.id, { original_filename: name });
      onChanged();
    }
  }

  async function share(file: FileItem) {
    const response = await shareFile(file.id);
    await navigator.clipboard?.writeText(response.share.url);
    alert(`Share link copied: ${response.share.url}`);
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Size</th>
          <th>Created</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {files.map((file) => (
          <tr key={file.id}>
            <td>
              <Link to={`/files/${file.id}`}>{file.original_filename}</Link>
            </td>
            <td>{formatBytes(file.size_bytes)}</td>
            <td>{formatDate(file.created_at)}</td>
            <td>
              <VisibilityBadge visibility={file.visibility} />
            </td>
            <td>
              <a href={`/api/files/${file.id}/download`}>Download</a>
              <button onClick={() => void rename(file)}>Rename</button>
              <button onClick={() => void makePublic(file)}>
                {file.visibility === 'public' ? 'Make private' : 'Make public'}
              </button>
              <button onClick={() => void share(file)} disabled={file.visibility !== 'public'}>
                Share
              </button>
              <button onClick={() => revokeShare(file.id).then(onChanged)}>Revoke</button>
              <button
                onClick={() => {
                  if (confirm('Delete this file?')) void deleteFile(file.id).then(onChanged);
                }}
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
