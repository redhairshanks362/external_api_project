# from django.db import models
#
# # Create your models here.
#
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     age = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.name
#
# class BasicAuthentication(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     age = models.IntegerField()

# # from rest_framework import serializers
# # from django.contrib.auth.models import User
# # from .models import Profile
# #
# #
# #
# # class UserSerializer(serializers.ModelSerializer):
# #     # username = serializers.ReadOnlyField(source='user.username')
# #     # email = serializers.ReadOnlyField(source='user.email')
# #
# #     class Meta:
# #         model = User
# #         fields = ['id', 'username', 'password']
# #
# #
# # class ProfileSerializer(serializers.ModelSerializer):
# #     user = UserSerializer(read_only=True)
# #     class Meta:
# #         model = Profile
# #         fields = ['id','user','name','age']
# #
# #     # def create(self, validated_data):
# #     #     user_data = validated_data.pop('username')
# #     #     user = User.objects.create_user(**user_data)  # Use create_user to create a User object
# #     #     profile = Profile.objects.create(user=user, **validated_data)
# #     #     return profile
#
#
# from rest_framework import serializers, fields
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from rest_framework.authentication import BasicAuthentication
# from .models import BasicAuthentication, UserProfile
#
# from user.models import Profile
#
#
# # Serializers
# class BasicAuthenticationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BasicAuthentication
#         fields = ['username', 'password']
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['name', 'age']
#
#
# class UserSerializer(serializers.ModelSerializer):
#     basic_authentication = BasicAuthenticationSerializer()
#     user_profile = UserProfileSerializer()
#
#     class Meta:
#         model = UserProfile
#         fields = ['user', 'email', 'basic_authentication', 'user_profile']

from django.db import models
from django.contrib.auth.models import User


# class BasicAuthentication(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)

from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    age = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.age} years old)"

#This code is for signal I have transferred it to signals.py
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# class CustomModel(models.Model):
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     email = models.EmailField()
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField()
#     name = models.CharField(max_length=255)
#     age = models.IntegerField()
#
#     def __str__(self):
#         return self.username


