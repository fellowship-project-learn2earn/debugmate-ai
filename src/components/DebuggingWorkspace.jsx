import { useState } from "react";

function DebuggingWorkspace() {
  const [language, setLanguage] = useState("Python");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const [validationError, setValidationError] = useState("");
  const [status, setStatus] = useState("idle");

  const handleSubmit = (event) => {
    event.preventDefault();

    setValidationError("");

    if (!code.trim()) {
      setValidationError("Please enter the code you want to debug.");
      return;
    }

    if (!error.trim()) {
      setValidationError("Please enter the error message.");
      return;
    }

    setStatus("loading");

    console.log({
      language,
      code,
      error,
    });

    setTimeout(() => {
      setStatus("success");
    }, 1500);
  };

  return (
    <section className="debug-workspace" id="debug">
      <div className="workspace-heading">
        <p className="section-label">DEBUGGING WORKSPACE</p>

        <h2>Let's understand your error.</h2>

        <p>
          Submit your code and error message. DebugMate will help explain what
          went wrong and guide you toward a solution.
        </p>
      </div>

      <form className="debug-form" onSubmit={handleSubmit}>
        {validationError && (
          <div className="form-error" role="alert">
            {validationError}
          </div>
        )}

        <div className="form-group">
          <label htmlFor="language">Programming Language</label>

          <select
            id="language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
            disabled={status === "loading"}
          >
            <option value="Python">Python</option>
            <option value="JavaScript">JavaScript</option>
            <option value="Java">Java</option>
            <option value="C++">C++</option>
            <option value="Go">Go</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="code">Your Code</label>

          <textarea
            id="code"
            value={code}
            onChange={(event) => {
  setCode(event.target.value);
  setValidationError("");
}}
            placeholder="Paste the code causing the error here..."
            rows="12"
            disabled={status === "loading"}
          />
        </div>

        <div className="form-group">
          <label htmlFor="error">Error Message</label>

          <textarea
            id="error"
            value={error}
            onChange={(event) => {
  setError(event.target.value);
  setValidationError("");
}}
            placeholder="Paste the error message here..."
            rows="6"
            disabled={status === "loading"}
          />
        </div>

        <button
          type="submit"
          className="debug-button"
          disabled={status === "loading"}
        >
          {status === "loading" ? "Analyzing..." : "Explain My Error"}
        </button>

        {status === "success" && (
  <div className="debug-result">
    <p className="result-label">ANALYSIS READY</p>

    <h3>Your debugging request was submitted successfully.</h3>

    <p>
      The AI explanation will appear here once the backend is connected.
    </p>

    <button
      type="button"
      className="reset-button"
      onClick={() => {
        setCode("");
        setError("");
        setStatus("idle");
        setValidationError("");
      }}
    >
      Debug Another Error
    </button>
  </div>
)}
      </form>
    </section>
  );
}

export default DebuggingWorkspace;