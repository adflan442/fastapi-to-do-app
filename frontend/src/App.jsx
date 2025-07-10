import { useState } from 'react';

function App() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('http://127.0.0.1:8000/echo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      setResponse(data.message);
    } catch (err) {
      setResponse("Error contacting the API");
      console.error(err);
    }
  };

  return (
    <div>
      <h1>Send to FastAPI</h1>
      <form onSubmit={handleSubmit}>
        <input 
          type="text"
          placeholder="Type something"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {response && <p>{response}</p>}
    </div>
  );
}

export default App;