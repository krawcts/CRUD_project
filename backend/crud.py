from sqlalchemy.orm import Session
from schemas import ProductUpdate, ProductCreate
from models import ProductModel

# get all (select * from)
def get_all_products(db: Session):
    """
    This function return all data from the products table
    """
    return db.query(ProductModel).all()

# get where id = 1
def get_product(db: Session, product_id: int):
    """
    This function return just one product from the products table
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# insert into (create)
def create_product(db: Session, product: ProductCreate):
    """
    This function creates one product and put it into products table
    """
    # transform view into ORM
    db_product = ProductModel(**product.model_dump())
    # add into table
    db.add(db_product)
    # commit
    db.commit()
    # refresh database
    db.refresh(db_product)
    # return created item to user
    return db_product

# udate where id = 1


# delete where id = 1
def delete_product(db: Session, product_id: int):
    """
    This function deletes one product from the products table
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product