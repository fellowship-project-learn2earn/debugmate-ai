import { useState } from "react";

function DebugResult({ result, language }) {
  const [copied, setCopied] = useState(false);

  if (!result) {
    return null;
  }

  const handleCopy = async () => {
    if (!result.correctedCode) {
      return;
    }

    try {
      await navigator.clipboard.writeText(result.correctedCode);
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
            <span className="result-spark">✦</span>
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

      <div className="analysis-grid">
        <article className="analysis-card">
          <span className="analysis-number">01</span>
          <div>
            <h3>What happened?</h3>
            <p>{result.whatHappened}</p>
          </div>
        </article>

        <article className="analysis-card">
          <span className="analysis-number">02</span>
          <div>
            <h3>Why did it happen?</h3>
            <p>{result.whyItHappened}</p>
          </div>
        </article>

        <article className="analysis-card">
          <span className="analysis-number">03</span>
          <div>
            <h3>How to fix it</h3>
            <p>{result.howToFix}</p>
          </div>
        </article>
      </div>

      <div className="corrected-code-section">
        <div className="code-header">
          <div>
            <span className="code-label">CORRECTED CODE</span>
            <span className="code-language">{language}</span>
          </div>

          <button
            type="button"
            className="copy-button"
            onClick={handleCopy}
            disabled={!result.correctedCode}
          >
            {copied ? "✓ Copied" : "Copy code"}
          </button>
        </div>

        <pre className="result-code-block">
          <code>
            {result.correctedCode || "No corrected code was provided."}
          </code>
        </pre>
      </div>

      <div className="learning-card">
        <div className="learning-icon">💡</div>

        <div>
          <span className="learning-label">LEARNING POINT</span>

          <p>{result.learningPoint}</p>
        </div>
      </div>
    </section>
  );
}

export default DebugResult;