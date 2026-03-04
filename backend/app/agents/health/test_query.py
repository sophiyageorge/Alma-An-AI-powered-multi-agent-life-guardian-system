from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.exercise import ExerciseEntry

db: Session = SessionLocal()

print("Database connection works!")

# Fetch all rows
entries = db.query(ExerciseEntry).all()
print(f"Found {len(entries)} rows")
for e in entries:
    print(
        f"ID: {e.id}, Heart Rate: {e.heart_rate}, "
        f"BP: {e.bp_systolic}/{e.bp_diastolic}, "
        f"SPO2: {e.spo2}, Steps: {e.steps}, "
        f"Timestamp: {e.date_created}"
    )

db.close()