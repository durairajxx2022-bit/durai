# FitBuddy – AI Fitness Plan Generator (Gemini + FastAPI)

Generates personalized 7-day workout plans and nutrition tips using Google's
Gemini models, with feedback-based plan revision and an admin dashboard.

## Project structure
```
fitbuddy/
├── requirements.txt
├── .env.example
├── fitbuddy.db              # auto-created on first run
└── app/
    ├── main.py               # FastAPI entry point
    ├── routes.py              # All route handlers
    ├── database.py            # SQLAlchemy models + DB helpers
    ├── schemas.py              # Pydantic request models
    ├── gemini_generator.py     # Gemini 1.5 Pro – workout plan generation
    ├── gemini_flash_generator.py # Gemini Flash – nutrition tips
    ├── updated_plan.py         # Feedback-based plan updater (Gemini 1.5 Pro)
    ├── templates/
    │   ├── index.html          # Input form
    │   ├── result.html         # Plan, tip, feedback form
    │   └── all_users.html      # Admin dashboard
    └── static/images/          # Put a gym-bg.jpg here for the background
```

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv fitbuddy-env
   # Windows
   fitbuddy-env\Scripts\activate
   # macOS/Linux
   source fitbuddy-env/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Gemini API key. Copy `.env.example` to `.env` and fill it in:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   Get a key from Google AI Studio: https://aistudio.google.com/app/apikey

4. (Optional) Drop a gym-themed image at `app/static/images/gym-bg.jpg` for the UI background.

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open the app:
   - Web UI: http://127.0.0.1:8000
   - Interactive API docs: http://127.0.0.1:8000/docs
   - Admin dashboard: http://127.0.0.1:8000/view-all-users

## Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Home page (input form) |
| `/generate-workout` | POST (form) | Generates plan + tip, saves user & plan |
| `/submit-feedback` | POST (form) | Revises plan based on feedback |
| `/view-all-users` | GET | Admin dashboard of all users & plans |
| `/api/generate-plan` | POST (JSON) | Same as above, JSON API |
| `/api/generate-workout/gemini` | POST (JSON) | Raw workout generation |
| `/api/nutrition-tip` | GET | Nutrition tip by goal |
| `/api/update-plan/{user_id}` | POST (JSON) | Update plan via feedback, JSON API |

## Notes
- Data persists in a local SQLite file (`fitbuddy.db`), created automatically on first run.
- Each user's original and feedback-updated plans are stored separately.
