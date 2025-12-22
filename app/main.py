from fastapi import FastAPI
from pydantic import BaseModel
import app.db as db

app = FastAPI()

# -----------------
# Login Request Model
# -----------------
class LoginRequest(BaseModel):
    mobile: str
    password: str


@app.get("/")
def root():
    return {"status": "GP Visit API Running"}

#-------------------
#REQUEST MODEL
#-------------------
from datetime import date

class GPVisitRequest(BaseModel):
    user_id: int
    gp_id: int
    inspection_type_id: int
    visit_date: date
    latitude: float
    longitude: float
    remarks: str

# -----------------
# LOGIN API
# -----------------
@app.post("/login")
def login(data: LoginRequest):
    try:
        conn = db.get_db()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT user_id, name, designation, role, password_hash
        FROM users
        WHERE mobile = %s AND status = 1
        """
        cursor.execute(sql, (data.mobile,))
        user = cursor.fetchone()

        if not user:
            return {"success": False, "message": "User not found or inactive"}

        # Plain password match (JWT + hashing will come next)
        if data.password != user["password_hash"]:
            return {"success": False, "message": "Invalid password"}

        return {
            "success": True,
            "user_id": user["user_id"],
            "name": user["name"],

            "designation": user["designation"],
            "role": user["role"]
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
from datetime import date
# -----------------
# GP VISIT ENTRY API
# -----------------

@app.post("/gp-visit")
def create_gp_visit(data: GPVisitRequest):
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO gp_visit
        (user_id, gp_id, inspection_type_id, visit_date,
         latitude, longitude, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            data.user_id,
            data.gp_id,
            data.inspection_type_id,
            data.visit_date,
            data.latitude,
            data.longitude,
            data.remarks
        ))

        conn.commit()

        return {
            "success": True,
            "message": "GP Visit entry saved successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
# -----------------
# GP LIST API
# -----------------
@app.get("/gp-list")
def get_gp_list():
    conn = db.get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT gp_id, gp_name FROM gram_panchayat")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# -----------------
# INSPECTION TYPE LIST API
# -----------------
@app.get("/inspection-types")
def get_inspection_types():
    conn = db.get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT inspection_type_id, inspection_type_name FROM inspection_type"
    )
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data
@app.get("/gp-list")
def get_gp_list():
    try:
        conn = db.get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT gp_id, gp_name FROM gram_panchayat ORDER BY gp_name"
        )
        data = cursor.fetchall()
        return data
    except Exception as e:
        return {"error": str(e)}
# For Azure health check
@app.get("/health")
def health():
    return {"status": "ok"}
