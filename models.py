"""
Models for Project Management System
User -> Projects -> Tasks relationship
"""
import json
import os
from datetime import datetime
from typing import List, Dict
import uuid


class User:
    """User class representing a system user"""
    
    def __init__(self, username: str, role: str = "developer"):
        self.user_id = str(uuid.uuid4())[:8]
        self.username = username
        self.role = role  # admin, manager, developer, viewer
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON storage"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create user from dictionary"""
        user = cls(data["username"], data["role"])
        user.user_id = data["user_id"]
        user.created_at = data["created_at"]
        return user
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class Task:
    """Task class representing individual tasks within a project"""
    
    STATUSES = ["pending", "in_progress", "completed"]
    PRIORITIES = ["low", "medium", "high"]
    
    def __init__(self, title: str, description: str = "", assigned_to: str = None):
        self.task_id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.status = "pending"
        self.priority = "medium"
        self.assigned_to = assigned_to
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def complete(self):
        """Mark task as completed"""
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
        return True
    
    def update_status(self, status: str) -> bool:
        """Update task status"""
        if status in self.STATUSES:
            self.status = status
            if status == "completed":
                self.completed_at = datetime.now().isoformat()
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON storage"""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create task from dictionary"""
        task = cls(data["title"], data["description"], data.get("assigned_to"))
        task.task_id = data["task_id"]
        task.status = data["status"]
        task.priority = data.get("priority", "medium")
        task.created_at = data["created_at"]
        task.completed_at = data.get("completed_at")
        return task
    
    def __str__(self):
        return f"[{self.status.upper()}] {self.title}"


class Project:
    """Project class containing multiple tasks"""
    
    def __init__(self, name: str, description: str = "", owner_id: str = None):
        self.project_id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.tasks: List[Task] = []
        self.created_at = datetime.now().isoformat()
    
    def add_task(self, task: Task):
        """Add a task to the project"""
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[i]
                return True
        return False
    
    def get_task(self, task_id: str) -> Task:
        """Get a task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_task_summary(self) -> Dict:
        """Get summary of task statuses"""
        summary = {"pending": 0, "in_progress": 0, "completed": 0}
        for task in self.tasks:
            summary[task.status] += 1
        return summary
    
    def to_dict(self) -> Dict:
        """Convert project to dictionary for JSON storage"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "tasks": [task.to_dict() for task in self.tasks],
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create project from dictionary"""
        project = cls(data["name"], data["description"], data.get("owner_id"))
        project.project_id = data["project_id"]
        project.created_at = data["created_at"]
        project.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return project
    
    def __str__(self):
        return f"{self.name} ({len(self.tasks)} tasks)"


class ProjectTracker:
    """Main tracker class managing users and projects"""
    
    def __init__(self, data_file: str = None):
        self.users: List[User] = []
        self.projects: List[Project] = []
        self.current_user: User = None
        if data_file:
            self.data_file = data_file
        else:
            self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tracker_data.json")
        self.load_data()
    
    def add_user(self, username: str, role: str = "developer") -> User:
        """Add a new user"""
        # Check if user already exists
        for user in self.users:
            if user.username == username:
                return None
        
        user = User(username, role)
        self.users.append(user)
        self.save_data()
        return user
    
    def get_user(self, username: str) -> User:
        """Get user by username"""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def login(self, username: str) -> bool:
        """Login a user"""
        user = self.get_user(username)
        if user:
            self.current_user = user
            return True
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def add_project(self, name: str, description: str = "") -> Project:
        """Add a new project"""
        if not self.current_user:
            return None
        
        project = Project(name, description, self.current_user.user_id)
        self.projects.append(project)
        self.save_data()
        return project
    
    def get_project(self, project_id: str) -> Project:
        """Get project by ID"""
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        for i, project in enumerate(self.projects):
            if project.project_id == project_id:
                del self.projects[i]
                self.save_data()
                return True
        return False
    
    def add_task_to_project(self, project_id: str, title: str, description: str = "") -> Task:
        """Add a task to a project"""
        project = self.get_project(project_id)
        if project:
            task = Task(title, description)
            project.add_task(task)
            self.save_data()
            return task
        return None
    
    def get_user_projects(self) -> List[Project]:
        """Get projects owned by current user"""
        if not self.current_user:
            return []
        return [p for p in self.projects if p.owner_id == self.current_user.user_id]
    
    def save_data(self):
        """Save all data to JSON file"""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                "users": [user.to_dict() for user in self.users],
                "projects": [project.to_dict() for project in self.projects]
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load all data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                self.users = [User.from_dict(user_data) for user_data in data.get("users", [])]
                self.projects = [Project.from_dict(proj_data) for proj_data in data.get("projects", [])]
        except Exception as e:
            print(f"Error loading data: {e}")