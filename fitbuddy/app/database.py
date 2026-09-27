"""
database.py
SQLAlchemy models + persistence helpers for FitBuddy.
Stores user info and AI-generated workout plans in a local SQLite DB.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    schedule = Column(Integer, default=7)


class WorkoutPlan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_plan = Column(Text, nullable=True)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


# ---------- User / Plan persistence helpers ----------

def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    existing = db.query(User).filter_by(id=user_id).first()
    if existing:
        existing.name = name
        existing.age = age
        existing.weight = weight
        existing.goal = goal
        existing.intensity = intensity
    else:
        user = User(
            id=user_id, name=name, age=age, weight=weight,
            goal=goal, intensity=intensity, schedule=7,
        )
        db.add(user)
    db.commit()
    db.close()


def save_plan(user_id: int, plan: str, nutrition_tip: str = None):
    db = SessionLocal()
    existing = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    if existing:
        existing.original_plan = plan
        if nutrition_tip:
            existing.nutrition_tip = nutrition_tip
    else:
        workout = WorkoutPlan(user_id=user_id, original_plan=plan, nutrition_tip=nutrition_tip)
        db.add(workout)
    db.commit()
    db.close()


def update_plan(user_id: int, updated_text: str):
    db = SessionLocal()
    workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    if workout:
        workout.updated_plan = updated_text
        db.commit()
    db.close()


def get_original_plan(user_id: int):
    db = SessionLocal()
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    db.close()
    return plan.original_plan if plan else None


def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user


def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users


def get_all_plans():
    db = SessionLocal()
    plans = db.query(WorkoutPlan).all()
    db.close()
    return plans
