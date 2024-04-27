from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routers.chatbot import router as chatbot_router
from app.routers.currency import router as currency_router
from app.routers.flights import router as flights_router
from app.routers.places import router as places_router
from app.routers.weather import router as weather_router

app = FastAPI(title="External Services")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(flights_router)
app.include_router(weather_router)
app.include_router(currency_router)
app.include_router(chatbot_router)
app.include_router(places_router)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
