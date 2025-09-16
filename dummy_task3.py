"""
Ioana_DummyTask3 Implementation

This module implements the requirements for DummyTask3 as part of the 
Padawan Integration Hackathon Day 1.

Reference: AB#22812
Related ADO Work Item: Task 22813 IoanaDummyTask_4
"""

def greet_padawan(name="Padawan"):
    """
    Simple greeting function for the hackathon task.
    
    Args:
        name (str): Name to greet, defaults to "Padawan"
        
    Returns:
        str: Greeting message
    """
    return f"Hello, {name}! Welcome to the Integration Hackathon!"


def complete_dummy_task_3():
    """
    Main function that completes DummyTask3 requirements.
    
    Returns:
        dict: Task completion status and details
    """
    task_info = {
        "task_name": "Ioana_DummyTask3",
        "status": "completed",
        "reference": "AB#22812",
        "related_work_item": "Task 22813 IoanaDummyTask_4",
        "message": greet_padawan("Ioana")
    }
    
    print(f"Task: {task_info['task_name']}")
    print(f"Status: {task_info['status']}")
    print(f"Reference: {task_info['reference']}")
    print(f"Message: {task_info['message']}")
    
    return task_info


if __name__ == "__main__":
    # Execute the dummy task
    result = complete_dummy_task_3()
    print("\nDummyTask3 completed successfully!")