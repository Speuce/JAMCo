from django.db import models
from account.models import KanbanColumn, User

# class Deadline(models.Model):
#     title = models.CharField(max_length=60)
#     date = models.DateField(verbose_name="Deadline Date")

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "date": self.date,
#         }

class Job(models.Model):
    column_id = models.ForeignKey(KanbanColumn, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    position_title = models.TextField()
    company = models.CharField(max_length=60)
    description = models.TextField()
    notes = models.TextField()
    cover_letter = models.TextField()
    deadlines = models.JSONField(encoder=None)

    def to_dict(self):
        return {
            "id": self.id,
            "position_title": self.position_title,
            "company": self.company,
            "description": self.description,
            "notes": self.notes,
            "cover_letter": self.cover_letter,
            "column_id": self.column_id,
            "deadlines": self.deadlines
        }
