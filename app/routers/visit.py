from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

# 1️⃣ Get GP List
@router.get("/gp-list")
def get_gp_list():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT gp_id, gp_name FROM gram_panchayat")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# 2️⃣ Get Inspection Types
@router.get("/inspection-types")
def get_inspection_types():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT inspection_type_id, inspection_type_name FROM inspection_type")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# 3️⃣ Save GP Visit
@router.post("/gp-visit")
def save_gp_visit(payload: dict):
    conn = get_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO gp_visit
    (gp_id, inspection_type_id, remarks, user_id)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        payload["gp_id"],
        payload["inspection_type_id"],
        payload.get("remarks"),
        payload["user_id"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True, "message": "GP Visit entry saved successfully"}
