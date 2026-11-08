from fastapi import FastAPI, File, HTTPException, UploadFile, BackgroundTasks

from db.connection import init_db
from services.dtp import import_dtp, get_dtp, get_load_log
from services.weather import fill_pending, get_weather

init_db()
app = FastAPI()


@app.post("/api/upload")
async def upload_csv(
    background: BackgroundTasks,
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Нужен CSV-файл")

    content = await file.read()

    try:
        count = import_dtp(content, file.filename)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=f"Ошибка в CSV: {e}")

    background.add_task(fill_pending)
    return {"inserted": count}
@app.get("/api/dtp")
def list_dtp(page: int = 1):
    return get_dtp(page=page)

@app.get("/api/weather")
def list_dtp(page: int = 1):
    return get_weather(page=page)

@app.get("/api/load_log")
def load_log(page: int = 1):
    return get_load_log()