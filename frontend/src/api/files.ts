import { api, csrf } from './client';

export type FileItem = {
  id: string;
  original_filename: string;
  mime_type: string;
  detected_file_type: string;
  size_bytes: number;
  visibility: 'private' | 'public';
  checksum: string;
  created_at: string;
  updated_at: string;
};

export type FileListQuery = {
  search?: string;
  visibility?: string;
  type?: string;
  sort?: string;
  direction?: string;
};

export function listFiles(query: FileListQuery = {}) {
  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  const suffix = params.toString() ? `?${params.toString()}` : '';
  return api<{ items: FileItem[]; total: number; storage_usage_bytes: number }>(`/files${suffix}`);
}

export const getFile = (id: string) => api<{ file: FileItem }>(`/files/${id}`);

export const patchFile = (
  id: string,
  body: Partial<Pick<FileItem, 'original_filename' | 'visibility'>>,
) => api<{ file: FileItem }>(`/files/${id}`, { method: 'PATCH', body: JSON.stringify(body) });

export const deleteFile = (id: string) => api<void>(`/files/${id}`, { method: 'DELETE' });

export const shareFile = (id: string) =>
  api<{ share: { url: string; expires_at: string | null; created_at: string } }>(`/files/${id}/share`, {
    method: 'POST',
    body: JSON.stringify({}),
  });

export const revokeShare = (id: string) => api<void>(`/files/${id}/share`, { method: 'DELETE' });

export function uploadFile(
  file: File,
  onProgress: (p: number, speed: number, eta: number) => void,
  signal?: AbortSignal,
): Promise<FileItem> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const start = Date.now();
    xhr.open('POST', '/api/files');
    xhr.withCredentials = true;
    xhr.setRequestHeader('X-CSRF-Token', csrf());
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const seconds = (Date.now() - start) / 1000;
        const speed = event.loaded / Math.max(seconds, 0.1);
        onProgress(Math.round((event.loaded / event.total) * 100), speed, (event.total - event.loaded) / Math.max(speed, 1));
      }
    };
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.responseText).file);
        return;
      }
      try {
        reject(new Error(JSON.parse(xhr.responseText).error.message));
      } catch {
        reject(new Error(xhr.statusText || 'Upload failed.'));
      }
    };
    xhr.onerror = () => reject(new Error('Network upload failed.'));
    signal?.addEventListener('abort', () => {
      xhr.abort();
      reject(new Error('Upload cancelled.'));
    });
    const form = new FormData();
    form.append('file', file);
    xhr.send(form);
  });
}
