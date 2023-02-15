"""
Job queries

Query functions for job related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from .models import *


def create_job(payload: dict) -> Job:
    try:
        return Job.objects.get(id=payload["id"])
    except ObjectDoesNotExist:
        return None  # what to put here?


def get_all_job_ids() -> QuerySet:
    # should be based on a single user_id? (again, user or google id)
    # which version below should be used? Both seem quite similar and yet are different
    return Job.objects.all().values_list("id", "position_title", named=True)
    return Job.objects.all().values("id", "position_title")
