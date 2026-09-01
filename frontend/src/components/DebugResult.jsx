import { useState } from "react";

function DebugResult({ result, language }) {
  const [copied, setCopied] = useState(false);

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

  const handleCopy = async () => {
    if (!possibleFix) {
      return;
    }

    try {
      await navigator.clipboard.writeText(possibleFix);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1800);
    } catch (error) {
      console.error("Unable to copy corrected code:", error);
    }
  };

  return (
    <section className="debug-result-panel" aria-live="polite">
      <div className="result-header">
        <div>
          <div className="result-eyebrow">
            <span className="result-spark">?</span>
            AI ANALYSIS
          </div>

          <h2>Here's what your code is telling us.</h2>

          <p>
            DebugMate analyzed your {language} code and error message.
          </p>
        </div>

        <div className="analysis-complete">
          <span />
          Analysis complete
        </div>
      </div>

      {errorType && (
        <div className="result-error-type">
          <span>ERROR TYPE</span>
          <strong>{errorType}</strong>
        </div>
      )}

      <div className="analysis-grid">
        <article className="analysis-card">
          <span className="analysis-number">01</span>

          <div>
            <h3>What happened?</h3>
            <p>{whatHappened || "No explanation was provided."}</p>
          </div>
        </article>

        <article className="analysis-card">
          <span className="analysis-number">02</span>

          <div>
            <h3>Why did it happen?</h3>

            {likelyCauses.length > 0 ? (
              <ul>
                {likelyCauses.map((cause, index) => (
                  <li key={index}>{cause}</li>
                ))}
              </ul>
            ) : (
              <p>No likely causes were provided.</p>
            )}
          </div>
        </article>

        <article className="analysis-card">
          <span className="analysis-number">03</span>

          <div>
            <h3>How to investigate</h3>

            {debuggingSteps.length > 0 ? (
              <ol>
                {debuggingSteps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            ) : (
              <p>No debugging steps were provided.</p>
            )}
          </div>
        </article>
      </div>

      <div className="corrected-code-section">
        <div className="code-header">
          <div>
            <span className="code-label">POSSIBLE FIX</span>
            <span className="code-language">{language}</span>
          </div>

          <button
            type="button"
            className="copy-button"
            onClick={handleCopy}
            disabled={!possibleFix}
          >
            {copied ? "? Copied" : "Copy code"}
          </button>
        </div>

        <pre className="result-code-block">
          <code>
            {possibleFix || "No possible fix was provided."}
          </code>
        </pre>

        {fixExplanation && (
          <div className="fix-explanation">
            <span className="code-label">WHY THIS FIX WORKS</span>
            <p>{fixExplanation}</p>
          </div>
        )}
      </div>

      {learningTopic && (
        <div className="learning-card">
          <div className="learning-icon">??</div>

          <div>
            <span className="learning-label">LEARNING POINT</span>
            <p>{learningTopic}</p>
          </div>
        </div>
      )}

      {practiceChallenge && (
        <div className="learning-card practice-card">
          <div className="learning-icon">?</div>

          <div>
            <span className="learning-label">PRACTICE CHALLENGE</span>
            <p>{practiceChallenge}</p>
          </div>
        </div>
      )}
    </section>
  );
}

export default DebugResult;
