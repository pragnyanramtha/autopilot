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
        self.protocol_dir = self.base_dir / "protocols"
        self.status_dir = self.base_dir / "status"
        
        # Create directories if they don't exist
        self.workflow_dir.mkdir(parents=True, exist_ok=True)
        self.protocol_dir.mkdir(parents=True, exist_ok=True)
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
    
    def send_protocol(self, protocol: dict) -> None:
        """
        Send a protocol to the automation engine.
        Serializes protocol to JSON file.
        
        Args:
            protocol: Protocol dictionary to send
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            # Generate ID if not present
            if 'metadata' not in protocol:
                protocol['metadata'] = {}
            if 'id' not in protocol['metadata']:
                import uuid
                protocol['metadata']['id'] = str(uuid.uuid4())
            
            protocol_id = protocol['metadata']['id']
            file_path = self.protocol_dir / f"{protocol_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(protocol, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send protocol: {e}")
    
    def receive_protocol(self, timeout: float = 0) -> Optional[dict]:
        """
        Receive a protocol from the AI brain.
        Polls for protocol files and deserializes the oldest one.
        
        Args:
            timeout: How long to wait for a protocol (0 = no wait)
            
        Returns:
            Protocol dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        
        while True:
            try:
                # Get all protocol files sorted by creation time
                protocol_files = sorted(
                    self.protocol_dir.glob("*.json"),
                    key=lambda p: p.stat().st_ctime
                )
                
                if protocol_files:
                    file_path = protocol_files[0]
                    
                    with open(file_path, 'r') as f:
                        protocol = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return protocol
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive protocol: {e}")
    
    def send_protocol_status(self, result) -> None:
        """
        Send protocol execution status from automation engine back to AI brain.
        
        Args:
            result: ExecutionResult object from ProtocolExecutor
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            # Convert ExecutionResult to dictionary
            status_data = {
                "type": "protocol_status",
                "protocol_id": result.protocol_id,
                "timestamp": datetime.now().isoformat(),
                "payload": result.to_dict()
            }
            
            # Use protocol_id as filename (sanitize it first)
            import re
            safe_id = re.sub(r'[^\w\-_]', '_', result.protocol_id)
            file_path = self.status_dir / f"{safe_id}_status.json"
            
            with open(file_path, 'w') as f:
                json.dump(status_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send protocol status: {e}")
    
    def receive_protocol_status(self, protocol_id: str, timeout: float = 0):
        """
        Receive execution status for a specific protocol.
        
        Args:
            protocol_id: ID of the protocol to check status for
            timeout: How long to wait for status (0 = no wait)
            
        Returns:
            ExecutionResult dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        
        # Sanitize protocol_id for filename
        import re
        safe_id = re.sub(r'[^\w\-_]', '_', protocol_id)
        file_path = self.status_dir / f"{safe_id}_status.json"
        
        while True:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        status_data = json.load(f)
                    
                    result = status_data.get('payload')
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return result
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive protocol status: {e}")
    
    def clear_messages(self) -> None:
        """
        Clear all pending messages (workflows, protocols, and status).
        Useful for cleanup or reset operations.
        """
        for file_path in self.workflow_dir.glob("*.json"):
            file_path.unlink()
        
        for file_path in self.protocol_dir.glob("*.json"):
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
