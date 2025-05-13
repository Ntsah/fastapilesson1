from fastapi import FastAPI
from sqlalchemy.testing.suite.test_reflection import users

from app.routers import category, products,auth

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)