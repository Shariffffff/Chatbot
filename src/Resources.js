<<<<<<< HEAD
=======
import React, { useState } from 'react';
import './Resources.css';
import axios from 'axios';

function Resources() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const backendUrl = 'http://ec2-18-133-64-91.eu-west-2.compute.amazonaws.com:5000';

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
      const response = await axios.post(`${backendUrl}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
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
>>>>>>> d53a1ae (updates)
