import React, { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus("loading");
    setError("");

    try {
      const response = await fetch("http://localhost:8000/api/v1/infographics/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate infographic");
      }

      const payload = await response.json();
      setResult(payload);
      setStatus("success");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
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
        {status === "loading" && <p className="status">Generating infographic...</p>}
        {error && <p className="error">{error}</p>}
        {result && (
          <div className="result">
            {result.spec && (
              <div className="spec">
                <h2>{result.spec.title}</h2>
                <p>{result.spec.date}</p>
                <p>{result.spec.summary}</p>
                <ul>
                  {result.spec.highlights.map((highlight) => (
                    <li key={highlight}>{highlight}</li>
                  ))}
                </ul>
                <p>Citations:</p>
                <ul>
                  {result.spec.citations.map((citation) => (
                    <li key={citation}>{citation}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.sources && (
              <div className="sources">
                <h3>Sources</h3>
                <ul>
                  {result.sources.map((source) => (
                    <li key={source.url}>
                      <a href={source.url} target="_blank" rel="noreferrer">
                        {source.title}
                      </a>
                      <p>{source.publisher} · {source.publish_date}</p>
                      <p>{source.snippet}</p>
                      <p className="reliability">Reliability: {source.reliability}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.confidence_note && (
              <div className="confidence">
                <h3>Confidence & Trust Notes</h3>
                <p>{result.confidence_note}</p>
              </div>
            )}

            {result.provenance && (
              <div className="provenance">
                <h3>Provenance</h3>
                <p>Sources fetched at: {result.provenance.sources_fetched_at}</p>
                <p>Last accessed at: {result.provenance.last_accessed_at}</p>
                <p>Retrieval method: {result.provenance.retrieval_method}</p>
                <p>Provider: {result.provenance.provider}</p>
                <p>Sources used: {result.provenance.source_count}</p>
              </div>
            )}

            {result.image_url && (
              <div className="image-preview">
                <h3>Infographic</h3>
                <img src={result.image_url} alt="Generated infographic" />
              </div>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
