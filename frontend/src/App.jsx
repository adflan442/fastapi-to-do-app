import { useEffect, useState } from 'react';
import DOMPurify from 'dompurify';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
    <div>
      <h1>FastAPI + React</h1>
      <p 
        dangerouslySetInnerHTML={{
          __html : data ? DOMPurify.sanitize(data['message']) : 'Loading data...',
          }}>
      </p>
    </div>
  );
}

export default App;