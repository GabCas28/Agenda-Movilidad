import json
from json.encoder import JSONEncoder
from django.db import models
from django.contrib.auth.models import User

class Changes(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    creation_date= models.DateField(auto_now_add=True)
    last_modified= models.DateTimeField(auto_now=True)
    old_state = models.JSONField(default=dict, blank=True, null=True)
    updates = models.JSONField(default=dict, blank=True, null=True)
    additions = models.JSONField(default=dict, blank=True, null=True)
    deletions = models.JSONField(default=dict, blank=True, null=True)
    
    @classmethod
    def create(cls, user,  old_state=dict(), updates=dict(), additions=dict(), deletions=dict()):

        changes = cls(user=user, old_state=old_state, updates=updates, additions=additions, deletions=deletions)
        return changes