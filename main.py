from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
redis = get_redis_connection(
        host=os.getenv('REDIS_HOST'),
        port=17963,
        decode_responses=True,
        username="default",
        password=os.getenv('REDIS_PASSWORD')
)

class Product(HashModel, index = True):
    name:str
    price:float
    quantity:int

    class Meta:
        database = redis

def format(pk:str):
    product = Product.get(pk)

    return {
        'id':product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }

@app.get("/")
def read_root():
    return "Server is up and running"

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
def get(pk:str):
    return format(pk)

@app.delete("/products/{pk}")
def delete(pk:str):
    return Product.delete(pk)
