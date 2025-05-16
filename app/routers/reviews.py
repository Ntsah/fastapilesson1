from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from sqlalchemy import select, insert, update
from app.routers.auth import get_current_user
from app.schemas import CreateProduct, CreateReview
from app.models import *

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get('/')
async def all_reviews(
        db: Annotated[AsyncSession, Depends(get_db)]
):
    reviews = await db.scalars(
        select(Review)
        .where(
            Review.is_active,
        )
    )
    all_reviews = reviews.all()
    if not all_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews'
        )
    return all_reviews


@router.get('/by_product/{product_id}')
async def products_reviews(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_id: int
):
    product = await db.scalar(
        select(Product)
        .where(
            Product.id == product_id,
            Product.is_active,
        )
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    reviews = await db.scalars(
        select(Review)
        .where(
            Review.product_id == product_id,
            Review.is_active,
        )
    )
    all_reviews = reviews.all()
    if not all_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no reviews')
    return all_reviews


@router.post('/')
async def add_review(
        db: Annotated[AsyncSession, Depends(get_db)],
        comment: str,
        grade: int,
        product_id: int,
        get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_supplier') or get_user.get('is_admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not allowed to add review')
    else:
        product = await db.scalar(
            select(Product)
            .where(
                Product.id == product_id,
                Product.is_active,
            )
        )
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )
        await db.execute(
            insert(Review)
            .values(comment=comment,
                    grade=grade,
                    product_id=product_id,
                    user_id=get_user["id"]
                    )
        )
        all_reviews = (await db.scalars(
            select(Review.grade)
            .where(Review.product_id == product_id)
        )).all()

        new_rating = sum(all_reviews) / len(all_reviews) if all_reviews else 0

        # 5. Update product's rating
        await db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(rating=new_rating)
        )
        await db.commit()

        return {'message': 'Review added successfully'}


@router.delete('/{review_id}')
async def delete_review(db: Annotated[AsyncSession, Depends(get_db)], review_id: int,
                        get_user: Annotated[dict, Depends(get_current_user)]):
    review = await db.scalar(select(Review).where(Review.id == review_id))
    if review.user_id != get_user['id'] and not get_user['is_admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not allowed to delete this review')

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Review not found')

    await db.execute(update(Review).where(Review.id == review_id).values(is_active=False))
    await db.commit()
    return {'message': 'Review deleted successfully'}
