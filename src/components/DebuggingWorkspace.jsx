import { useMemo, useState } from "react";
import DebugResult from "./DebugResult";
import { analyzeCode } from "../services/debugService";

const LANGUAGES = [
  {
    name: "Python",
    icon: "🐍",
    status: "available",
    placeholder:
      "numbers = [1, 2, 3]\nprint(numbers[5])",
    errorPlaceholder:
      "IndexError: list index out of range",
  },
  {
    name: "JavaScript",
    icon: "🟨",
    status: "available",
    placeholder:
      "const user = undefined;\nconsole.log(user.name);",
    errorPlaceholder:
      "TypeError: Cannot read properties of undefined",
  },
  {
    name: "Java",
    icon: "☕",
    status: "available",
    placeholder:
      'public class Main {\n  public static void main(String[] args) {\n    int[] numbers = {1, 2, 3};\n    System.out.println(numbers[5]);\n  }\n}',
    errorPlaceholder:
      "ArrayIndexOutOfBoundsException",
  },
  {
    name: "Go",
    icon: "🐹",
    status: "available",
    placeholder:
      'package main\n\nimport "fmt"\n\nfunc main() {\n    numbers := []int{1, 2, 3}\n    fmt.Println(numbers[5])\n}',
    errorPlaceholder:
      "panic: runtime error: index out of range",
  },
  {
    name: "Rust",
    icon: "🦀",
    status: "coming-soon",
    placeholder: "",
    errorPlaceholder: "",
  },
  {
    name: "C",
    icon: "C",
    status: "coming-soon",
    placeholder: "",
    errorPlaceholder: "",
  },
  {
    name: "C++",
    icon: "C++",
    status: "coming-soon",
    placeholder: "",
    errorPlaceholder: "",
  },
];

function DebuggingWorkspace() {
  const [language, setLanguage] = useState("Python");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);

  const selectedLanguage = useMemo(
    () => LANGUAGES.find((item) => item.name === language),
    [language]
  );

  const lineCount = Math.max(code.split("\n").length, 1);

  const handleSubmit = async (event) => {
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

    setResult(null);
    setStatus("loading");

    try {
      const data = await analyzeCode({
        language,
        code,
        error,
      });

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

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
    setValidationError("");
    setStatus((currentStatus) =>
      currentStatus === "error" ? "idle" : currentStatus
    );
  };

  return (
    <section className="debug-workspace" id="debug">
      <div className="workspace-heading">
        <div>
          <span className="eyebrow">DEBUGGING WORKSPACE</span>

          <h2>Turn an error into a lesson.</h2>

          <p>
            Select your language, paste your code and error, then let
            DebugMate explain what went wrong and how to fix it.
          </p>
        </div>

        <div className="workspace-status">
          <span className="status-dot" />
          AI debugging assistant
        </div>
      </div>

      <form className="debug-form" onSubmit={handleSubmit}>
        {validationError && (
          <div className="message-box validation-error" role="alert">
            <strong>Check your input</strong>
            <span>{validationError}</span>
          </div>
        )}

        {status === "error" && (
          <div className="message-box api-error" role="alert">
            <strong>Analysis unavailable</strong>
            <span>
              Something went wrong while analyzing your code. Please try
              again.
            </span>
          </div>
        )}

        <div className="workspace-toolbar">
          <div className="language-control">
            <label htmlFor="language">Language</label>

            <div className="language-select-wrapper">
              <span className="language-icon">
                {selectedLanguage?.icon}
              </span>

              <select
                id="language"
                value={language}
                onChange={handleLanguageChange}
                disabled={status === "loading"}
              >
                {LANGUAGES.map((item) => (
                  <option
                    key={item.name}
                    value={item.name}
                    disabled={item.status === "coming-soon"}
                  >
                    {item.name}
                    {item.status === "coming-soon" ? " — Coming Soon" : ""}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="supported-indicator">
            <span className="supported-dot" />
            {selectedLanguage?.name} supported
          </div>
        </div>

        <div className="editor-section">
          <div className="field-heading">
            <label htmlFor="code">Your Code</label>
            <span>{selectedLanguage?.name}</span>
          </div>

          <div className="code-editor">
            <div className="line-numbers" aria-hidden="true">
              {Array.from({ length: lineCount }, (_, index) => (
                <span key={index}>{index + 1}</span>
              ))}
            </div>

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
              placeholder={selectedLanguage?.placeholder}
              spellCheck="false"
              disabled={status === "loading"}
              aria-label={`Enter your ${language} code`}
            />
          </div>
        </div>

        <div className="editor-section">
          <div className="field-heading">
            <label htmlFor="error">Error Message</label>
            <span>Paste the exact error</span>
          </div>

          <textarea
            id="error"
            className="error-input"
            value={error}
            onChange={(event) => {
              setError(event.target.value);
              setValidationError("");
              setStatus((currentStatus) =>
                currentStatus === "error" ? "idle" : currentStatus
              );
            }}
            placeholder={selectedLanguage?.errorPlaceholder}
            rows="4"
            spellCheck="false"
            disabled={status === "loading"}
          />
        </div>

        <div className="submit-area">
          <button
            type="submit"
            className="debug-button"
            disabled={status === "loading"}
          >
            {status === "loading" ? (
              <>
                <span className="button-spinner" />
                Analyzing your code...
              </>
            ) : (
              <>
                <span>✦</span>
                Explain My Error
              </>
            )}
          </button>

          <p>
            DebugMate analyzes your code and error together to give you a
            structured explanation.
          </p>
        </div>

        {status === "success" && result && (
          <DebugResult result={result} language={language} />
        )}

        {status === "success" && (
          <button
            type="button"
            className="reset-button"
            onClick={handleReset}
          >
            ← Debug Another Error
          </button>
        )}
      </form>
    </section>
  );
}

export default DebuggingWorkspace;