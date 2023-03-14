"""
Job views

API-layer for job related operations.
"""
import logging
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from jamco.helper import read_request
from . import business

logger = logging.getLogger(__name__)


@require_POST
def get_minimum_jobs(request: HttpRequest):
    """
    Gets {id, position, company} for each job a given user has
    Called on Kanban Load
    Populates Kanban Cards with minimum overview thumbnail data per job
    """

    body = read_request(request)
    user_id = body.get("user_id")  # user whose jobs are needed

    logger.debug(f"get_minimum_jobs: {user_id}")

    try:
        jobs = list(business.get_minimum_jobs(user_id))
        return JsonResponse(status=200, data={"jobs": jobs})
    except Exception as err_msg:
        logger.error(err_msg)
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def get_job_by_id(request: HttpRequest):
    """
    Gets complete job object for user by id
    Called when job card is clicked on Kanban
    Populates JobDetailModal
    """

    body = read_request(request)
    user_id = body.get("user_id")
    job_id = body.get("job_id")

    logger.debug(f"get_job_by_id: user: {user_id}, job: {job_id}")

    try:
        job = business.get_job_by_id(user_id, job_id)

        return JsonResponse(status=200, data={"job_data": job.to_dict()})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def create_job(request: HttpRequest):
    """
    Creates job for user
    Returns job
    """

    body = read_request(request)
    logger.debug(f"create_job: {body}")

    try:
        job = business.create_job(body)
        return JsonResponse(status=200, data={"job": job.to_dict()})
    except KeyError as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def update_job(request: HttpRequest):
    """
    Updates user's job object
    """

    body = read_request(request)
    logger.debug(f"update_job: {body}")

    try:
        business.update_job(body)
        return JsonResponse(status=200, data={})
    except (ObjectDoesNotExist, AttributeError) as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def create_review_request(request: HttpRequest):
    """
    Creates a request for a cover letter review
    """

    body = read_request(request)
    logger.debug(f"create_review_request: {body}")

    try:
        review_request = business.create_review_request(body)
        return JsonResponse(status=200, data={"review_request": review_request.to_dict()})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def create_review(request: HttpRequest):
    """
    Creates a cover letter review
    """

    body = read_request(request)
    logger.debug(f"create_review: {body}")

    try:
        review = business.create_review(body)
        return JsonResponse(status=200, data={"review": review.to_dict()})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})


@require_POST
def get_reviews_for_user(request: HttpRequest):
    """
    Gets all the cover letter reviews that are addressed to a specific user
    """

    body = read_request(request)
    logger.debug(f"get_reviews_for_user: {body}")

    try:
        reviews = business.get_reviews_for_user(body)
        return JsonResponse(status=200, data={"reviews": [review.to_dict() for review in reviews]})
    except Exception as err_msg:
        return JsonResponse(status=400, data={"error": repr(err_msg)})
