"""
Job business

Business logic for job related operations.
"""
from .models import Job
from . import query


def get_minimum_jobs(in_user: int) -> list[Job]:
    return query.get_minimum_jobs(in_user)


def get_job_by_id(in_user: int, job_id: int) -> Job:
    return query.get_job_by_id(in_user, job_id)


def create_job(payload: dict) -> Job:
    return query.create_job(payload)


def update_job(payload: dict) -> None:
    query.update_job(payload)
    return None
