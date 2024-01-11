// LandingPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css'; // Ensure you have this CSS file for styling

const LandingPage = () => {
  return (
    <div className="landing-page">
      <h1>Welcome to the Autism Support Chatbot</h1>
      <div className="sections-container">
        <section className="specialist-section">
          <h2>For Specialists</h2>
          <p>If you are a specialist, you can upload and manage documents containing information on autism to help improve the chatbot's responses.</p>
          <Link to="/upload">Upload Documents</Link>
          <br/>
          <Link to="/documents">View Uploaded Documents</Link>
        </section>
        <section className="user-section">
          <h2>For Users</h2>
          <p>Need assistance or information? Chat with our bot now!</p>
          <Link to="/chat">Start Chatting</Link>
        </section>
      </div>
    </div>
  );
};

export default LandingPage;
