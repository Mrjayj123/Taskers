"""
Unit tests for Project Management System
"""
import unittest
import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import User, Task, Project, ProjectTracker


class TestUser(unittest.TestCase):
    """Test User class"""
    
    def test_user_creation(self):
        user = User("testuser", "developer")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "developer")
        self.assertIsNotNone(user.user_id)
    
    def test_user_to_dict(self):
        user = User("testuser", "admin")
        user_dict = user.to_dict()
        self.assertEqual(user_dict["username"], "testuser")
        self.assertEqual(user_dict["role"], "admin")
    
    def test_user_from_dict(self):
        data = {"user_id": "123", "username": "test", "role": "manager", "created_at": "2024-01-01"}
        user = User.from_dict(data)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.role, "manager")


class TestTask(unittest.TestCase):
    """Test Task class"""
    
    def test_task_creation(self):
        task = Task("Test Task", "Description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "pending")
    
    def test_task_complete(self):
        task = Task("Test Task")
        task.complete()
        self.assertEqual(task.status, "completed")
        self.assertIsNotNone(task.completed_at)
    
    def test_update_status(self):
        task = Task("Test Task")
        res = task.update_status("in_progress")
        self.assertTrue(res)
        self.assertEqual(task.status, "in_progress")
    
    def test_invalid_status(self):
        task = Task("Test Task")
        res = task.update_status("invalid")
        self.assertFalse(res)
        self.assertEqual(task.status, "pending")


class TestProject(unittest.TestCase):
    """Test Project class"""
    
    def test_project_creation(self):
        project = Project("Test Project", "Description")
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(len(project.tasks), 0)
    
    def test_add_task(self):
        project = Project("Test Project")
        task = Task("Task 1")
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)
    
    def test_remove_task(self):
        project = Project("Test Project")
        task = Task("Task 1")
        project.add_task(task)
        result = project.remove_task(task.task_id)
        self.assertTrue(result)
        self.assertEqual(len(project.tasks), 0)
    
    def test_get_task_summary(self):
        project = Project("Test Project")
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        task2.update_status("in_progress")
        task3 = Task("Task 3")
        task3.complete()
        
        project.add_task(task1)
        project.add_task(task2)
        project.add_task(task3)
        
        summary = project.get_task_summary()
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["in_progress"], 1)
        self.assertEqual(summary["completed"], 1)


class TestProjectTracker(unittest.TestCase):
    """Test ProjectTracker class"""
    
    def setUp(self):
        """Setup test environment"""
        # Use temporary file for testing
        temp_file = tempfile.mktemp(suffix=".json")
        self.tracker = ProjectTracker(data_file=temp_file)
    
    def tearDown(self):
        """Cleanup test environment"""
        if os.path.exists(self.tracker.data_file):
            os.remove(self.tracker.data_file)
    
    def test_add_user(self):
        user = self.tracker.add_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(len(self.tracker.users), 1)
    
    def test_add_duplicate_user(self):
        self.tracker.add_user("testuser")
        user2 = self.tracker.add_user("testuser")
        self.assertIsNone(user2)
    
    def test_login(self):
        self.tracker.add_user("testuser")
        result = self.tracker.login("testuser")
        self.assertTrue(result)
        self.assertIsNotNone(self.tracker.current_user)
    
    def test_login_nonexistent(self):
        result = self.tracker.login("nonexistent")
        self.assertFalse(result)
    
    def test_add_project(self):
        self.tracker.add_user("testuser")
        self.tracker.login("testuser")
        project = self.tracker.add_project("Test Project")
        self.assertIsNotNone(project)
        self.assertEqual(len(self.tracker.projects), 1)
    
    def test_add_task_to_project(self):
        self.tracker.add_user("testuser")
        self.tracker.login("testuser")
        project = self.tracker.add_project("Test Project")
        task = self.tracker.add_task_to_project(project.project_id, "Test Task")
        self.assertIsNotNone(task)
        self.assertEqual(len(project.tasks), 1)
    
    def test_save_and_load(self):
        # Add data
        self.tracker.add_user("testuser")
        self.tracker.login("testuser")
        self.tracker.add_project("Test Project")
        self.tracker.save_data()
        
        # Create new tracker and load
        new_tracker = ProjectTracker()
        new_tracker.data_file = self.tracker.data_file
        new_tracker.load_data()
        
        self.assertEqual(len(new_tracker.users), 1)
        self.assertEqual(len(new_tracker.projects), 1)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False)


if __name__ == "__main__":
    run_tests()