from django.db import models

# Create your models here.
class SendEmail(models.Model):
    email = models.EmailField(unique=True)
    code=models.CharField(max_length=4)
    create_date=models.DateField(auto_now_add=True)

    class Meta:
        db_table='email'

