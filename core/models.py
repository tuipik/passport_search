from django.db import models


class DocumentType(models.Model):
    title = models.CharField(max_length=255)
    has_expiration_date = models.BooleanField(default=False)
    has_series = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class LostPassport(models.Model):
    descriptor = models.CharField(max_length=255)
    document_series = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    theft_date = models.DateField(blank=True)
    insert_date = models.DateField(blank=True)
    ovd = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.document_series} {self.document_number}'







