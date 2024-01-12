import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DocumentList.css';

function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const backendUrl = 'http://3.8.181.7:5000';  // Update with your EC2 instance public IP address

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${backendUrl}/documents`);
      setDocuments(response.data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching documents:', error);
      setIsLoading(false);
    }
  };

  const handleDelete = async (documentId) => {
    try {
      await axios.delete(`${backendUrl}/documents/delete/${documentId}`);
      fetchDocuments(); // Refresh the list after deletion
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  if (isLoading) return <p>Loading documents...</p>;

  return (
    <div className="DocumentList">
      <h2>Uploaded Documents</h2>
      <ul>
        {documents.map(doc => (
          <li key={doc.id}>
            {doc.filename} (Uploaded on: {doc.upload_date})
            {' '}
            <a href={`${backendUrl}/documents/${doc.filename}`} target="_blank" rel="noopener noreferrer">
              View Document
            </a>
            {' '}
            <button onClick={() => handleDelete(doc.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default DocumentList;
