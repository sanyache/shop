# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StProfile(models.Model):
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name= u"Профіль користувача"

    mobile_phone = models.CharField(
        max_length= 12,
        blank= True,
        verbose_name= u"Мобільний телефон",
        default=''
    )

    def __unicode__(self):
        return self.user.username