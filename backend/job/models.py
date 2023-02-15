from django.db import models
from account.models import KanbanColumn


class Job(models.Model):
    column_number = models.ForeignKey(KanbanColumn, on_delete=models.CASCADE)
    # User ForeignKey google_id or user_id ?
    position_title = models.TextField()
    company = models.CharField(max_length=60)
    description = models.TextField()
    notes = models.TextField()
    cover_letter = models.TextField()

    def to_dict(self):
        return {
            "id": self.id,
            "position_title": self.position_title,
            "company": self.company,
            "description": self.description,
            "notes": self.notes,
            "cover_letter": self.cover_letter,
        }


class Deadline(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    deadline_title = models.CharField(max_length=60)
    deadline_date = models.DateField(verbose_name="Deadline Date")

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "deadline_title": self.deadline_title,
            "deadline_date": self.deadline_date,
        }
