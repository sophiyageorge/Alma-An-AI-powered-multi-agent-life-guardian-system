# # app/routers/meal_approval.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.dependencies import get_current_user, get_db
# from app.models.meal import WeeklyMealPlan

# router = APIRouter()


# @router.post("/meal-plan/{meal_plan_id}/approve")
# def approve_meal_plan(
#     meal_plan_id: int,
#     current_user = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     User approves a meal plan. After approval, grocery list can be generated.
#     """
#     entry = db.query(WeeklyMealPlan).filter(
#         WeeklyMealPlan.id == meal_plan_id,
#         WeeklyMealPlan.user_id == current_user.user_id
#     ).first()

#     if not entry:
#         raise HTTPException(status_code=404, detail="Meal plan not found")

#     entry.is_approved = True
#     db.commit()
#     db.refresh(entry)

#     return {
#         "meal_plan_id": entry.id,
#         "approved": entry.is_approved,
#         "message": "Meal plan approved. You can now generate grocery list."
#     }
# app/routers/meal_approval.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_current_user, get_db
from app.models.meal import WeeklyMealPlan

router = APIRouter()


@router.post("/meal-plan/{meal_plan_id}/approve")
def approve_meal_plan(
    meal_plan_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User approves a meal plan. After approval, grocery list can be generated.
    """

    entry = db.query(WeeklyMealPlan).filter(
        WeeklyMealPlan.id == meal_plan_id,
        WeeklyMealPlan.user_id == current_user.user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    # ✅ Check if already approved
    if entry.is_approved:
        return {
            "meal_plan_id": entry.id,
            "approved": True,
            "message": "Meal plan already approved."
        }

    # ✅ Approve meal plan
    entry.is_approved = True
    db.commit()
    db.refresh(entry)

    return {
        "meal_plan_id": entry.id,
        "approved": entry.is_approved,
        "message": "Meal plan approved. You can now generate grocery list."
    }