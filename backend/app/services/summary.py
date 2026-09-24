from __future__ import annotations

from typing import Any


class SummaryService:
    def generate_summary(self, data: dict[str, Any]) -> str:
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


def generate_summary(data: dict[str, Any]) -> str:
    return SummaryService().generate_summary(data)
