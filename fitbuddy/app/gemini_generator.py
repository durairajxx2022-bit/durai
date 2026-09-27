"""
gemini_generator.py
Uses Gemini 1.5 Pro to generate structured 7-day workout plans
and to revise plans based on user feedback.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")


def generate_workout_gemini(user_input: dict) -> str:
    """
    Generate a personalized, structured 7-day workout plan.

    Args:
        user_input (dict): expects keys 'goal' and 'intensity'.

    Returns:
        str: the generated workout plan text.
    """
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of
**{user_input['goal']}**, and prefers **{user_input['intensity']} intensity** workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
