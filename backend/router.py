from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_all_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()

# create route to fetch all itens
@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    all_products = get_all_products(db)
    return all_products

# create route to fetch 1 item
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist.")
    return product

# create route to add 1 item
@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(product=product, db=db)


# create route to delete 1 item
@router.delete()

# create route to update 1 item
@router.put()