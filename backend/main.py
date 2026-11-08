from fastapi import FastAPI, File, HTTPException, UploadFile

from db.connection import init_db
from services.dtp import import_dtp, get_dtp

init_db()
app = FastAPI()


@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Нужен CSV-файл")

    content = await file.read()

    try:
        count = import_dtp(content)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Ошибка в CSV: {e}")

    return {"inserted": count}

@app.get("/api/dtp")
def list_dtp(page: int = 1):
    return get_dtp(page=page)