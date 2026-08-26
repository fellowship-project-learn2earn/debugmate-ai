function DebugResult({ result }) {
  if (!result) {
    return null;
  }

  const {
    error_type: errorType,
    what_happened: whatHappened,
    likely_causes: likelyCauses = [],
    debugging_steps: debuggingSteps = [],
    possible_fix: possibleFix,
    fix_explanation: fixExplanation,
    learning_topic: learningTopic,
    practice_challenge: practiceChallenge,
  } = result;

  return (
    <section className="debug-result-panel">
      <div className="result-header">
        <p className="section-label">AI ANALYSIS</p>
        <h2>Here's what happened.</h2>
        {errorType && <span className="error-type-badge">{errorType}</span>}
      </div>

      <div className="result-section">
        <h3>What happened?</h3>
        <p>{whatHappened}</p>
      </div>

      {likelyCauses.length > 0 && (
        <div className="result-section">
          <h3>Likely causes</h3>
          <ul>
            {likelyCauses.map((cause, i) => (
              <li key={i}>{cause}</li>
            ))}
          </ul>
        </div>
      )}

      {debuggingSteps.length > 0 && (
        <div className="result-section">
          <h3>How to investigate</h3>
          <ol>
            {debuggingSteps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
      )}

      <div className="result-section">
        <h3>Possible fix</h3>
        <pre className="code-block">
          <code>{possibleFix}</code>
        </pre>
        {fixExplanation && <p>{fixExplanation}</p>}
      </div>

      {learningTopic && (
        <div className="result-learning">
          <p className="result-label">WHAT TO LEARN</p>
          <p>{learningTopic}</p>
        </div>
      )}

      {practiceChallenge && (
        <div className="result-practice">
          <p className="result-label">PRACTICE CHALLENGE</p>
          <p>{practiceChallenge}</p>
        </div>
      )}
    </section>
  );
}

export default DebugResult;