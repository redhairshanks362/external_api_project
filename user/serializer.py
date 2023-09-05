# # # from rest_framework import serializers
# # # from django.contrib.auth.models import User
# # # from .models import Profile
# # #
# # #
# # #
# # # class UserSerializer(serializers.ModelSerializer):
# # #     # username = serializers.ReadOnlyField(source='user.username')
# # #     # email = serializers.ReadOnlyField(source='user.email')
# # #
# # #     class Meta:
# # #         model = User
# # #         fields = ['id', 'username', 'password']
# # #
# # #
# # # class ProfileSerializer(serializers.ModelSerializer):
# # #     user = UserSerializer(read_only=True)
# # #     class Meta:
# # #         model = Profile
# # #         fields = ['id','user','name','age']
# # #
# # #     # def create(self, validated_data):
# # #     #     user_data = validated_data.pop('username')
# # #     #     user = User.objects.create_user(**user_data)  # Use create_user to create a User object
# # #     #     profile = Profile.objects.create(user=user, **validated_data)
# # #     #     return profile
# #
# #
# # from rest_framework import serializers, fields
# # from django.contrib.auth.models import User
# # from django.shortcuts import get_object_or_404
# # from django.http import JsonResponse
# # from rest_framework.authentication import BasicAuthentication
# # from .models import BasicAuthentication, UserProfile
# #
# # from user.models import Profile
# #
# #
# # # Serializers
# # class BasicAuthenticationSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = BasicAuthentication
# #         fields = ['username', 'password']
# #
# #
# # class UserProfileSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Profile
# #         fields = ['name', 'age']
# #
# #
# # class UserSerializer(serializers.ModelSerializer):
# #     basic_authentication = BasicAuthenticationSerializer()
# #     user_profile = UserProfileSerializer()
# #
# #     class Meta:
# #         model = UserProfile
# #         fields = ['user', 'email', 'basic_authentication', 'user_profile']
#
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class BasicAuthentication(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     age = models.IntegerField()


# from rest_framework import serializers
# from django.contrib.auth.models import User
#
# from user.models import BasicAuthentication, UserProfile
#
#
# class BasicAuthenticationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BasicAuthentication
#         fields = ['username', 'password']
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['name', 'age']
#
# class UserSerializer(serializers.ModelSerializer):
#     basic_authentication = BasicAuthenticationSerializer()
#     user_profile = UserProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'basic_authentication', 'user_profile']

from rest_framework import serializers
from django.contrib.auth.models import User


# from user.models import BasicAuthentication, UserProfile


# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = '__all__'
            # ['username', 'password', 'name', 'age']

from rest_framework import serializers
from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     age = serializers.SerializerMethodField()
#
#     class Meta:
#
#         model = User
#         fields = '__all__'
#         # fields = ['first_name','age']
#
#     def get_age(self , obj):
#         return obj.age
#
#     def get_name(self,obj):
#         return obj.name

from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'age']


# class UserSerializer(serializers.ModelSerializer):
#     #name = serializers.SerializerMethodField()
#     #age = serializers.SerializerMethodField()
#     userprofile = UserProfileSerializer(source='userprofile_set.first', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password', 'email', 'is_staff', 'is_active', 'date_joined', 'userprofile']


class CustomSerializer(serializers.ModelSerializer):
    #name = serializers.CharField(source='userprofile.name')
    #age = serializers.IntegerField(source='userprofile.age')
    name = serializers.SerializerMethodField('get_name')
    age = serializers.SerializerMethodField('get_age')
    #userprofile = UserProfileSerializer(source='userprofile_set.first', read_only=True)
    # name = serializers.CharField(source='userprofile.name')
    # age = serializers.IntegerField(source='userprofile.age')

    class Meta:
        model = User
        fields = '__all__'

    def get_age(self , obj):
        profile = UserProfile.objects.filter(user=obj).first()
        return profile.age

    def get_name(self,obj):
        profile = UserProfile.objects.filter(user=obj).first()
        return profile.name










