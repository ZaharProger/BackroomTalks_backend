from django.db import models


class Chat(models.Model):
    code = models.BinaryField(max_length=64)
