"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports-related activities
    "Basketball Team": {
        "description": "Competitive basketball practices and games",
        "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["tyler@mergington.edu", "nina@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Casual and competitive soccer sessions",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    # Artistic activities
    "Art Club": {
        "description": "Painting, drawing, and mixed-media workshops",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and school productions",
        "schedule": "Tuesdays, 5:00 PM - 7:00 PM",
        "max_participants": 30,
        "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Competitive debating and public speaking practice",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["oliver@mergington.edu", "grace@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["lucas@mergington.edu", "emma.s@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email to avoid case-sensitive duplicates
    normalized_email = email.strip().lower()

    # Validate student is not already signed up
    if normalized_email in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Validate capacity
    if len(activity["participants"]) >= activity.get("max_participants", float("inf")):
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Validate student is not already signed up
    if normalized_email in (p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
