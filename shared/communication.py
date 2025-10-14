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
        self.visual_nav_dir = self.base_dir / "visual_navigation"
        
        # Create directories if they don't exist
        self.workflow_dir.mkdir(parents=True, exist_ok=True)
        self.protocol_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)
        self.visual_nav_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    def send_visual_navigation_request(self, request: dict) -> None:
        """
        Send a visual navigation request to the automation engine.
        
        Message structure:
        {
            "type": "visual_navigation_request",
            "request_id": "unique_id",
            "task_description": "Click the submit button",
            "workflow_goal": "Submit the form",
            "iteration": 1,
            "max_iterations": 10,
            "timestamp": "ISO timestamp"
        }
        
        Args:
            request: Visual navigation request dictionary
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            request_data = {
                "type": "visual_navigation_request",
                "timestamp": datetime.now().isoformat(),
                **request
            }
            
            request_id = request.get('request_id', 'unknown')
            file_path = self.visual_nav_dir / f"request_{request_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(request_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send visual navigation request: {e}")
    
    def receive_visual_navigation_request(self, timeout: float = 0) -> Optional[dict]:
        """
        Receive a visual navigation request from the AI brain.
        
        Args:
            timeout: How long to wait for a request (0 = no wait)
            
        Returns:
            Visual navigation request dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        
        while True:
            try:
                # Get all request files sorted by creation time
                request_files = sorted(
                    self.visual_nav_dir.glob("request_*.json"),
                    key=lambda p: p.stat().st_ctime
                )
                
                if request_files:
                    file_path = request_files[0]
                    
                    with open(file_path, 'r') as f:
                        request = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return request
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive visual navigation request: {e}")
    
    def send_visual_navigation_response(self, response: dict) -> None:
        """
        Send a visual navigation response with screenshot to the AI brain.
        
        Message structure:
        {
            "type": "visual_navigation_response",
            "request_id": "unique_id",
            "screenshot_base64": "base64_encoded_image",
            "mouse_position": {"x": 100, "y": 200},
            "screen_size": {"width": 1920, "height": 1080},
            "timestamp": "ISO timestamp"
        }
        
        Args:
            response: Visual navigation response dictionary with base64 screenshot
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            response_data = {
                "type": "visual_navigation_response",
                "timestamp": datetime.now().isoformat(),
                **response
            }
            
            request_id = response.get('request_id', 'unknown')
            file_path = self.visual_nav_dir / f"response_{request_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(response_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send visual navigation response: {e}")
    
    def receive_visual_navigation_response(self, request_id: str, timeout: float = 5.0) -> Optional[dict]:
        """
        Receive a visual navigation response for a specific request.
        
        Args:
            request_id: ID of the request to get response for
            timeout: How long to wait for response (default: 5.0 seconds)
            
        Returns:
            Visual navigation response dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        file_path = self.visual_nav_dir / f"response_{request_id}.json"
        
        while True:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        response = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return response
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive visual navigation response: {e}")
    
    def send_visual_action_command(self, command: dict) -> None:
        """
        Send a visual action command to the automation engine.
        
        Message structure:
        {
            "type": "visual_action_command",
            "request_id": "unique_id",
            "action": "click",  # or 'double_click', 'right_click', 'type'
            "coordinates": {"x": 500, "y": 300},
            "text": null,  # For 'type' actions
            "request_followup": true,  # Whether to send new screenshot after
            "timestamp": "ISO timestamp"
        }
        
        Args:
            command: Visual action command dictionary
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            command_data = {
                "type": "visual_action_command",
                "timestamp": datetime.now().isoformat(),
                **command
            }
            
            request_id = command.get('request_id', 'unknown')
            file_path = self.visual_nav_dir / f"command_{request_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(command_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send visual action command: {e}")
    
    def receive_visual_action_command(self, timeout: float = 0) -> Optional[dict]:
        """
        Receive a visual action command from the AI brain.
        
        Args:
            timeout: How long to wait for a command (0 = no wait)
            
        Returns:
            Visual action command dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        
        while True:
            try:
                # Get all command files sorted by creation time
                command_files = sorted(
                    self.visual_nav_dir.glob("command_*.json"),
                    key=lambda p: p.stat().st_ctime
                )
                
                if command_files:
                    file_path = command_files[0]
                    
                    with open(file_path, 'r') as f:
                        command = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return command
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive visual action command: {e}")
    
    def send_visual_action_result(self, result: dict) -> None:
        """
        Send a visual action result back to the AI brain.
        
        Message structure:
        {
            "type": "visual_action_result",
            "request_id": "unique_id",
            "status": "success",  # or 'error'
            "error": null,
            "screenshot_base64": "...",  # If request_followup was true
            "mouse_position": {"x": 500, "y": 300},
            "timestamp": "ISO timestamp"
        }
        
        Args:
            result: Visual action result dictionary
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            result_data = {
                "type": "visual_action_result",
                "timestamp": datetime.now().isoformat(),
                **result
            }
            
            request_id = result.get('request_id', 'unknown')
            file_path = self.visual_nav_dir / f"result_{request_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(result_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send visual action result: {e}")
    
    def receive_visual_action_result(self, request_id: str, timeout: float = 5.0) -> Optional[dict]:
        """
        Receive a visual action result for a specific request.
        
        Args:
            request_id: ID of the request to get result for
            timeout: How long to wait for result (default: 5.0 seconds)
            
        Returns:
            Visual action result dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        file_path = self.visual_nav_dir / f"result_{request_id}.json"
        
        while True:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        result = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return result
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive visual action result: {e}")
    
    def send_visual_navigation_result(self, result: dict) -> None:
        """
        Send the final visual navigation workflow result to the protocol executor.
        
        This is sent by the AI Brain when the visual navigation workflow completes
        (either successfully, with failure, or timeout).
        
        Message structure:
        {
            "type": "visual_navigation_result",
            "request_id": "unique_id",
            "status": "success",  # or 'failed', 'timeout', 'stopped'
            "actions_taken": [...],
            "final_coordinates": {"x": 500, "y": 300},
            "error": null,
            "timestamp": "ISO timestamp"
        }
        
        Args:
            result: Visual navigation workflow result dictionary
            
        Raises:
            CommunicationError: If serialization or file write fails
        """
        try:
            result_data = {
                "type": "visual_navigation_result",
                "timestamp": datetime.now().isoformat(),
                **result
            }
            
            request_id = result.get('request_id', 'unknown')
            file_path = self.visual_nav_dir / f"workflow_result_{request_id}.json"
            
            with open(file_path, 'w') as f:
                json.dump(result_data, f, indent=2)
                
        except Exception as e:
            raise CommunicationError(f"Failed to send visual navigation result: {e}")
    
    def receive_visual_navigation_result(self, request_id: str, timeout: float = 60.0) -> Optional[dict]:
        """
        Receive the final visual navigation workflow result for a specific request.
        
        This is used by the protocol executor to wait for the AI Brain to complete
        the visual navigation workflow.
        
        Args:
            request_id: ID of the request to get result for
            timeout: How long to wait for result (default: 60.0 seconds)
            
        Returns:
            Visual navigation workflow result dictionary if found, None otherwise
            
        Raises:
            CommunicationError: If deserialization fails
        """
        start_time = time.time()
        file_path = self.visual_nav_dir / f"workflow_result_{request_id}.json"
        
        while True:
            try:
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        result = json.load(f)
                    
                    # Delete the file after reading
                    file_path.unlink()
                    
                    return result
                
                # Check timeout
                if timeout == 0 or (time.time() - start_time) >= timeout:
                    return None
                
                # Wait a bit before checking again
                time.sleep(0.1)
                
            except Exception as e:
                raise CommunicationError(f"Failed to receive visual navigation result: {e}")
    
    def clear_messages(self) -> None:
        """
        Clear all pending messages (workflows, protocols, status, and visual navigation).
        Useful for cleanup or reset operations.
        """
        for file_path in self.workflow_dir.glob("*.json"):
            file_path.unlink()
        
        for file_path in self.protocol_dir.glob("*.json"):
            file_path.unlink()
        
        for file_path in self.status_dir.glob("*.json"):
            file_path.unlink()
        
        for file_path in self.visual_nav_dir.glob("*.json"):
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
