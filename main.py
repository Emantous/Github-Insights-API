from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI
import os


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI(title="GitHub Insights API")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "github-insights-api",
        "version": os.getenv("APP_VERSION", "0.1.0")
    }

'''@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict'''