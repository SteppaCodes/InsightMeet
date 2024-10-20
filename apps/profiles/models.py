from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.accounts.models import User


class Insightor(BaseModel): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    specialization = models.CharField(max_length=100)
    bio = models.TextField()
    country = models.CharField(max_length=300, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.full_name} - {self.title}'


class Education(BaseModel):
    insightor = models.ForeignKey(Insightor, on_delete=models.CASCADE)
    institution = models.CharField(max_length=300)
    degree = models.CharField(max_length=300)
    field_of_study = models.CharField(max_length=300, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()


class Certifications(BaseModel):
    insightor = models.ForeignKey(Insightor, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    issuing_organization = models.CharField(max_length=300)
    issue_date = models.DateField()


class Request(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(_("description"))
    terms_agreement = models.BooleanField(default=False)
    resume = models.FileField()
