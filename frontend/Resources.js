import React, { useState } from 'react';
import './Resources.css'; // Make sure this file exists and contains your CSS
import axios from 'axios';

function Resources() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }

    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData);
      alert('File uploaded successfully: ' + response.data.message);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file: ' + (error.response?.data?.error || error.message));
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="Resources">
      <h1>Upload Document for Chatbot</h1>
      {isUploading ? (
        <p>Uploading...</p>
      ) : (
        <>
          <input type="file" onChange={handleFileInput} />
          <button onClick={handleFileUpload} disabled={!selectedFile || isUploading}>
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>
        </>
      )}
    </div>
  );
}

export default Resources;
