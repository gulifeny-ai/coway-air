from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import BASE_DIR, APP_TITLE
from app.utils.startup import ensure_directories, build_dart_index
from app.routes import auth, pages, research, reports, best_reports, admin, health

app = FastAPI(title=APP_TITLE)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")


@app.on_event("startup")
async def on_startup() -> None:
    ensure_directories()
    build_dart_index()


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(research.router)
app.include_router(reports.router)
app.include_router(best_reports.router)
app.include_router(admin.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
