from fastapi import FastAPI

app = FastAPI()

items = {}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "item": items.get(item_id)}

@app.post("/items/")
def create_item(item: dict):
    item_id = len(items) + 1
    items[item_id] = item
    return {"item_id": item_id, "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: dict):
    if item_id in items:
        items[item_id] = updated_item
        return {"message": "Item updated successfully"}
    else:
        return {"error": "Item not found"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted successfully"}
    else:
        return {"error": "Item not found"}
