from fastapi import FastAPI, File, HTTPException, UploadFile, BackgroundTasks

from db.connection import init_db, get_connection
from models.BaseModel import BaseModel
from models.data import load_features
from services.dtp import import_dtp, get_raw_dtp, get_load_log, get_daily
from services.feature import get_features, is_features_ready
from services.models import fetch_model
from services.utils import fetch_page
from services.weather import fill_pending, get_weather_raw, get_weather_parsed, get_weather

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
@app.get("/api/raw_dtp")
def list_raw_dtp(page: int = 1):
    return get_raw_dtp(page=page)

@app.get("/api/daily")
def list_daily(page: int = 1):
    return get_daily(page=page)

@app.get("/api/features")
def list_features(page: int = 1):
    return get_features(page)

@app.get("/api/weather_raw")
def list_weather_raw(page: int = 1):
    return get_weather_raw(page=page)

@app.get("/api/weather_parsed")
def list_weather_parsed(page: int = 1):
    return get_weather_parsed(page=page)

@app.get("/api/weather")
def list_weather_parsed(page: int = 1):
    return get_weather(page=page)

@app.get("/api/features/ready")
def features_ready():
    with get_connection() as conn:
        return is_features_ready(conn)

@app.get("/api/load_log")
def load_log(page: int = 1):
    return get_load_log()

@app.get("/api/runs")
def list_runs(page: int = 1, model_id: int = 1):
    return fetch_model(model_id, page, 500)

@app.get("/api/model_start")
def list_features(model_id: int = 1):
    with get_connection() as conn:
        if (model_id == 1):
            return BaseModel(conn).run()
        if (model_id == 2):
            return BaseModel(conn).run()
        return BaseModel(conn).run()