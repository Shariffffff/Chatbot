import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import Resources from './Resources';
import DocumentList from './DocumentList';
import Bot from './Bot'; // Ensure you have a Chatbot component



const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/upload" element={<Resources />} />
        <Route path="/chat" element={<Bot />} />
        <Route path="/documents" element={<DocumentList />} />

      </Routes>
    </Router>
  );
};

export default App;
