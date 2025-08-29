from fastapi import APIRouter
from db import get_connection

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM deliveries ORDER BY created_at DESC;")
    rows = cur.fetchall()
    conn.close()
    return {"history": rows}
