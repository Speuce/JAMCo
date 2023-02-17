"""
Job queries

Query functions for job related operations.
"""
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from .models import *

logger = logging.getLogger(__name__)


def create_job(payload: dict) -> Job:
    job = Job.objects.create(
        type=payload["type"] if payload.get("type") else None,
        kcolumn=KanbanColumn.objects.get(id=payload["kcolumn_id"]),
        user=User.objects.get(id=payload["user_id"]),
        position_title=payload["position_title"],
        company=payload["company"],
        description=payload["description"] if payload.get("description") else "",
        notes=payload["notes"] if payload.get("notes") else "",
        cover_letter=payload["cover_letter"] if payload.get("cover_letter") else "",
        deadlines=payload["deadlines"] if payload.get("cover_letter") else None,
    )
    logger.debug(f"Created Job: {job.to_dict()}")
    return job


def job_exists(job_id: str) -> bool:
    return Job.objects.filter(id=job_id).exists()


def update_job(payload: dict) -> None:
    # raise exception if update fails
    job = Job.objects.get(id=payload["id"])
    for key, value in payload.items():
        # If there are invalid keys in the payload (e.g. the frontend misspelled
        # the name of a field), raise an exception
        if hasattr(job, key):
            setattr(job, key, value)
        else:
            raise AttributeError("Job has no attribute " + key)

        # Since this is at the end of the func, it'll only execute if an exception
        # isn't raised. That is, we'll only save changes if the entire payload is
        # error-free.
        job.save()

def get_job_by_id(in_user: int, job_id: int) -> Job:
    try:
        return Job.objects.get(id=job_id, user__id=in_user)
    except:
        raise ObjectDoesNotExist("Job with that User does not exist")


def get_minimum_jobs(in_user: int) -> QuerySet:
    return (
        Job.objects.all()
        .filter(user__id=in_user)
        .values("id", "kcolumn", "position_title", "company", "type")
    )


def delete_job(in_user: int, job_id: int):
    Job.objects.get(id=job_id, user__id=in_user).delete()
