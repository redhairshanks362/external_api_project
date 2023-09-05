# from django.shortcuts import render
#
# # Create your views here.
#
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from .models import Profile
# from .serializer import ProfileSerializer
# from .serializer import UserSerializer
#
#
#
# # class ProfileDetailView(generics.RetrieveAPIView):
# #     queryset = Profile.objects.all()
# #     serializer_class = UserSerializer
#
#
# # class ProfileDetailView(generics.RetrieveAPIView):
# #     queryset = Profile.objects.all()
# #     serializer_class = ProfileSerializer
# #     lookup_field = 'id'
# #
# #
# # class CreateProfileView(generics.CreateAPIView):
# #     queryset = Profile.objects.all()
# #     serializer_class = ProfileSerializer
# #
# #     def post(self, request, *args, **kwargs):
# #         serializer = ProfileSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # views.py
#
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Profile
# #from .serializers import ProfileSerializer
#
#
#
# #class ProfileDetailView(viewsets.ModelViewSet):
# class ProfileDetailView(APIView):
#     serializer_class = ProfileSerializer
#
#     def post(self, request, *args, **kwargs):
#         user_data = request.data.get('user', {})
#         user_serializer = UserSerializer(data=user_data)
#
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#
#             profile_data = request.data
#             profile_data['user'] = user.id
#             profile_serializer = ProfileSerializer(data=profile_data)
#
#             if profile_serializer.is_valid():
#                 profile_serializer.save()
#                 return Response({'message': 'Profile created successfully'}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data

#from .serializer import UserProfileSerializer, UserSerializer
from .models import UserProfile
#from .serializer import UserSerializer
from .serializer import CustomSerializer


@api_view(['POST'])
def create_user(request):
    print(request.data)
    #user = User.objects.filter(id=request.data['id'])
    user_id = request.data.get('id')  # Assuming you pass 'id' in the request data
    user = User.objects.filter(id=user_id).first()
    print('user', user)
    name = request.data.get('name')
    age = request.data.get('age')
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.name = name
    profile.age = age
    profile.save()
    serializer = CustomSerializer(user)
    #serializer = CustomSerializer(user,data=request.data)
    #try:
        #if serializer.is_valid():
            #user = serializer.save()
    return Response(serializer.data, status=201)
    #except serializers.ValidationError as e:
        #print(e.detail)
    return Response(serializer.errors, status=400)
#
#
# @api_view(['GET'])
# def get_user(request, user_id):
#      # user = get_object_or_404(User, id=user_id)
#      # serializer = UserProfileSerializer(user)
#      # return Response(serializer.data, status=200)
#      user = User.objects.filter(id=user_id).first()  # Fetch the User object
#      #serializer = UserSerializer(user)
#      serializer = CustomSerializer(user)
#      return Response(serializer.data)
#      # user_profile = get_object_or_404(UserProfile, user_id=user_id)
#      # age = user_profile.age
#      # name = user_profile.name
#      # return Response({'age': age, 'name':name})

@api_view(['GET'])
def user_profile(request, user_id):
    user = User.objects.filter(id=user_id).first()
    print('user', user)

    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomSerializer(user)
        return Response(serializer.data)

# @api_view(['GET'])
# def showall(request):
#     users = User.objects.all()
#
#     if users:
#         serializer = CustomSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'No users found'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def showall(request):
    users = User.objects.all()

    if users:
        serialized_users = []
        for user in users:
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                serializer = CustomSerializer(user)
                serialized_users.append(serializer.data)
        return Response(serialized_users, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No users found'}, status=status.HTTP_204_NO_CONTENT)



    # elif request.method == 'POST':
    #     serializer = CustomSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)