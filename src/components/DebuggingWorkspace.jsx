import { useState } from "react";
import DebugResult from "./DebugResult";
import { analyzeCode } from "../services/debugService";

function DebuggingWorkspace() {
  const [language, setLanguage] = useState("Python");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Clear previous validation message
    setValidationError("");

    // Validate code
    if (!code.trim()) {
      setValidationError("Please enter the code you want to debug.");
      return;
    }

    // Validate error message
    if (!error.trim()) {
      setValidationError("Please enter the error message.");
      return;
    }

    // Remove previous result before starting a new analysis
    setResult(null);
    setStatus("loading");

    try {
      const data = await analyzeCode({
        language,
        code,
        error,
      });

      // Store the new analysis result
      setResult(data);
      setStatus("success");
    } catch (err) {
      console.error("Debug analysis failed:", err);

      setResult(null);
      setStatus("error");
    }
  };

  const handleReset = () => {
    setCode("");
    setError("");
    setValidationError("");
    setResult(null);
    setStatus("idle");
  };

  return (
    <section className="debug-workspace" id="debug">
      <div className="workspace-heading">
        <span className="eyebrow">DEBUGGING WORKSPACE</span>

        <h2>Let's understand your error.</h2>

        <p>
          Submit your code and error message. DebugMate will help explain what
          went wrong and guide you toward a solution.
        </p>
      </div>

      <form className="debug-form" onSubmit={handleSubmit}>
        {/* Validation Error */}
        {validationError && (
          <div className="validation-error" role="alert">
            {validationError}
          </div>
        )}

        {/* API Error */}
        {status === "error" && (
          <div className="api-error" role="alert">
            We couldn't analyze your error right now. Please try again.
          </div>
        )}

        {/* Programming Language */}
        <div className="form-group">
          <label htmlFor="language">Programming Language</label>

          <select
            id="language"
            value={language}
            onChange={(event) => {
              setLanguage(event.target.value);
              setValidationError("");
            }}
            disabled={status === "loading"}
          >
            <option value="Python">Python</option>
            <option value="JavaScript">JavaScript</option>
            <option value="Java">Java</option>
            <option value="C++">C++</option>
            <option value="Go">Go</option>
          </select>
        </div>

        {/* Code */}
        <div className="form-group">
          <label htmlFor="code">Your Code</label>

          <textarea
            id="code"
            value={code}
            onChange={(event) => {
              setCode(event.target.value);
              setValidationError("");
              setStatus((currentStatus) =>
                currentStatus === "error" ? "idle" : currentStatus
              );
            }}
            placeholder="Paste the code here..."
            rows="10"
            disabled={status === "loading"}
          />
        </div>

        {/* Error Message */}
        <div className="form-group">
          <label htmlFor="error">Error Message</label>

          <textarea
            id="error"
            value={error}
            onChange={(event) => {
              setError(event.target.value);
              setValidationError("");
              setStatus((currentStatus) =>
                currentStatus === "error" ? "idle" : currentStatus
              );
            }}
            placeholder="Paste the error message here..."
            rows="5"
            disabled={status === "loading"}
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="debug-button"
          disabled={status === "loading"}
        >
          {status === "loading" ? "Analyzing..." : "Explain My Error"}
        </button>

        {/* AI Result */}
        {status === "success" && result && (
          <DebugResult result={result} />
        )}

        {/* Reset */}
        {status === "success" && (
          <button
            type="button"
            className="reset-button"
            onClick={handleReset}
          >
            Debug Another Error
          </button>
        )}
      </form>
    </section>
  );
}

export default DebuggingWorkspace;