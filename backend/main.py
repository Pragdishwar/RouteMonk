from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import history, optimize

app = FastAPI(title="RouteMonk Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(history.router)
app.include_router(optimize.router)

@app.get("/")
def root():
    return {"message": "RouteMonk Backend Running!"}
