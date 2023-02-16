"""
Job queries

Query functions for job related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from .models import *


def create_job(payload: dict) -> Job:
    # need to return Job.objects.create(x,y,z)
    try:
        return Job.objects.get(id=payload["id"])
    except ObjectDoesNotExist:
        return None  # what to put here?


def update_job(payload: dict) -> None:
    # raise exception if update fails
    pass


def get_job_by_id(in_user_id: int, job_id: int) -> Job:
    return Job.objects.get(user_id=in_user_id, id=job_id)


def get_minimum_jobs(in_user_id: int) -> QuerySet:
    # should be based on a single user_id (user.id)
    # return {id, position, company} for all user's jobs

    return (
        Job.objects.all()
        .filter(user_id=in_user_id)
        .values("id", "position_title", "company")
    )
