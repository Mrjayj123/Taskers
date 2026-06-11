# Project Management System (Taskers1)

A terminal-based Project Management System featuring user registration/login, project creation, task management, and data persistence. Built using Python, it manages the relationship: **User → Projects → Tasks**.

---

## How It Works: System Flow

The application behaves as a structured CLI loop, interacting with JSON-based storage for persistence. Below is the step-by-step runtime flow:

```mermaid
graph TD
    Start([Run main.py]) --> LoadDb[Load data/tracker_data.json]
    LoadDb --> AuthLoop{User Logged In?}
    
    AuthLoop -- No --> LoginMenu[Show Login Menu]
    LoginMenu --> ChoiceAuth{User Choice}
    ChoiceAuth -- 1. Login --> DoLogin[Enter Username & Validate]
    ChoiceAuth -- 2. Register --> DoRegister[Register User & Role]
    ChoiceAuth -- 3. Exit --> ExitApp([Exit System])
    
    DoLogin --> AuthLoop
    DoRegister --> AuthLoop
    
    AuthLoop -- Yes --> MainMenu[Show Main Menu]
    MainMenu --> ChoiceMain{User Choice}
    
    ChoiceMain -- 1. View All Projects --> ViewProj[List all project IDs, names, owners, task counts]
    ChoiceMain -- 2. Create Project --> CreateProj[Create project with current user as owner]
    ChoiceMain -- 3. View My Projects --> ViewMyProj[List projects owned by current user]
    ChoiceMain -- 4. Manage Tasks --> ManageTasks[Check project ownership -> Manage task menu]
    ChoiceMain -- 5. View Users --> ViewUsers[List usernames, roles, and project counts]
    ChoiceMain -- 6. Logout --> DoLogout[Logout current user]
    
    ViewProj --> MainMenu
    CreateProj --> MainMenu
    ViewMyProj --> MainMenu
    ManageTasks --> MainMenu
    ViewUsers --> MainMenu
    DoLogout --> AuthLoop
```

### Detailed Flow Steps

1. **Initialization**:
   - Running `main.py` invokes the CLI loop in `cli.py`.
   - The system instantiates `ProjectTracker` in `models.py`, which loads existing users and projects from `models/data/tracker_data.json`.
2. **Authentication Loop**:
   - If no user is logged in, the **Login Menu** is shown.
   - The user can register a new username and select a role (admin, manager, developer, viewer), or log in with an existing username.
3. **Main Menu Loop**:
   - Once logged in, the user sees the **Main Menu**.
   - They can view all projects across the system or view only projects they own.
4. **Project and Task Management**:
   - When creating a project, the system generates an 8-character UUID. The logged-in user's ID is registered as the owner.
   - To manage tasks, the user must input the 8-character Project ID. The system checks ownership: **only the project owner can add, view, update, or delete tasks**.
5. **Persistence**:
   - Any modifications (creating projects, adding tasks, updating task statuses, deleting tasks/projects) trigger `self.tracker.save_data()`, writing updates immediately back to `tracker_data.json`.

---

## File Structure

- **[main.py](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/main.py)**: The main execution entry point for starting the CLI application.
- **[cli.py](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/cli.py)**: Handles user interaction, menus, console tables (with a fallback custom formatter in case `tabulate` is not installed), and input validation.
- **[models.py](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/models.py)**: Contains data models (`User`, `Task`, `Project`, `ProjectTracker`) and file storage I/O logic.
- **[utilis.py](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/utilis.py)**: General helper functions (date formatting, logging setup, email validator).
- **[test_tracker.py](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/test_tracker.py)**: Unit test suite for models and tracking logic.
- **[Pipfile](file:///wsl.localhost/Ubuntu/home/jay_joel/PYTHON/Learning/Taskers1/Pipfile)**: Manages dependencies (e.g., `tabulate`).

---

## Setup & Running the Code

### Prerequisites
- Python 3.12+
- Pipenv (optional, for virtual environment management)

### Installation
Clone or navigate to the project directory, then install the dependencies:
```bash
pipenv install
```
*Note: If you run the code without installing dependencies, the CLI will automatically fallback to a built-in custom table formatter.*

### Run the Application
Execute the entry point script:
```bash
python3 main.py
```

### Run Unit Tests
Run the unit test suite:
```bash
python3 test_tracker.py
```
