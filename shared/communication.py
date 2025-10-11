"""
File-based communication layer for AI Automation Assistant.
Provides simple JSON file-based message passing between AI Brain and Automation Engine.
"""
import json
import os
import time
from pathlib import Path
from typing import Optional
from datetime import datetime

from shared.data_models import Workflow, WorkflowStep, ExecutionResult


class CommunicationError(Exception):
    """Raised when communication operations fail."""
    pass


class MessageBroker:
    """
    Handles inter-component communication using JSON files.
    Provides workflow transmission and status reporting.
    """
    
    def __init__(self, base_dir: str = "shared/messages"):
        """
        Initialize the message broker.
        
        Args:
            base_dir: Directory for storing message files
        """
        self.base_dir = Path(base_dir)
        self.workflow_dir = self.base_dir / "workflows"
        self.status_dir = self.base_dir / "status"
        
        # Create directories if they don't exist
        self.workflow_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
    
    def send_workflow(self, workflow: Workflow) -> None:
        """
        Send a workflow to the automation engine.
        Serializes workflow to JSON file.
        
        Args:
            workflow: Workflow object to send
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            workflow_data = self._serialize_workflow(workflow)
            file_path = self.workflow_dir / f"{workflow.id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(workflow_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send workflow: {e}")
    
    def receive_workflow(self, timeout: float = 0) -> Optional[Workflow]:
        """
        Receive a workflow from the AI brain.
        Polls for workflow files and deserializes the oldest one.
        
        Args:
            timeout: How long to wait for a workflow (0 = no wait)
            
        Returns:
            Workflow object if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        
        while True:
            try:
                # Get all workflow files sorted by creation time
                workflow_files = sorted(
                    self.workflow_dir.glob("*.json"),
                    key=lambda p: p.stat().st_ctime
                )
                
                if workflow_files:
                    file_path = workflow_files[0]
                    
                    with open(file_path, 'r') as f:
                        workflow_data = json.load(f)
                    
                    workflow = self._deserialize_workflow(workflow_data)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return workflow
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive workflow: {e}")
    
    def send_status(self, result: ExecutionResult) -> None:
        """
        Send execution status from automation engine back to AI brain.
        
        Args:
            result: ExecutionResult object to send
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            status_data = self._serialize_status(result)
            file_path = self.status_dir / f"{result.workflow_id}_status.json"
            
            with open(file_path, 'w') as f:
                json.dump(status_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send status: {e}")
    
    def receive_status(self, workflow_id: str, timeout: float = 0) -> Optional[ExecutionResult]:
        """
        Receive execution status for a specific workflow.
        
        Args:
            workflow_id: ID of the workflow to check status for
            timeout: How long to wait for status (0 = no wait)
            
        Returns:
            ExecutionResult object if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        file_path = self.status_dir / f"{workflow_id}_status.json"
        
        while True:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        status_data = json.load(f)
                    
                    result = self._deserialize_status(status_data)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return result
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive status: {e}")
    
    def clear_messages(self) -> None:
        """
        Clear all pending messages (workflows and status).
        Useful for cleanup or reset operations.
        """
        for file_path in self.workflow_dir.glob("*.json"):
            file_path.unlink()
        
        for file_path in self.status_dir.glob("*.json"):
            file_path.unlink()
    
    def _serialize_workflow(self, workflow: Workflow) -> dict:
        """
        Serialize a Workflow object to a dictionary.
        
        Args:
            workflow: Workflow object to serialize
            
        Returns:
            Dictionary representation of the workflow
        """
        return {
            "type": "workflow",
            "id": workflow.id,
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "steps": [
                    {
                        "type": step.type,
                        "coordinates": step.coordinates,
                        "data": step.data,
                        "delay_ms": step.delay_ms,
                        "validation": step.validation
                    }
                    for step in workflow.steps
                ],
                "metadata": workflow.metadata,
                "created_at": workflow.created_at.isoformat()
            }
        }
    
    def _deserialize_workflow(self, data: dict) -> Workflow:
        """
        Deserialize a dictionary to a Workflow object.
        
        Args:
            data: Dictionary containing workflow data
            
        Returns:
            Workflow object
            
        Raises:
            CommunicationError: If data structure is invalid
        """
        try:
            payload = data["payload"]
            
            steps = [
                WorkflowStep(
                    type=step["type"],
                    coordinates=tuple(step["coordinates"]) if step["coordinates"] else None,
                    data=step["data"],
                    delay_ms=step["delay_ms"],
                    validation=step["validation"]
                )
                for step in payload["steps"]
            ]
            
            return Workflow(
                id=data["id"],
                steps=steps,
                metadata=payload["metadata"],
                created_at=datetime.fromisoformat(payload["created_at"])
            )
        except (KeyError, ValueError) as e:
            raise CommunicationError(f"Invalid workflow data structure: {e}")
    
    def _serialize_status(self, result: ExecutionResult) -> dict:
        """
        Serialize an ExecutionResult object to a dictionary.
        
        Args:
            result: ExecutionResult object to serialize
            
        Returns:
            Dictionary representation of the execution result
        """
        return {
            "type": "status",
            "workflow_id": result.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "payload": {
                "status": result.status,
                "steps_completed": result.steps_completed,
                "error": result.error,
                "duration_ms": result.duration_ms
            }
        }
    
    def _deserialize_status(self, data: dict) -> ExecutionResult:
        """
        Deserialize a dictionary to an ExecutionResult object.
        
        Args:
            data: Dictionary containing status data
            
        Returns:
            ExecutionResult object
            
        Raises:
            CommunicationError: If data structure is invalid
        """
        try:
            payload = data["payload"]
            
            return ExecutionResult(
                workflow_id=data["workflow_id"],
                status=payload["status"],
                steps_completed=payload["steps_completed"],
                error=payload["error"],
                duration_ms=payload["duration_ms"]
            )
        except (KeyError, ValueError) as e:
            raise CommunicationError(f"Invalid status data structure: {e}")
