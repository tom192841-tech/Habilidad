from fastapi import APIRouter, Response, status
from config.db import conn
from models.app import products
from schemas.app import Product
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
user = APIRouter()

@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    filas = conn.execute(users.select()).fetchall()
    return [fila._asdict() for fila in filas]

@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    r = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    return r._asdict()

@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str):
    r = conn.execute(users.select().where(users.c.id == id)).first()
    return r._asdict()

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(name = user.name,
                email = user.email,
                password=f.encrypt(user.password.encode("utf-8"))
                ).where(users.c.id == id))
    result = conn.execute(users.select().where(users.c.id == id)).first()
    return result._asdict()
    