from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.review import Review
from app.utils.gemini import review_with_gemini


def review_code(
    code: str,
    db: Session,
    user_id: int
):
    """
    Generate an AI review for the given code,
    save it to the database, and return the saved review.
    """

    # Validate input
    if not code.strip():
        raise ValueError("Code cannot be empty.")

    # Generate AI review
    ai_review = review_with_gemini(code)

    # Create Review object
    new_review = Review(
        code=code,
        review=ai_review,
        owner_id=user_id
    )

    # Save to database
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


def get_reviews(
    db: Session,
    user_id: int
):
    """
    Get all reviews created by the logged-in user.
    Returns the newest reviews first.
    """

    return (
        db.query(Review)
        .filter(Review.owner_id == user_id)
        .order_by(Review.created_at.desc())
        .all()
    )


def get_review_by_id(
    review_id: int,
    db: Session,
    user_id: int
):
    """
    Get a single review by ID.
    Only returns the review if it belongs to the logged-in user.
    """

    review = (
        db.query(Review)
        .filter(
            Review.id == review_id,
            Review.owner_id == user_id
        )
        .first()
    )

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found."
        )

    return review
def delete_review(
    review_id: int,
    db: Session,
    user_id: int
):
    """
    Delete a review that belongs to the logged-in user.
    """

    review = (
        db.query(Review)
        .filter(
            Review.id == review_id,
            Review.owner_id == user_id
        )
        .first()
    )

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found."
        )

    db.delete(review)
    db.commit()

    return {
        "message": "Review deleted successfully."
    }