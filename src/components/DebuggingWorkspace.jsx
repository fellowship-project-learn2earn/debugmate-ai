import { useState } from "react";

function DebuggingWorkspace() {
  const [language, setLanguage] = useState("Python");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    console.log({
      language,
      code,
      error,
    });
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
        <div className="form-group">
          <label htmlFor="language">Programming Language</label>

          <select
            id="language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
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
            onChange={(event) => setCode(event.target.value)}
            placeholder="Paste the code causing the error here..."
            rows="12"
          />
        </div>

        <div className="form-group">
          <label htmlFor="error">Error Message</label>

          <textarea
            id="error"
            value={error}
            onChange={(event) => setError(event.target.value)}
            placeholder="Paste the error message here..."
            rows="6"
          />
        </div>

        <button type="submit" className="debug-button">
          Explain My Error
        </button>
      </form>
    </section>
  );
}

export default DebuggingWorkspace;