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
    # TODO
    # raise exception if update fails
    pass

def get_job_by_id(user_id: int, job_id: int) -> Job:
    # TODO
    return None


def get_minimum_jobs(user_id: int) -> QuerySet:
    # should be based on a single user_id (user.id)
    # return {id, position, company} for all user's jobs

    # Jared - I don't think it really matters which of values or values_list we use
    # can likely easily switch if we need

    # which version below should be used? Both seem quite similar and yet are different
    return Job.objects.all().values_list("id", "position_title", "company", named=True)
    return Job.objects.all().values("id", "position_title", "company")
