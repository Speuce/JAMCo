from django.db import models
from account.models import User


class KanbanColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    column_number = models.IntegerField()

    def to_dict(self):
        return {"id": self.id, "name": self.name, "column_number": self.column_number}
