import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

# Explicit path, not just load_dotenv() -- the default searches upward from
# the CURRENT WORKING DIRECTORY, which fails to find this file when
# ai_engine is imported as a sibling package (e.g. from backend/, whose
# cwd is a different directory entirely). Anchoring to this file's own
# location makes it work regardless of what process imports this module.
load_dotenv(Path(__file__).parent / ".env")

DEFAULT_API_URL = "https://olowoporoku.app.n8n.cloud/webhook/baalebos-ai"


class GatewayError(Exception):
    """Raised when the nexus-ai-gateway call fails or returns no usable text."""


class GatewayClient:
    def __init__(self, api_url: str | None = None, api_key: str | None = None, timeout: float = 45.0):
        self.api_url = api_url or os.getenv("BAALEBOS_API_URL", DEFAULT_API_URL)
        self.api_key = api_key or os.getenv("BAALEBOS_API_KEY")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "BAALEBOS_API_KEY is missing. Set it in a .env file in the "
                "ai_engine/ folder, or as an environment variable."
            )

    async def chat(self, system_prompt: str, user_prompt: str, mode: str = "auto") -> str:
        """
        The gateway takes a single `message` string, not separate system/user
        roles -- so we combine them here before sending.
        """
        combined_message = f"{system_prompt}\n\n{user_prompt}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        payload = {"message": combined_message, "mode": mode}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(self.api_url, json=payload, headers=headers)
            except httpx.TimeoutException as exc:
                raise GatewayError(f"Gateway request timed out: {exc}") from exc
            except httpx.RequestError as exc:
                raise GatewayError(f"Gateway request failed: {exc}") from exc

        if response.status_code != 200:
            raise GatewayError(
                f"Gateway returned {response.status_code}: {response.text[:300]}"
            )

        # Catch instances where n8n returns a 200 status but an empty/non-JSON string
        try:
            data = response.json()
        except ValueError as exc:
            print(f"\n[CRITICAL ERROR] n8n returned a 200 OK status but invalid/empty text data: '{response.text}'")
            raise GatewayError(
                "Gateway response could not be parsed as JSON. Check your n8n workflow node output structure."
            ) from exc

        # matches the live gateway's response shape: {"output": "...", "text": "...", ...}
        text = data.get("output") or data.get("text")
        if not text:
            raise GatewayError(f"Gateway returned no usable text: {data}")

        return text
