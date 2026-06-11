# Behavior-Driven Diagrams (BDD)

This document maps out the system behaviors using behavior diagrams (Mermaid). They define expected reactions, state changes, and permission gates across the application.

---

## 1. Authentication & Session State Diagram

Shows the behavior flow of registration, login, session validation, and logout.

```mermaid
stateDiagram-v2
    [*] --> LoggedOut : Start Application
    
    state LoggedOut {
        [*] --> DisplayLoginMenu
        DisplayLoginMenu --> RegisterMode : Select Option 2
        DisplayLoginMenu --> LoginMode : Select Option 1
        DisplayLoginMenu --> [*] : Select Option 3 (Exit)
        
        RegisterMode --> CheckUsernameExists : Submit Username
        CheckUsernameExists --> RegisterMode : Username taken (Error)
        CheckUsernameExists --> AddUserToDb : Username unique
        AddUserToDb --> AutoLoginUser : Success
        
        LoginMode --> ValidateUsername : Submit Username
        ValidateUsername --> LoginMode : Not Found (Error)
    }

    AutoLoginUser --> LoggedIn : Transition Session
    ValidateUsername --> LoggedIn : Success
    
    state LoggedIn {
        [*] --> DisplayMainMenu
        DisplayMainMenu --> ViewProjects : View options
        DisplayMainMenu --> CreateProject : Create project
        DisplayMainMenu --> ManageTasks : Manage tasks
        DisplayMainMenu --> LoggedOut : Logout (Option 6)
    }
```

---

## 2. Project Ownership & Permission Flow Diagram

Defines the system behavior and authorization gate when a user tries to manage a project's tasks.

```mermaid
flowchart TD
    Start[User selects Option 4: Manage Project Tasks] --> InputProjId[User inputs Project ID]
    InputProjId --> FetchProj{Does Project exist?}
    
    FetchProj -- No --> ShowError[Show project not found error] --> End[Return to Main Menu]
    
    FetchProj -- Yes --> CheckOwner{Is Current User ID == Project Owner ID?}
    
    CheckOwner -- No --> DenyAccess[Display Permission Error: \n'You can only manage tasks in your own projects!'] --> End
    
    CheckOwner -- Yes --> GrantAccess[Grant task management access \n& Show Task Menu] --> TaskMenuOption[User chooses task option]
    
    TaskMenuOption --> AddTask[Add Task]
    TaskMenuOption --> ViewTask[View Tasks]
    TaskMenuOption --> UpdateTask[Update Status]
    TaskMenuOption --> DeleteTask[Delete Task]
    TaskMenuOption --> Back[Back to Main Menu] --> End
```

---

## 3. Task Status Lifecycle State Diagram

Illustrates the state machine and valid state changes for individual tasks.

```mermaid
stateDiagram-v2
    [*] --> Pending : Task Created
    
    state Pending {
        [*] --> Idle
    }
    
    Pending --> InProgress : Update status to 'in_progress'
    Pending --> Completed : Update status to 'completed'
    
    state InProgress {
        [*] --> WorkStarted
    }
    
    InProgress --> Pending : Update status to 'pending'
    InProgress --> Completed : Update status to 'completed'
    
    state Completed {
        [*] --> SetCompletedTime : Set completed_at timestamp
    }
    
    Completed --> Pending : Update status to 'pending' (Clear completed_at)
    Completed --> InProgress : Update status to 'in_progress' (Clear completed_at)
```
