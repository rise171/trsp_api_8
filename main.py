import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from database import create_tables, delete_tables
from fastapi.middleware.cors import CORSMiddleware
from routers import router

load_dotenv()

@asynccontextmanager
async def life(app: FastAPI):
    await create_tables()
    print("base are create")
    yield
    await delete_tables()
    print("base are delete")

app = FastAPI(lifespan=life)

app.include_router(router)

async def reset_database():
    print("delete database")
    await delete_tables()
    print("create again")
    await create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

if __name__ == "__main__":
    asyncio.run(reset_database())
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)