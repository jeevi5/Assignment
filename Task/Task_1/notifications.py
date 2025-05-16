"""
    This module defines the classes which are responsible for handling notifications
"""

import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TaskNotification:
    """
        This utility class is implemented for handling task-related notifications.
        This class currently simulates sending notifications after any updates in the task.
    """
    @staticmethod
    def send_update_notification(task_id: int):
        """
            Function to simulate sending notifications.
            Args:
                task_id: The ID of the task that is updated.
        """
        try:
            time.sleep(2)  # Simulate delay
            logger.info(f"Notification sent for task {task_id}")
        except Exception as e:
            logger.error(f"Failed to send notification for task {task_id}: {e}")

