"""
Job business

Business logic for job related operations.
"""
from .models import Job
from . import query

def get_minimum_jobs(user_id: int) -> list[Job]:
    return query.get_minimum_jobs(user_id)

def get_job_by_id(user_id: int, job_id: int) -> Job:
    return query.get_job_by_id(user_id, job_id)

def create_job(payload: dict) -> Job:
    return query.create_job(payload)

def update_job(payload: dict) -> None:
    # need to handle updating deadlines array with Deadline objects
    query.update_job(payload)
    return None
