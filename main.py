import httpx
import logging

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


# Создание приложения FastAPI
app = FastAPI()

# CORS Middlware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://mike-auto.ru/api/proxy/filter/filter"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Referer": "https://mike-auto.ru/korea",
}

# Подключаем папку frontend/dist как статические файлы
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


@app.get("/api")
def read_root():
    return {"message": "Hello from FastAPI"}


# Эндпоинт для получения автомобилей с конкретной страницы
@app.get("/api/proxy/filter/page")
async def get_cars_page(
    page: int = Query(..., ge=1),
    manufacturerId: int | None = None,
    modelId: int | None = None,
    generationId: int | None = None,
    colorsId: int | None = None,
    fuelId: int | None = None,
    transmissionId: int | None = None,
    mountOneId: int | None = None,
    mountTwoId: int | None = None,
    yearOneId: int | None = None,
    yearTwoId: int | None = None,
    mileageOneId: int | None = None,
    mileageTwoId: int | None = None,
):
    """
    Возвращает автомобили с указанной страницы и фильтрацией.
    """
    params = {"page": page}
    if manufacturerId:
        params["manufacturerId"] = manufacturerId
    if modelId:
        params["modelId"] = modelId
    if generationId:
        params["generationId"] = generationId
    if colorsId:
        params["color"] = colorsId
    if fuelId:
        params["fuel"] = fuelId
    if transmissionId:
        params["transmission"] = transmissionId
    if mountOneId:
        params["mountOneId"] = mountOneId
    if mountTwoId:
        params["mountTwoId"] = mountTwoId
    if yearOneId:
        params["yearOne"] = yearOneId
    if yearTwoId:
        params["yearTwo"] = yearTwoId
    if mileageOneId:
        params["mileageOne"] = mileageOneId
    if mileageTwoId:
        params["mileageTwo"] = mileageTwoId

    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Fetching page {page} with filters: {params}")
            response = await client.get(BASE_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "page": page,
                "data": data.get("data", []),
                "pageCount": data.get("pageCount", 0),
            }
    except httpx.RequestError as e:
        logger.error(f"Error fetching page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch page {page}")
