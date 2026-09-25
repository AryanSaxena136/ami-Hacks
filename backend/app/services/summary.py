from __future__ import annotations

import os
from typing import Any

import httpx


class SummaryService:
    def _rule_based_summary(self, data: dict[str, Any]) -> str:
        zone = data.get("zone") or "the monitored zone"
        rainfall = float(data.get("rainfall", 0) or 0)
        traffic = float(data.get("traffic", 0) or 0)
        incident_reports = float(data.get("incident_reports", 0) or 0)

        if rainfall >= 30 and traffic >= 70 and incident_reports >= 10:
            return (
                f"Heavy rainfall is currently coinciding with high traffic congestion and increased "
                f"waterlogging reports in {zone}. Residents may experience localized travel disruption."
            )
        if rainfall >= 30:
            return f"Heavy rainfall is affecting {zone}. Conditions are wetter than usual and mobility may be reduced."
        if traffic >= 70:
            return f"Traffic congestion is elevated in {zone}. Travel delays may be noticeable during peak demand."
        if incident_reports >= 8:
            return f"Incident reports are elevated in {zone}. City services may need closer monitoring in this area."
        return f"Conditions in {zone} are currently stable with no major civic disruption detected."

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

    def _llm_summary(self, data: dict[str, Any]) -> str | None:
        llm_config = self._llm_config()
        if not llm_config:
            return None

        api_key, model, base_url = llm_config
        url = f"{base_url}/chat/completions"

        zone = data.get("zone") or "the monitored zone"
        rainfall = float(data.get("rainfall", 0) or 0)
        traffic = float(data.get("traffic", 0) or 0)
        incident_reports = float(data.get("incident_reports", 0) or 0)

        prompt = (
            f"You are a civic operations analyst. Summarize the current situation for {zone} using the following "
            f"processed signals: rainfall={rainfall}, traffic_congestion={traffic}, incident_reports={incident_reports}. "
            "Keep it concise, actionable, and suitable for a city operations dashboard."
        )

        try:
            response = httpx.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 180,
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
        return self._rule_based_summary(data)


def generate_summary(data: dict[str, Any]) -> str:
    return SummaryService().generate_summary(data)
