from src.controllers.auth import auth_router
from fastapi import FastAPI
import uvicorn

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(auth_router)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)