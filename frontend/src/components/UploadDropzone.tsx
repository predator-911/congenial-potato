import { useState } from 'react';

import { uploadFile } from '../api/files';
import { ErrorAlert } from './ErrorAlert';
import { UploadProgress } from './UploadProgress';

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.txt', '.csv', '.docx'];
const LARGE_WARNING_BYTES = 100 * 1024 * 1024;
const MAX_BYTES = 250 * 1024 * 1024;

function extensionOf(name: string) {
  const index = name.lastIndexOf('.');
  return index >= 0 ? name.slice(index).toLowerCase() : '';
}

export function UploadDropzone({ onDone }: { onDone: () => void }) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [speed, setSpeed] = useState(0);
  const [eta, setEta] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [busy, setBusy] = useState(false);
  const [controller, setController] = useState<AbortController | null>(null);

  function validate(file: File) {
    if (file.size === 0) return 'Empty files are not allowed.';
    if (file.size > MAX_BYTES) return 'This file is larger than the 250 MB local limit.';
    if (!ALLOWED_EXTENSIONS.includes(extensionOf(file.name))) {
      return 'Allowed file types are PDF, PNG, JPG, TXT, CSV, and DOCX.';
    }
    return '';
  }

  async function send(file: File) {
    const validationError = validate(file);
    setSelectedFile(file);
    setError(validationError);
    setSuccess('');
    setProgress(0);
    if (validationError) return;

    setBusy(true);
    const nextController = new AbortController();
    setController(nextController);
    try {
      await uploadFile(
        file,
        (nextProgress, nextSpeed, nextEta) => {
          setProgress(nextProgress);
          setSpeed(nextSpeed);
          setEta(nextEta);
        },
        nextController.signal,
      );
      setSuccess('Upload complete. Your file is private by default.');
      setProgress(100);
      window.setTimeout(onDone, 700);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed.');
    } finally {
      setBusy(false);
      setController(null);
    }
  }

  return (
    <section
      className="drop"
      onDragOver={(event) => event.preventDefault()}
      onDrop={(event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        if (file) void send(file);
      }}
    >
      <h2>Secure upload</h2>
      <p>Drag and drop a PDF, PNG, JPG, TXT, CSV, or DOCX. Large files up to 250 MB are streamed.</p>
      <input
        aria-label="Choose file"
        type="file"
        accept=".pdf,.png,.jpg,.jpeg,.txt,.csv,.docx"
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (file) void send(file);
        }}
      />
      {selectedFile && selectedFile.size >= LARGE_WARNING_BYTES && (
        <p className="warning">Large file selected. Keep this tab open while upload progress completes.</p>
      )}
      {(busy || progress > 0) && <UploadProgress p={progress} speed={speed} eta={eta} />}
      {busy && <button onClick={() => controller?.abort()}>Cancel</button>}
      {success && <p className="success">{success}</p>}
      <ErrorAlert message={error} />
      {error && selectedFile && !busy && <button onClick={() => void send(selectedFile)}>Retry</button>}
    </section>
  );
}
