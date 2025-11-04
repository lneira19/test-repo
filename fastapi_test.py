from fastapi import FastAPI, HTTPException, Query
import random
from typing import Annotated

#> fastapi dev fastapi_test.py

# Instancia de la clase FastAPI
app = FastAPI()

# Acumulador
items_db = ["HOLA", "MUNDO", "FASTAPI", "PYTHON", "API"]

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
@app.post("/items")
def add_item(body: dict):
    item_name = body.get("name")
    
    # Validación simple para el campo 'name'
    if not item_name:
        raise HTTPException(status_code=400, detail="Campo 'name' es requerido.")
    
    # Verificar si el ítem ya existe
    if item_name in items_db:
        raise HTTPException(status_code=400, detail="El ítem ya existe.")

    # Si está todo bien, agregar el nombre del item
    items_db.append(item_name)
    return {"message": f"Ítem '{item_name}' agregado exitosamente."}

# Endpoint para obtener la lista de ítems en orden aleatorio
# Utiliza el método GET
@app.get("/items")
def get_randomized_items():
    # Copiar y mezclar la lista de ítems
    randomized = items_db.copy()

    if len(randomized) > 1:
        # Mezclar la lista de ítems
        random.shuffle(randomized)    
        return {
            "Orden original": items_db,
            "Orden aleatorio": randomized,
            "Cantidad de ítems": len(items_db)
        }
    else:
        raise HTTPException(status_code=404, detail="No hay suficientes ítems para mezclar.")

# Endpoint para actualizar un ítem en la lista
# Utiliza el método PUT
@app.put("/items/{update_item_name}")
def update_item(update_item_name: str, body: dict):
    """
    Args:
        update_item_name (str): Nombre del ítem a actualizar.
        body (dict): Cuerpo de la solicitud que contiene el nuevo nombre del ítem.
    """

    #1- Verificar si el ítem a actualizar existe
    if update_item_name not in items_db:
        raise HTTPException(
            status_code=404,
            detail="El ítem a actualizar no existe.")
    
    #2- Obtener el nuevo nombre del ítem
    #  desde el cuerpo de la solicitud
    new_name = body.get("name")
    if not new_name:
        raise HTTPException(
            status_code=400,
            detail="Campo 'name' es requerido.")

    #3- Verificar si el nuevo nombre ya existe
    if new_name in items_db:
        raise HTTPException(
            status_code=409,
            detail="El nuevo nombre del ítem ya existe.")
    
    #4- Actualizar el ítem en la lista si todo está bien
    index = items_db.index(update_item_name)
    items_db[index] = new_name

    return {
        "message": f"Ítem '{update_item_name}' actualizado a '{new_name}'."
    }

# Endpoint para eliminar un ítem de la lista
# Utiliza el método DELETE
@app.delete("/items/{item}")
def delete_item(item: str):
    if item not in items_db:
        raise HTTPException(
            status_code=404,
            detail="El ítem a eliminar no existe.")
    
    items_db.remove(item)

    return {
        "message": f"Ítem '{item}' eliminado exitosamente.",
        "items_restantes": len(items_db)
    }