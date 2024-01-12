import React, { useState } from 'react';
import './Bot.css';

function Bot() {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const backendUrl = 'http://3.8.181.7:5000';  // Update with your EC2 instance public IP address

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const newMessage = { text: userInput, sender: 'user' };
    setMessages([...messages, newMessage]);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
      });
      const data = await response.json();

      const botResponse = { text: data.response, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botResponse]);
    } catch (error) {
      console.error('Error:', error);
    }

    setUserInput('');
  };

  return (
    <div className="chatbot-container">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          placeholder="Type your message here..."
          className="input-field"
        />
        <button type="submit" className="submit-button">Send</button>
      </form>
    </div>
  );
}

export default Bot;
