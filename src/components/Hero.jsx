function Hero() {
  return (
    <section className="hero">
      <div className="hero-grid">
        <div className="hero-content">
          <div className="hero-label">
            <span className="hero-pulse" />
            AI-POWERED DEBUGGING ASSISTANT
          </div>

          <h1>
            AI debugging,
            <br />
            <span>explained.</span>
          </h1>

          <p className="hero-description">
            Stop staring at error messages. DebugMate explains what went
            wrong, why it happened, how to fix it, and what you should learn
            from it.
          </p>

          <div className="hero-actions">
            <a href="#debug" className="hero-button">
              Start Debugging
              <span>→</span>
            </a>

            <a href="#how-it-works" className="hero-secondary-button">
              See how it works
            </a>
          </div>

          <div className="hero-languages">
            <span>Supports</span>
            <span>🐍 Python</span>
            <span>🟨 JavaScript</span>
            <span>☕ Java</span>
            <span>🐹 Go</span>
          </div>
        </div>

        <div className="hero-visual" aria-hidden="true">
          <div className="hero-window">
            <div className="window-bar">
              <div className="window-dots">
                <span />
                <span />
                <span />
              </div>

              <span>debugmate.ai</span>

              <span className="window-status">● READY</span>
            </div>

            <div className="hero-code">
              <div>
                <span>01</span>
                <code>numbers = [1, 2, 3]</code>
              </div>

              <div className="error-line">
                <span>02</span>
                <code>print(numbers[5])</code>
              </div>

              <div className="error-message">
                <span>!</span>
                IndexError: list index out of range
              </div>
            </div>

            <div className="hero-analysis">
              <div className="analysis-mini-header">
                <span>✦ AI ANALYSIS</span>
                <span>READY</span>
              </div>

              <div className="analysis-mini-line">
                <span>What happened?</span>
                <span>Your code accessed an invalid list index.</span>
              </div>

              <div className="analysis-mini-line">
                <span>Learning point</span>
                <span>Lists use zero-based indexing.</span>
              </div>
            </div>
          </div>

          <div className="hero-glow" />
        </div>
      </div>
    </section>
  );
}

export default Hero;