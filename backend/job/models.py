from django.db import models
from account.models import User
from column.models import KanbanColumn


class Job(models.Model):
    kcolumn = models.ForeignKey(KanbanColumn, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_title = models.TextField()
    company = models.CharField(max_length=60)
    description = models.TextField(null=True)
    notes = models.TextField(null=True)
    cover_letter = models.TextField(null=True)
    deadlines = models.JSONField(encoder=None, null=True)
    type = models.TextField(null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "position_title": self.position_title,
            "company": self.company,
            "description": self.description,
            "notes": self.notes,
            "cover_letter": self.cover_letter,
            "kcolumn_id": self.kcolumn.id,
            "user_id": self.user.id,
            "deadlines": self.deadlines,
            "type": self.type,
        }


class ReviewRequest(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    fulfilled = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job.id,
            "reviewer_id": self.reviewer.id,
            "message": self.message,
            "fulfilled": self.fulfilled,
        }


class Review(models.Model):
    request = models.ForeignKey(ReviewRequest, on_delete=models.SET_NULL, null=True)
    response = models.TextField(blank=True)
    completed = models.DateTimeField(null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "response": self.response,
            "completed": self.completed.isoformat() if self.completed else None,
        }
