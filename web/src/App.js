import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [spamScore, setSpamScore] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    setError(null);
    setSpamScore(null);
    const formData = new FormData();
    formData.append('file', acceptedFiles[0]);

    try {
      const response = await axios.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSpamScore(response.data.spam_score.toFixed(2));
    } catch (err) {
      setError(err.response ? err.response.data : err.message);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'image/*',
    maxFiles: 1,
  });

  return (
    <div className="container">
      <div className="row mt-5">
        <div className="col">
          <h1 className="text-center mb-4">Email Spam Detection</h1>
          <div
            {...getRootProps()}
            className={`border border-3 border-dashed rounded p-3 mb-3 ${
              isDragActive ? 'border-primary' : 'border-secondary'
            }`}
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <p className="text-center">Drop the image here...</p>
            ) : (
              <p className="text-center">
                Drag and drop an image here, or click to select a file
              </p>
            )}
          </div>
          {spamScore && (
            <div className="alert alert-info" role="alert">
              Spam Score: {spamScore}
            </div>
          )}
          {error && (
            <div className="alert alert-danger" role="alert">
              Error: {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
