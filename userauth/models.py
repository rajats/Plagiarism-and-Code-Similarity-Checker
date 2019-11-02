from django.db import models
from django.contrib.auth.models import User

class RegUser(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	instructor = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.user)
