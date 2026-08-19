const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function analyzeCode({ language, code, error }) {
  const response = await fetch(`${API_BASE_URL}/api/debug`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      language,
      code,
      error,
    }),
  });

  if (!response.ok) {
    throw new Error("Unable to analyze the code.");
  }

  return response.json();
}