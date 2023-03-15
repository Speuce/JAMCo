"""
Job business

Business logic for job related operations.
"""
from .models import Job, ReviewRequest, Review
from . import query


def get_minimum_jobs(in_user: int) -> list[Job]:
    return query.get_minimum_jobs(in_user)


def get_job_by_id(in_user: int, job_id: int) -> Job:
    return query.get_job_by_id(in_user, job_id)


def create_job(payload: dict) -> Job:
    return query.create_job(payload)


def update_job(payload: dict) -> None:
    query.update_job(payload)


def create_review_request(payload: dict) -> ReviewRequest:
    return query.create_review_request(payload)


def get_review_requests_for_user(payload: dict) -> ReviewRequest:
    return query.create_review_request(payload)


def create_review(payload: dict) -> Review:
    return query.create_review(payload)


def get_reviews_for_user(payload: dict) -> list[Review]:
    return query.get_reviews_for_user(payload)
