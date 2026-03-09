import React, { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [spec, setSpec] = useState(null);
  const [imageBlob, setImageBlob] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch("http://localhost:8000/api/v1/infographics/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const blob = await response.blob();
    setImageBlob(URL.createObjectURL(blob));

    const specResponse = await response.json();
    setSpec(specResponse);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Research Infographic Studio</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your research prompt"
            rows={4}
            required
          />
          <button type="submit">Generate Infographic</button>
        </form>
        {spec && (
          <div className="spec">
            <h2>{spec.title}</h2>
            <p>{spec.date}</p>
            <p>{spec.summary}</p>
            <ul>
              {spec.highlights.map((highlight) => (
                <li key={highlight}>{highlight}</li>
              ))}
            </ul>
            <p>Citations:</p>
            <ul>
              {spec.citations.map((citation) => (
                <li key={citation}>{citation}</li>
              ))}
            </ul>
          </div>
        )}
        {imageBlob && <img src={imageBlob} alt="Generated infographic" />}
      </header>
    </div>
  );
}

export default App;
