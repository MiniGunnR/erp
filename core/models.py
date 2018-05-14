from django.shortcuts import reverse
from django.db import models
from utils.models import Timestamped
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Company(models.Model):
    name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_1 = models.CharField(max_length=50, blank=True, null=True)
    phone_2 = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Designation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Floor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Line(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Shift(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{name}, {branch}".format(name=self.name, branch=self.branch)


class BaseProfile(Timestamped):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

    proximity_id = models.CharField(max_length=20, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    designation = models.ForeignKey(Designation, blank=True, null=True, on_delete=models.CASCADE)

    # photo = models.ImageField(upload_to=os.path.join(settings.BASE_DIR, 'media', 'user', 'photo'), blank=True, null=True)
    photo = models.ImageField(upload_to='user/photo/', blank=True, null=True)

    MALE = 1
    FEMALE = 2
    THIRD_GENDER = 3

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (THIRD_GENDER, 'Third Gender'),
    ]

    gender = models.SmallIntegerField(validators=[MaxValueValidator(3)], choices=GENDER_CHOICES, default=MALE)

    B_P = 1
    B_N = 2
    A_P = 3
    A_N = 4
    AB_P = 5
    AB_N = 6
    O_P = 7
    O_N = 8

    BLOOD_GROUP_CHOICES = (
        (B_P, 'B +ve'),
        (B_N, 'B -ve'),
        (A_P, 'A +ve'),
        (A_N, 'A -ve'),
        (AB_P, 'AB +ve'),
        (AB_N, 'AB -ve'),
        (O_P, 'O +ve'),
        (O_N, 'O -ve'),
    )

    blood_group = models.SmallIntegerField(choices=BLOOD_GROUP_CHOICES, default=B_P)

    ISLAM = 1
    HINDUISM = 2
    BUDDHISM = 3
    CHRISTIANITY = 4

    RELIGION_CHOICES = (
        (ISLAM, 'Islam'),
        (HINDUISM, 'Hinduism'),
        (BUDDHISM, 'Buddhism'),
        (CHRISTIANITY, 'Christianity'),
    )

    religion = models.SmallIntegerField(choices=RELIGION_CHOICES, default=ISLAM)
    nationality = models.CharField(max_length=20, default='Bangladeshi')

    married = models.BooleanField(default=False)
    children = models.SmallIntegerField(default=0, blank=True, null=True)

    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    phone_1 = models.CharField(max_length=50, blank=True, null=True)
    phone_2 = models.CharField(max_length=50, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    national_id_new = models.CharField(max_length=20, blank=True, null=True)

    nominee = models.CharField(max_length=50, blank=True, null=True)
    nominee_address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    nominee_address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    nominee_phone_1 = models.CharField(max_length=50, blank=True, null=True)
    nominee_phone_2 = models.CharField(max_length=50, blank=True, null=True)
    nominee_national_id = models.CharField(max_length=20, blank=True, null=True)
    nominee_national_id_new = models.CharField(max_length=20, blank=True, null=True)

    spouse = models.CharField(max_length=50, blank=True, null=True)
    spouses_contact = models.CharField(max_length=50, blank=True, null=True)

    fathers_name = models.CharField(max_length=50, blank=True, null=True)
    fathers_contact = models.CharField(max_length=50, blank=True, null=True)
    mothers_name = models.CharField(max_length=50, blank=True, null=True)
    mothers_contact = models.CharField(max_length=50, blank=True, null=True)

    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, blank=True, null=True, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, blank=True, null=True, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, blank=True, null=True, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AccountsProfile(models.Model):
    bank = models.ForeignKey(Bank, blank=True, null=True, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, blank=True, null=True)

    basic_salary = models.IntegerField(blank=True, null=True)
    house_rent = models.IntegerField(blank=True, null=True)
    medical = models.IntegerField(blank=True, null=True)
    travelling  = models.IntegerField(blank=True, null=True)
    food= models.IntegerField(blank=True, null=True)
    gross_salary = models.IntegerField(blank=True, null=True)
    provident_fund = models.FloatField(blank=True, null=True)

    updated_by_accounts = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ITProfile(models.Model):
    sip = models.CharField(max_length=10, blank=True, null=True)

    updated_by_it = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Profile(BaseProfile, AccountsProfile, ITProfile):

    def __str__(self):
        return "{user}'s Profile".format(user=self.user.username)

    def save(self, *args, **kwargs):
        if not self.proximity_id:
            self.proximity_id = '0'
        self.proximity_id = ('0' * (10 - len(self.proximity_id))) + self.proximity_id
        super(Profile, self).save(*args, **kwargs)


class Mail(Timestamped):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    to_email = models.EmailField()
    from_email = models.EmailField()
    cc_emails = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, default='From Design Ace Limited')
    body = models.TextField(default='')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "{content_type} : {to_email} - {subject}".format(content_type=self.content_type, to_email=self.to_email, subject=self.subject[:50])

    def get_absolute_url(self):
        return reverse('europarts:{}_details'.format(self.content_type), args=[str(self.object_id)])