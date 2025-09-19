from fastapi import FastAPI
from api.endpoints.accounts import router as accounts_router
from api.endpoints.products import router as products_router

app = FastAPI()

app.include_router(accounts_router, prefix="/account", tags=["account"])
app.include_router(products_router, prefix="/products", tags=["products"])




