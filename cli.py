
#CLI interface for Project Management System
import sys
try:
    from tabulate import tabulate
except ImportError:
    def tabulate(table_data, headers, tablefmt=None):
        # A simple fallback table formatter
        cols_count = len(headers)
        col_widths = [len(h) for h in headers]
        for row in table_data:
            for i in range(min(cols_count, len(row))):
                col_widths[i] = max(col_widths[i], len(str(row[i])))
        
        # Build horizontal separator
        sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
        
        lines = [sep]
        # Header row
        header_row = "|" + "|".join([f" {headers[i].ljust(col_widths[i])} " for i in range(cols_count)]) + "|"
        lines.append(header_row)
        lines.append(sep)
        
        # Data rows
        for row in table_data:
            data_row = "|" + "|".join([f" {str(row[i]).ljust(col_widths[i])} " for i in range(min(cols_count, len(row)))]) + "|"
            lines.append(data_row)
        lines.append(sep)
        return "\n".join(lines)

from models import ProjectTracker


class ProjectCLI:
    """Command-line interface for project management"""
    
    def __init__(self):
        self.tracker = ProjectTracker()
    
    def run(self):
        """Main CLI loop"""
        self.print_welcome()
        
        while True:
            if not self.tracker.current_user:
                self.show_login_menu()
            else:
                self.show_main_menu()
    
    def print_welcome(self):
        """Print welcome message"""
        print("\n" + "="*50)
        print("   PROJECT MANAGEMENT SYSTEM CLI")
        print("="*50)
    
    def show_login_menu(self):
        """Show login/registration menu"""
        print("\n--- LOGIN MENU ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option!")
    
    def login(self):
        """Handle user login"""
        username = input("Username: ").strip()
        
        if self.tracker.login(username):
            print(f"\n✓ Welcome back, {username}!")
        else:
            print(f"\n✗ User '{username}' not found. Please register first.")
    
    def register(self):
        """Handle user registration"""
        username = input("Username: ").strip()
        
        if self.tracker.get_user(username):
            print(f"\n✗ User '{username}' already exists!")
            return
        
        print("Roles: admin, manager, developer, viewer")
        role = input("Role (default: developer): ").strip().lower()
        
        if not role:
            role = "developer"
        
        user = self.tracker.add_user(username, role)
        if user:
            print(f"\n✓ User '{username}' registered successfully!")
            self.tracker.login(username)
        else:
            print("\n✗ Registration failed!")
    
    def show_main_menu(self):
        """Show main menu for logged-in user"""
        print(f"\n--- MAIN MENU [{self.tracker.current_user.username}] ---")
        print("1. View All Projects")
        print("2. Create Project")
        print("3. View My Projects")
        print("4. Manage Project Tasks")
        print("5. View All Users")
        print("6. Logout")
        
        choice = input("\nChoose option: ").strip()
        
        if choice == "1":
            self.view_all_projects()
        elif choice == "2":
            self.create_project()
        elif choice == "3":
            self.view_my_projects()
        elif choice == "4":
            self.manage_tasks()
        elif choice == "5":
            self.view_all_users()
        elif choice == "6":
            self.tracker.logout()
            print("\n✓ Logged out successfully!")
        else:
            print("\n✗ Invalid option!")
    
    def view_all_projects(self):
        """Display all projects"""
        if not self.tracker.projects:
            print("\n📁 No projects available.")
            return
        
        table_data = []
        for project in self.tracker.projects:
            owner = self.tracker.get_user_by_id(project.owner_id)
            owner_name = owner.username if owner else "Unknown"
            summary = project.get_task_summary()
            table_data.append([
                project.project_id,
                project.name,
                owner_name,
                summary['completed'],
                summary['in_progress'],
                summary['pending']
            ])
        
        headers = ["ID", "Project Name", "Owner", "Done", "Progress", "Pending"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def view_my_projects(self):
        """Display projects owned by current user"""
        my_projects = self.tracker.get_user_projects()
        
        if not my_projects:
            print("\n📁 You don't own any projects yet.")
            return
        
        table_data = []
        for project in my_projects:
            summary = project.get_task_summary()
            table_data.append([
                project.project_id,
                project.name,
                project.description[:30] + "..." if len(project.description) > 30 else project.description,
                summary['completed'],
                summary['in_progress'],
                summary['pending']
            ])
        
        headers = ["ID", "Project", "Description", "Done", "Progress", "Pending"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def create_project(self):
        """Create a new project"""
        print("\n--- Create New Project ---")
        name = input("Project name: ").strip()
        
        if not name:
            print("✗ Project name required!")
            return
        
        description = input("Description (optional): ").strip()
        
        project = self.tracker.add_project(name, description)
        if project:
            print(f"\n✓ Project '{name}' created successfully!")
            print(f"  Project ID: {project.project_id}")
        else:
            print("\n✗ Failed to create project!")
    
    def manage_tasks(self):
        """Manage tasks in a project"""
        project_id = input("\nEnter Project ID: ").strip()
        project = self.tracker.get_project(project_id)
        
        if not project:
            print(f"\n✗ Project '{project_id}' not found!")
            return
        
        # Check ownership
        if project.owner_id != self.tracker.current_user.user_id:
            print("\n✗ You can only manage tasks in your own projects!")
            return
        
        while True:
            self.show_task_menu(project)
            
            choice = input("\nTask option (or 'back' to exit): ").strip()
            
            if choice == "1":
                self.add_task(project)
            elif choice == "2":
                self.view_tasks(project)
            elif choice == "3":
                self.update_task_status(project)
            elif choice == "4":
                self.delete_task(project)
            elif choice.lower() == "back":
                break
            else:
                print("✗ Invalid option!")
    
    def show_task_menu(self, project):
        """Show task management menu"""
        print(f"\n--- Tasks for: {project.name} ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task Status")
        print("4. Delete Task")
        print("Type 'back' to return")
    
    def add_task(self, project):
        """Add a task to project"""
        title = input("Task title: ").strip()
        
        if not title:
            print("✗ Title required!")
            return
        
        description = input("Description (optional): ").strip()
        
        task = self.tracker.add_task_to_project(project.project_id, title, description)
        if task:
            print(f"\n✓ Task '{title}' added! (ID: {task.task_id})")
        else:
            print("\n✗ Failed to add task!")
    
    def view_tasks(self, project):
        """View all tasks in a project"""
        if not project.tasks:
            print("\n📋 No tasks in this project.")
            return
        
        table_data = []
        for task in project.tasks:
            table_data.append([
                task.task_id,
                task.title,
                task.status,
                task.priority,
                task.description[:30] + "..." if len(task.description) > 30 else task.description
            ])
        
        headers = ["ID", "Title", "Status", "Priority", "Description"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def update_task_status(self, project):
        """Update a task's status"""
        task_id = input("Task ID: ").strip()
        task = project.get_task(task_id)
        
        if not task:
            print(f"\n✗ Task '{task_id}' not found!")
            return
        
        print(f"\nCurrent status: {task.status}")
        print("Available statuses: pending, in_progress, completed")
        new_status = input("New status: ").strip().lower()
        
        if task.update_status(new_status):
            self.tracker.save_data()
            print(f"\n✓ Task status updated to '{new_status}'!")
        else:
            print(f"\n✗ Invalid status '{new_status}'! Status must be one of: pending, in_progress, completed")
    
    def delete_task(self, project):
        """Delete a task"""
        task_id = input("Task ID: ").strip()
        
        if project.remove_task(task_id):
            self.tracker.save_data()
            print(f"\n✓ Task '{task_id}' deleted!")
        else:
            print(f"\n✗ Task '{task_id}' not found!")
    
    def view_all_users(self):
        """View all registered users"""
        if not self.tracker.users:
            print("\n👥 No users registered.")
            return
        
        table_data = []
        for user in self.tracker.users:
            project_count = len([p for p in self.tracker.projects if p.owner_id == user.user_id])
            table_data.append([
                user.username,
                user.role,
                project_count,
                user.created_at[:10]
            ])
        
        headers = ["Username", "Role", "Projects", "Joined"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    def get_user_by_id(self, user_id):
        """Helper to get user by ID"""
        for user in self.tracker.users:
            if user.user_id == user_id:
                return user
        return None


# Add helper method to ProjectTracker
def get_user_by_id(self, user_id):
    """Get user by ID"""
    for user in self.users:
        if user.user_id == user_id:
            return user
    return None


ProjectTracker.get_user_by_id = get_user_by_id


def main():
    """Main entry point"""
    cli = ProjectCLI()
    cli.run()


if __name__ == "__main__":
    main()