from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product as ProductModel
from schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from auth import verify_token

router = APIRouter()
security = HTTPBearer()

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

@router.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    new_product = ProductModel(name=product.name, price=product.price, description=product.description)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    products = db.query(ProductModel).all()
    return products

@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    existing_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.description = product.description
    db.commit()
    db.refresh(existing_product)
    return existing_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(token.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}