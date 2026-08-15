function DebugResult({ result }) {
  if (!result) {
    return null;
  }

  return (
    <section className="debug-result-panel">
      <div className="result-header">
        <p className="section-label">AI ANALYSIS</p>
        <h2>Here's what happened.</h2>
      </div>

      <div className="result-section">
        <h3>What happened?</h3>
        <p>{result.summary}</p>
      </div>

      <div className="result-section">
        <h3>Why did it happen?</h3>
        <p>{result.cause}</p>
      </div>

      <div className="result-section">
        <h3>How to fix it</h3>
        <p>{result.solution}</p>
      </div>

      <div className="result-section">
        <h3>Corrected code</h3>

        <pre className="code-block">
          <code>{result.correctedCode}</code>
        </pre>
      </div>

      <div className="result-learning">
        <p className="result-label">WHAT YOU LEARNED</p>

        <p>{result.learningPoint}</p>
      </div>
    </section>
  );
}

export default DebugResult;