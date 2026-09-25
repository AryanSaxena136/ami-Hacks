from __future__ import annotations

import os
from typing import Any

import httpx

try:
    from langchain_groq import ChatGroq
except ImportError:  # pragma: no cover - optional dependency at runtime
    ChatGroq = None


class SummaryService:
    def _build_summary_prompt(self, data: dict[str, Any]) -> str:
        zone = data.get("zone") or "the monitored zone"
        rainfall = float(data.get("rainfall", 0) or 0)
        traffic = float(data.get("traffic", 0) or 0)
        incident_reports = float(data.get("incident_reports", 0) or 0)

        return (
            "You are a civic operations analyst helping a city dashboard. "
            f"The current situation in {zone} is: rainfall={rainfall}, traffic_congestion={traffic}, "
            f"incident_reports={incident_reports}. "
            "Your job is to generate a brief, actionable summary for city operators. "
            "Interpret the live data, explain what is happening, note the operational impact, "
            "and keep the summary concise, specific, and suitable for a dashboard. "
            "Do not use fixed templates or generic threshold text. Write a unique summary based on the current signals."
        )

    def _extract_llm_content(self, payload: dict[str, Any]) -> str | None:
        choices = payload.get("choices") or []
        if not choices:
            output_text = payload.get("output_text")
            if isinstance(output_text, str) and output_text.strip():
                return output_text.strip()
            return None

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            return None

        message = first_choice.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
            if isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict):
                        text = part.get("text")
                        if isinstance(text, str):
                            parts.append(text)
                combined = "".join(parts).strip()
                if combined:
                    return combined

        text = first_choice.get("text")
        if isinstance(text, str) and text.strip():
            return text.strip()

        return None

    def _llm_config(self) -> tuple[str, str, str] | None:
        api_key = os.getenv("GROK_API_KEY") or os.getenv("LLM_API_KEY")
        if not api_key:
            return None

        model = os.getenv("GROK_MODEL") or os.getenv("LLM_MODEL") or (
            "grok-2-latest" if os.getenv("GROK_API_KEY") else "gpt-4o-mini"
        )
        base_url = (
            os.getenv("GROK_BASE_URL") or os.getenv("LLM_BASE_URL") or (
                "https://api.x.ai/v1" if os.getenv("GROK_API_KEY") else "https://api.openai.com/v1"
            )
        ).rstrip("/")
        return api_key, model, base_url

    def _langchain_groq_summary(self, data: dict[str, Any]) -> str | None:
        if ChatGroq is None:
            return None

        api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")
        if not api_key:
            return None

        prompt = self._build_summary_prompt(data)

        try:
            model = ChatGroq(
                model=os.getenv("GROQ_MODEL") or os.getenv("GROK_MODEL") or "llama-3.3-70b-versatile",
                api_key=api_key,
                temperature=0.2,
            )
            result = model.invoke(prompt)
            content = getattr(result, "content", None)
            if isinstance(content, str) and content.strip():
                return content.strip()
            if isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict):
                        text = part.get("text")
                        if isinstance(text, str):
                            parts.append(text)
                combined = "".join(parts).strip()
                if combined:
                    return combined
        except Exception:
            return None

        return None

    def _llm_summary(self, data: dict[str, Any]) -> str | None:
        groq_summary = self._langchain_groq_summary(data)
        if groq_summary:
            return groq_summary

        llm_config = self._llm_config()
        if not llm_config:
            return None

        api_key, model, base_url = llm_config
        url = f"{base_url}/chat/completions"

        prompt = self._build_summary_prompt(data)

        try:
            response = httpx.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 180
                },
                timeout=15.0,
            )
            response.raise_for_status()
            payload = response.json()
            summary = self._extract_llm_content(payload)
            if summary:
                return summary
        except Exception:
            return None

        return None

    def generate_summary(self, data: dict[str, Any]) -> str:
        llm_summary = self._llm_summary(data)
        if llm_summary:
            return llm_summary

        if ChatGroq is None:
            return "Summary is unavailable because langchain_groq is not installed."

        if not self._llm_config():
            return "Summary is unavailable because no AI API key or model is configured."

        return "Summary is unavailable because the configured AI provider rejected the request (invalid key or endpoint)."


def generate_summary(data: dict[str, Any]) -> str:
    return SummaryService().generate_summary(data)
