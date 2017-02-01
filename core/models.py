import os
from django.db import models
from utils.models import Timestamped
from django.conf import settings
from django.core.validators import MaxValueValidator


# class Company(models.Model):
#     name = models.CharField(max_length=100)
#     address_line_1 = models.CharField(max_length=100)
#     address_line_2 = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_1 = models.CharField(max_length=50)
#     phone_2 = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


# class Designation(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Section(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Building(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Floor(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Line(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Shift(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Bank(models.Model):
#     name = models.CharField(max_length=100)
#     branch = models.CharField(max_length=50)
#     address_line_1 = models.CharField(max_length=100, blank=True, null=True)
#     address_line_2 = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return "{name}, {branch}".format(name=self.name, branch=self.branch)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    # company = models.ForeignKey(Company)
    #
    # proximity_id = models.CharField(max_length=20, blank=True, null=True)
    # joining_date = models.DateField()
    # designation = models.ForeignKey(Designation, blank=True, null=True)
    #
    # address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    # address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    # phone_1 = models.CharField(max_length=50, blank=True, null=True)
    # phone_2 = models.CharField(max_length=50, blank=True, null=True)
    #
    # date_of_birth = models.DateField()
    # national_id = models.CharField(max_length=20, blank=True, null=True)
    # national_id_new = models.CharField(max_length=20, blank=True, null=True)
    #
    # B_P = 1
    # B_N = 2
    # A_P = 3
    # A_N = 4
    # AB_P = 5
    # AB_N = 6
    # O_P = 7
    # O_N = 8
    #
    # BLOOD_GROUP_CHOICES = (
    #     (B_P, 'B +ve'),
    #     (B_N, 'B -ve'),
    #     (A_P, 'A +ve'),
    #     (A_N, 'A -ve'),
    #     (AB_P, 'AB +ve'),
    #     (AB_N, 'AB -ve'),
    #     (O_P, 'O +ve'),
    #     (O_N, 'O -ve'),
    # )
    #
    # blood_group = models.CharField(max_length=2, choices=BLOOD_GROUP_CHOICES, default=B_P)
    #
    # MALE = 1
    # FEMALE = 2
    # THIRD_GENDER = 3
    #
    # GENDER_CHOICES = (
    #     (MALE, 'Male'),
    #     (FEMALE, 'Female'),
    #     (THIRD_GENDER, 'Third Gender'),
    # )
    #
    # gender = models.SmallIntegerField(validators=MaxValueValidator(3), choices=GENDER_CHOICES, default=MALE)
    #
    # married = models.BooleanField(default=False, blank=True, null=True)
    # children = models.SmallIntegerField(default=0, blank=True, null=True)
    #
    # ISLAM = 1
    # HINDUISM = 2
    # BUDDHISM = 3
    # CHRISTIANITY = 4
    #
    # RELIGION_CHOICES = (
    #     (ISLAM, 'Islam'),
    #     (HINDUISM, 'Hinduism'),
    #     (BUDDHISM, 'Buddhism'),
    #     (CHRISTIANITY, 'Christianity'),
    # )
    #
    # religion = models.SmallIntegerField(choices=RELIGION_CHOICES, default=ISLAM)
    # nationality = models.CharField(max_length=20, default='Bangladeshi')
    #
    # nominee = models.CharField(max_length=50)
    # nominee_address_line_1 = models.CharField(max_length=100)
    # nominee_address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    # nominee_phone_1 = models.CharField(max_length=50)
    # nominee_phone_2 = models.CharField(max_length=50, blank=True, null=True)
    # nominee_national_id = models.CharField(max_length=20, blank=True, null=True)
    # nominee_national_id_new = models.CharField(max_length=20, blank=True, null=True)
    #
    # spouse = models.CharField(max_length=50, blank=True, null=True)
    #
    # fathers_name = models.CharField(max_length=50)
    # fathers_contact = models.CharField(max_length=50, blank=True, null=True)
    # mothers_name = models.CharField(max_length=50)
    # mothers_contact = models.CharField(max_length=50, blank=True, null=True)
    #
    # department = models.ForeignKey(Department, blank=True, null=True)
    # section = models.ForeignKey(Section, blank=True, null=True)
    # building = models.ForeignKey(Building, blank=True, null=True)
    # floor = models.ForeignKey(Floor, blank=True, null=True)
    # line = models.ForeignKey(Line, blank=True, null=True)
    # shift = models.ForeignKey(Shift, blank=True, null=True)
    #
    # bank = models.ForeignKey(Bank, blank=True, null=True)
    # account_number = models.CharField(max_length=50, blank=True, null=True)
    #
    # basic_salary = models.IntegerField(blank=True, null=True)
    # house_rent = models.IntegerField(blank=True, null=True)
    # medical = models.IntegerField(blank=True, null=True)
    # travelling  = models.IntegerField(blank=True, null=True)
    # food_= models.IntegerField(blank=True, null=True)
    # gross_salary = models.IntegerField(blank=True, null=True)
    # provident_fund = models.FloatField(blank=True, null=True)

    sip = models.CharField(max_length=10, blank=True, null=True)

    # photo = models.ImageField(upload_to=os.path.join(settings.BASE_DIR, 'media', 'user', 'photo'), blank=True, null=True)

    def __str__(self):
        return "{user}'s Profile".format(user=self.user.get_full_name())

