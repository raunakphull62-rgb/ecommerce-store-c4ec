from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from supabase import create_client, Client
from supabase.py import SupabaseClient
from supabase.exceptions import ClientException
from jose import jwt
from datetime import datetime, timedelta
import os

# Initialize the supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SECRET = os.getenv("SUPABASE_SECRET")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize the FastAPI router
router = APIRouter()

# Define the order schema
class Order(BaseModel):
    id: int
    user_id: int
    order_date: datetime
    total: float
    status: str

# Define the order creation schema
class OrderCreate(BaseModel):
    user_id: int
    order_date: datetime
    total: float
    status: str

# Define the order update schema
class OrderUpdate(BaseModel):
    order_date: datetime
    total: float
    status: str

# Define the authentication scheme
security = HTTPBearer()

# Define the function to verify the JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Define the function to get the current user
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(token.credentials)
    return payload

# Define the function to create an order
@router.post("/orders", response_model=Order)
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    try:
        # Create a new order
        new_order = {
            "user_id": order.user_id,
            "order_date": order.order_date,
            "total": order.total,
            "status": order.status
        }
        # Insert the new order into the database
        data = supabase.from_("orders").insert([new_order]).execute()
        # Return the newly created order
        return data[0]
    except ClientException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define the function to get all orders
@router.get("/orders", response_model=List[Order])
async def get_orders(current_user: dict = Depends(get_current_user)):
    try:
        # Get all orders from the database
        data = supabase.from_("orders").select("*").execute()
        # Return the list of orders
        return data
    except ClientException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define the function to get an order by ID
@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int, current_user: dict = Depends(get_current_user)):
    try:
        # Get the order from the database
        data = supabase.from_("orders").select("*").eq("id", order_id).execute()
        # Return the order
        return data[0]
    except ClientException as e:
        raise HTTPException(status_code=404, detail="Order not found")

# Define the function to update an order
@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderUpdate, current_user: dict = Depends(get_current_user)):
    try:
        # Update the order in the database
        data = supabase.from_("orders").update({
            "order_date": order.order_date,
            "total": order.total,
            "status": order.status
        }).eq("id", order_id).execute()
        # Return the updated order
        return data[0]
    except ClientException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define the function to delete an order
@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, current_user: dict = Depends(get_current_user)):
    try:
        # Delete the order from the database
        supabase.from_("orders").delete().eq("id", order_id).execute()
        # Return a success message
        return {"message": "Order deleted successfully"}
    except ClientException as e:
        raise HTTPException(status_code=404, detail="Order not found")