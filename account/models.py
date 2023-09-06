from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
        ]


class Address(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="addresses"
    )
    local_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["user", "local_address"]),
        ]


class Profession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="professions")
    profession = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(fields=["user", "profession"]),
        ]


class Certifications(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="certifications"
    )
    certificate_name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["user", "certificate_name"]),
        ]
