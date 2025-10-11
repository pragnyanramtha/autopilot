"""
Data models for the AI Automation Assistant.
Defines core data structures used across components.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class WorkflowStep:
    """Represents a single step in an automation workflow."""
    type: str  # "mouse_move", "click", "type", "wait", "capture"
    coordinates: Optional[tuple[int, int]] = None
    data: Optional[str] = None
    delay_ms: int = 0
    validation: Optional[dict] = None


@dataclass
class Workflow:
    """Represents a complete automation workflow."""
    id: str
    steps: list[WorkflowStep]
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExecutionResult:
    """Represents the result of workflow execution."""
    workflow_id: str
    status: str  # "success", "failed", "interrupted"
    steps_completed: int
    error: Optional[str] = None
    duration_ms: int = 0
