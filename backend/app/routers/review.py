from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.review_schema import (
    CodeReviewRequest,
    CodeReviewResponse,
)
from app.services.review_service import (
    review_code,
    get_reviews,
    get_review_by_id,
    delete_review,
)
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/review",
    tags=["AI Review"],
)


@router.post(
    "/",
    response_model=CodeReviewResponse
)
def review_python_code(
    request: CodeReviewRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Generate an AI review for the submitted code,
    save it to the database, and return the saved review.
    """

    return review_code(
        code=request.code,
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/",
    response_model=List[CodeReviewResponse]
)
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get all reviews created by the logged-in user.
    """

    return get_reviews(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/{review_id}",
    response_model=CodeReviewResponse
)
def get_single_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get a single review by its ID.
    Only the owner can access it.
    """

    return get_review_by_id(
        review_id=review_id,
        db=db,
        user_id=current_user.id
    )


@router.delete("/{review_id}")
def delete_user_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Delete a review.
    Only the owner can delete it.
    """

    return delete_review(
        review_id=review_id,
        db=db,
        user_id=current_user.id
    )