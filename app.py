from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from psutil import users
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
users_collection = db["users"]

# CORS - Allow all origins for dev (be strict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Serializer
def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user["age"]
    }

# Serve UI
@app.get("/")
def home(request: Request):
    users = list(users_collection.find())
    users = [serialize_user(u) for u in users]
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "users": users}  
    )

# Create
@app.post("/create")
async def create_user(name: str = Form(...), email: str = Form(...), age: int = Form(...)):
    user = {"name": name, "email": email, "age": age}
    users_collection.insert_one(user)
    return {"msg": "User created"}

# Read (API)
@app.get("/users")
def get_users():
    users = list(users_collection.find())
    return [serialize_user(user) for user in users]

# Update
@app.post("/update")
async def update_user(user_id: str = Form(...), name: str = Form(...), email: str = Form(...), age: int = Form(...)):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"name": name, "email": email, "age": age}}
    )
    return {"msg": "User updated"}

# Delete
@app.post("/delete")
async def delete_user(user_id: str = Form(...)):
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"msg": "User deleted"}
