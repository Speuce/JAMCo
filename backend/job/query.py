"""
Job queries

Query functions for job related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from .models import *


def create_job(payload: dict) -> Job:
    try:
        return Job.objects.get(id=payload["id"])
    except ObjectDoesNotExist:
        return None  # what to put here?


def get_all_jobs() -> list(Job):
    return None
