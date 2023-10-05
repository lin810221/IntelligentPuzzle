from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(1, 3)

    @task
    def read_item(self):
        item_id = 1
        self.client.get(f"/items/{item_id}")

    @task
    def create_item(self):
        data = {"name": "New Item", "description": "A new item"}
        self.client.post("/items/", json=data)

    @task
    def update_item(self):
        item_id = 1
        data = {"name": "Updated Item", "description": "An updated item"}
        self.client.put(f"/items/{item_id}", json=data)

    @task
    def delete_item(self):
        item_id = 1
        self.client.delete(f"/items/{item_id}")
