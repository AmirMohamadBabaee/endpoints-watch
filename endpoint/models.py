from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model


# Create your models here.
class Timestampable(models.Model):
    """
    Abstract Class to add record creation and modification time of objects
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    class Meta:
        abstract = True


class SoftDeletes(models.Model):
    """
    Abstract Class to define deletion time of objects
    """

    deleted_at = models.DateTimeField(null=True)    
    
    class Meta:
        abstract = True


class Endpoint(Timestampable, SoftDeletes, models.Model):
    
    user        = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    endpoint    = models.URLField()
    threshold   = models.PositiveIntegerField()
    fail_times  = models.PositiveIntegerField(default=0, editable=False)

    def get_fail_times(self):
        fail_counter = self.request_set.filter(Q(result__lt=200) | Q(result__gte=300)).count()
        self.fail_times = fail_counter
        self.save()
        return fail_counter

    class Meta:
        unique_together = ('user', 'endpoint',)


class Request(Timestampable, SoftDeletes, models.Model):

    endpoint    = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    result      = models.SmallIntegerField()

    def get_endpoint(self):
        return self.endpoint.endpoint
