"""
Service Targets Management Module

This module handles all service target operations including creation and management.
"""

import logging
from typing import Dict, Any, Optional, List
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class ServiceTargetsManager(BaseThalesCDSPCSMTool):
    """Manages service targets operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def create_ssh_target(self, name: str, host: str, port: str, username: str,
                               password: Optional[str] = None, private_key: Optional[str] = None,
                               description: Optional[str] = None, tags: Optional[List[str]] = None,
                               delete_protection: Optional[str] = None, json: bool = False,
                               uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create an SSH target."""
        try:
            # Validate required parameters
            if not host:
                return {
                    "success": False,
                    "error": "Host is required for SSH targets",
                    "message": "Please specify the SSH host"
                }
            
            if not port:
                return {
                    "success": False,
                    "error": "Port is required for SSH targets",
                    "message": "Please specify the SSH port"
                }
            
            if not username:
                return {
                    "success": False,
                    "error": "Username is required for SSH targets",
                    "message": "Please specify the SSH username"
                }
            
            if not password and not private_key:
                return {
                    "success": False,
                    "error": "Either password or private key is required for SSH targets",
                    "message": "Please specify either SSH password or private key"
                }
            
            # TODO: Implement when SSH target creation is available
            # result = await self.client.create_ssh_target(request_data)
            
            return {
                "success": False,
                "error": "SSH target creation not yet implemented",
                "message": "SSH target creation is planned for future release"
            }
        except Exception as e:
            logger.error(f"Failed to create SSH target '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create SSH target '{name}'"
            }
    
    async def create_rabbitmq_target(self, name: str, host: str, port: str, username: str,
                                    password: str, vhost: str = "/", description: Optional[str] = None,
                                    tags: Optional[List[str]] = None, delete_protection: Optional[str] = None,
                                    json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create a RabbitMQ target."""
        try:
            # Validate required parameters
            if not host:
                return {
                    "success": False,
                    "error": "Host is required for RabbitMQ targets",
                    "message": "Please specify the RabbitMQ host"
                }
            
            if not port:
                return {
                    "success": False,
                    "error": "Port is required for RabbitMQ targets",
                    "message": "Please specify the RabbitMQ port"
                }
            
            if not username:
                return {
                    "success": False,
                    "error": "Username is required for RabbitMQ targets",
                    "message": "Please specify the RabbitMQ username"
                }
            
            if not password:
                return {
                    "success": False,
                    "error": "Password is required for RabbitMQ targets",
                    "message": "Please specify the RabbitMQ password"
                }
            
            # TODO: Implement when RabbitMQ target creation is available
            # result = await self.client.create_rabbitmq_target(request_data)
            
            return {
                "success": False,
                "error": "RabbitMQ target creation not yet implemented",
                "message": "RabbitMQ target creation is planned for future release"
            }
        except Exception as e:
            logger.error(f"Failed to create RabbitMQ target '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create RabbitMQ target '{name}'"
            }
    
    def get_supported_service_types(self) -> List[str]:
        """Get list of supported service types."""
        return ['ssh', 'rabbitmq', 'artifactory', 'dockerhub', 'github', 'chef', 'web', 'salesforce']
    
    def validate_service_type(self, service_type: str) -> bool:
        """Validate if the service type is supported."""
        return service_type.lower() in self.get_supported_service_types() 