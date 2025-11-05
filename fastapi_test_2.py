from fastapi import FastAPI, HTTPException, Query
import random
from typing import Annotated
from pydantic import BaseModel, Field

#> fastapi dev fastapi_test.py

# Instancia de la clase FastAPI
app = FastAPI()

# Acumulador
items_db = ["HOLA", "MUNDO", "FASTAPI", "PYTHON", "API"]

class Item(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
        description="Nombre del ítem."
    )

# El decorador @app.get("/")
# define una ruta GET en la raíz del servidor
# Cuando alguien envíe un GET request a "/",
# la función home() será llamada
@app.get("/")
def home():
    return {"message": "¡Hola, mundo!"}


# 'max_value' es un parámetro de ruta
# Cuando alguien envíe un GET request a "/random/{max_value}",
# la función get_random_number() será llamada
@app.get("/random/{max_value}")
def get_random_number(max_value: int):
    random_number = random.randint(1, max_value)
    return {
        "max_value": max_value,
        "random_number": random_number
    }

# Endpoint para agregar un ítem a la lista
# Utiliza el método POST
class ItemResponse(BaseModel):
    message: str
    item: str

@app.post("/items", response_model=ItemResponse)
def add_item(item: Item):
    
    # Verificar si el ítem ya existe
    if item.name in items_db:
        raise HTTPException(status_code=400, detail="El ítem ya existe.")

    # Si está todo bien, agregar el nombre del item
    items_db.append(item.name)

    return ItemResponse(
        message=f"Ítem '{item.name}' agregado exitosamente.",
        item=item.name
    )

# Endpoint para obtener la lista de ítems en orden aleatorio
# Utiliza el método GET

class ItemListResponse(BaseModel):
    original_order: list[str]
    randomized_order: list[str]
    item_count: int

@app.get("/items", response_model=ItemListResponse)
def get_randomized_items():
    # Copiar y mezclar la lista de ítems
    randomized = items_db.copy()

    if len(randomized) > 1:
        # Mezclar la lista de ítems
        random.shuffle(randomized)    
        return ItemListResponse(
            original_order=items_db,
            randomized_order=randomized,
            item_count=len(items_db)
        )
    else:
        raise HTTPException(status_code=404, detail="No hay suficientes ítems para mezclar.")

# Endpoint para actualizar un ítem en la lista
# Utiliza el método PUT
class ItemUpdateResponse(BaseModel):
    message: str
    old_item: str
    new_item: str

@app.put("/items/{update_item_name}", response_model=ItemUpdateResponse)
def update_item(update_item_name: str, item: Item):
    """
    Args:
        update_item_name (str): Nombre del ítem a actualizar.
        item (Item): Nuevo nombre del ítem en el cuerpo de la solicitud.
    """

    #1- Verificar si el ítem a actualizar existe
    if update_item_name not in items_db:
        raise HTTPException(
            status_code=404,
            detail="El ítem a actualizar no existe.")

    #2- Verificar si el nuevo nombre ya existe
    if item.name in items_db:
        raise HTTPException(
            status_code=409,
            detail="El nuevo nombre del ítem ya existe.")
    
    #4- Actualizar el ítem en la lista si todo está bien
    index = items_db.index(update_item_name)
    items_db[index] = item.name

    return ItemUpdateResponse(
        message="Ítem actualizado exitosamente.",
        old_item=update_item_name,
        new_item=item.name
    )

# Endpoint para eliminar un ítem de la lista
# Utiliza el método DELETE
class ItemDeleteResponse(BaseModel):
    message: str
    delete_item: str
    remaining_items: int

@app.delete("/items/{item}", response_model=ItemDeleteResponse)
def delete_item(item: str):
    if item not in items_db:
        raise HTTPException(
            status_code=404,
            detail="El ítem a eliminar no existe.")
    
    items_db.remove(item)

    return ItemDeleteResponse(
        message=f"Ítem '{item}' eliminado exitosamente.",
        delete_item=item,
        remaining_items=len(items_db)
    )