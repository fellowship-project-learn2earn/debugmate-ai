const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function analyzeCode({ language, code, error, intendedBehavior }) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      language: language.toLowerCase(),
      code,
      error_message: error,
      ...(intendedBehavior ? { intended_behavior: intendedBehavior } : {}),
    }),
  });

  if (!response.ok) {
    let message = "Unable to analyze the code.";
    try {
      const body = await response.json();
      message = body?.detail?.message || message;
    } catch {
      // response wasn't JSON — fall back to the default message
    }
    throw new Error(message);
  }

  return response.json();
}