from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.models.review import Review, ReviewInfo, ReviewResponse
from app.services.review_service import ReviewService
from app.models.book import Book
from app.dependencies.services import get_review_service
from app.dependencies.db import get_db

router = APIRouter()

@router.get("/books/{book_id}/reviews", response_model=list[ReviewResponse])
def get_reviews(book_id: int, service: ReviewService = Depends(get_review_service)):
    reviews = service.get_reviews_by_book_id(book_id)
    if not reviews:
        raise HTTPException(status_code=404, detail=f"No reviews found for book {book_id}")
    return reviews

@router.post("/books/{book_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def add_review(book_id: int, review: ReviewInfo, service: ReviewService = Depends(get_review_service)):
    new_review = service.add_review(book_id, review)
    if not new_review:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return new_review


@router.put("/books/{book_id}/reviews/{review_id}", response_model=ReviewResponse)
def update_review(book_id: int, review_id: int, new_review: ReviewInfo, db: Session = Depends(get_db)):
    """
    Activity 2: Spot and fix a possible mistake in the below implementation.

    Update an existing review, given the book_id and the review_id.
    Ensure that the review is associated with the book.

    TODO: The current implementation checks if the book_id exists but does not verify
          that the review belongs to the specified book_id. Identify this issue and 
          modify the code to ensure that only a review associated with the given 
          book_id can be updated.
    """

    # Check if the book exists in the books table
    book_exists = db.query(Book).filter(Book.id == book_id).first()  # `Book` is used here
    if not book_exists:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

    # Find and update the review
    review = db.query(Review).filter(Review.id == review_id).first()  # Issue: Missing association check with book_id
    if not review:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} not found")

    # Update the review's content
    review.review = new_review.review
    db.commit()
    db.refresh(review)
    return review


@router.delete("/books/{book_id}/reviews/{review_id}")
def delete_review(book_id: int, review_id: int, service: ReviewService = Depends(get_review_service)):
    success = service.delete_review(book_id, review_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Review with id {review_id} for book {book_id} not found")
    return {"message": "Review deleted successfully"}
