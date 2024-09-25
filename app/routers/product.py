from venv import create

from app.routers.category import create_category
from fastapi import APIRouter, Depends, status,  HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import CreateProduct

from slugify import slugify

router = APIRouter(prefix='/products',tags=['products'])

@router.get('/')
async def all_products(db: Annotated[Session,Depends(get_db)]):
    products = db.scalars(select(Product).where(Product.is_active == True and Product.stock > 0)).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    else:
        return products



@router.post('/create')
async def create_product(db: Annotated[Session,Depends(get_db)], create_product: CreateProduct):
    db.execute(insert(Product).values(
        name = create_product.name,
        description = create_product.description,
        price = create_product.price,
        rating = 0.0,
        slug = slugify(create_product.name),
        image_url = create_product.image_url,
        category_id = create_product.category,
        stock = create_product.stock
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def product_by_category(category_slug: str):
    pass

@router.put('/detail/{product_slug}')
async def update_product(db: Annotated[Session, Depends(get_db)] ,update_prod : CreateProduct ,product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    else:
        db.execute(update(Product).where(Product.slug == product_slug).values(
        name = update_prod.name,
        description = update_prod.description,
        price = update_prod.price,
        rating = 0.0,
        slug = slugify(update_prod.name),
        image_url = update_prod.image_url,
        category_id = update_prod.category,
        stock = update_prod.stock
        ))
    return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Product update is successful'
        }

@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[Session, Depends(get_db)] ,product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='here are no product'
        )
    else:
        return product


@router.delete('/delete')
async def delete_product(db: Annotated[Session,Depends(get_db)],product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='here are no product'
        )
    else:
        db.execute(update(Product).where(Product.slug == product_slug).values(
            is_active = False
        ))
        db.commit()
    return {
    'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }



