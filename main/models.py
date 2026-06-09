from django.db import models


class Member(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    LANGUAGE_CHOICES = (
        ("mr", "Marathi"),
        ("en", "English"),
    )

    full_name = models.CharField(max_length=255)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES
    )

    education = models.CharField(
        max_length=255,
        blank=True
    )

    birth_date = models.DateField()

    age = models.PositiveIntegerField()

    height = models.CharField(
        max_length=50,
        blank=True
    )

    complexion = models.CharField(
        max_length=100,
        blank=True
    )

    occupation = models.CharField(
        max_length=255,
        blank=True
    )

    annual_income = models.CharField(
        max_length=100,
        blank=True
    )

    mobile = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    address = models.TextField()

    native_place = models.CharField(
        max_length=255,
        blank=True
    )

    father_name = models.CharField(
        max_length=255,
        blank=True
    )

    father_occupation = models.CharField(
        max_length=255,
        blank=True
    )

    mother_name = models.CharField(
        max_length=255,
        blank=True
    )

    caste = models.CharField(
        max_length=100,
        default="Matang"
    )

    sub_caste = models.CharField(
        max_length=100,
        blank=True
    )

    gotra = models.CharField(
        max_length=100,
        blank=True
    )

    expectations = models.TextField(
        blank=True
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default="mr"
    )

    photo = models.ImageField(
        upload_to="members/",
        blank=True,
        null=True
    )
    blood_group = models.CharField(
    max_length=20,
    blank=True
    )

    brothers = models.PositiveIntegerField(
        default=0
    )

    sisters = models.PositiveIntegerField(
        default=0
    )

    relative_info = models.TextField(
        blank=True
    )

    surname = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.full_name