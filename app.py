from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from uuid import uuid4 as uuid

app = FastAPI()

class Producto(BaseModel):
    nombre:str
    precio:float
    stock:int
    id: Optional[float]

inventario = [
    {"id": 1, "nombre": "Mouse Logitech G502", "precio": 50.0, "stock": 12},
    {"id": 2, "nombre": "Teclado Mecánico Redragon", "precio": 45.0, "stock": 8}
]

@app.get("/productos")
def productos():
    return inventario

@app.get("/productos/{producto_id}")
def buscar_producto(producto_id: float):
    producto = [i for i in inventario if i["id"] == producto_id]
    if producto:
        return producto
    raise HTTPException(status_code=404,detail="No se encontro tu producto")

@app.post("/productos")
def agregar_producto(producto: Producto):
    producto.id = uuid()
    inventario.append(producto)
    return producto

@app.delete("/productos/{producto_id}")
def elminar_producto(producto_id: float):
    for index,post in enumerate(inventario):
        if post["id"] == producto_id:
            inventario.pop(index)
            return {"message": "Post has been deleted succesfully"}
    raise HTTPException(status_code=404,detail="No se encontro tu producto")
            
    


