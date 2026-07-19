"""Deployment manifest — import the pipelines and notebooks you want to deploy and list them in __all__."""

from agent_logs_pipeline import run_agent_logs
import agent_logs_dashboard

__all__: list[str] = ["run_agent_logs", "agent_logs_dashboard"]
