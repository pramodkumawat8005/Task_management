from fastapi import FastAPI 
from dto import productDto
from mockdata import product
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/products")
def get_products():
    return product

@app.get("/products/{id}")
def get_one_product(id: int):
    return product[id - 1]

@app.post("/add_products")
def add_product(product_data: productDto):
    product_data = product_data.model_dump()
    product.append(product_data)
    return product_data

@app.put("/update_products/{id}")
def update_product(id: int, product_data: productDto):
    for index, p in enumerate(product):
        if p["id"] == id:
            product[index] = product_data.model_dump()
            return {"message": "Product updated", "product": product[index]}
    return {"message": "Product not found"}

@app.delete("/delete_products/{id}")
def delete_product(id: int):
    for index, p in enumerate(product):
        if p["id"] == id:
            deleted_product = product.pop(index)
            return {"message": "Product deleted", "product": deleted_product}
    return {"message": "Product not found"}
