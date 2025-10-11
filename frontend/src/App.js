import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:5000');

function App() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const outputRef = useRef(null);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('terminal_output', (data) => {
      setOutput((prevOutput) => prevOutput + data.output);
    });

    return () => {
      socket.off('connect');
      socket.off('terminal_output');
    };
  }, []);

  useEffect(() => {
    // Auto-scroll to the bottom
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [output]);

  const handleSend = () => {
    if (input.trim()) {
      socket.emit('terminal_input', { input });
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Taskwithbat - Interactive CLI</h1>
        <div className="terminal-container">
          <pre className="output" ref={outputRef}>
            {output}
          </pre>
          <div className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter command..."
              autoFocus
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;