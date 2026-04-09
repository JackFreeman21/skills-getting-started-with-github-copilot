# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Remove participants from activities
- Web interface for easy management

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - **Web Interface**: http://localhost:8000 (main application)
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Usage

- **View Activities**: Visit the web interface to see all available activities and current participants
- **Sign Up**: Use the web form or API to register for activities
- **Manage Participants**: Remove students from activities using the delete buttons or API

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/`                                                               | Redirect to web interface                                           |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/participants/{email}`               | Remove a student from an activity                                   |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

**Available Activities:**
- Chess Club (Intellectual)
- Programming Class (Intellectual)
- Gym Class (Sports)
- Basketball Team (Sports)
- Soccer Club (Sports)
- Art Club (Artistic)
- Drama Club (Artistic)
- Debate Club (Intellectual)
- Science Club (Intellectual)

All data is stored in memory, which means data will be reset when the server restarts.
