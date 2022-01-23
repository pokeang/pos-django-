from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status, exceptions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from .models import User
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserDetailsSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import generate_access_token, generate_refresh_token
from common.permissions import IsOnlySuperUser


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
    UserModel = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed('username and password required')

    user = UserModel.objects.filter(username=username).first()

    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserDetailsSerializer(user).data

    access_token = generate_access_token(serialized_user)
    refresh_token = generate_refresh_token(serialized_user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response


@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserDetailsSerializer(user).data
    return Response({'user': serialized_user})


@api_view(['POST'])
@ensure_csrf_cookie
# @permission_classes([AllowAny])
@permission_classes([IsOnlySuperUser])
def user_register(request):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        # user = User.objects.create_user(
        #     username=serializer['username'].value,
        #     password=serializer['password1'].value,
        #     email=serializer['email'].value,
        #     is_shop_manager=serializer['is_shop_manager'].value,
        #     store_id=serializer['store_id'].value,
        #     salary=serializer['salary'].value,
        #     birth_date=serializer['birth_date'].value,
        #     phone=serializer['phone'].value,
        #     fb_name=serializer['fb_name'].value,
        #     address=serializer['address'].value,
        #     profile_image=serializer['profile_image'].value
        # )
        user = serializer.save(request)
        created_serializer = UserDetailsSerializer(user)
        return Response(created_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOnlySuperUser])
def user_RUD(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response("User not found !", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            serializer = UserDetailsSerializer(user, data=request.data, read_only=False)
            if serializer.is_valid():
                data = request.data
                user.store_id = data['store_id']
                user.username = data['username']
                user.email = data['email']
                user.salary = data['salary']
                user.birth_date = data['birth_date']
                user.address = data['address']
                user.phone = data['phone']
                user.fb_name = data['fb_name']
                user.profile_image = data['profile_image']
                user.is_shop_manager = data['is_shop_manager']
                user.save()
                created_serializer = UserDetailsSerializer(user)
                return Response(created_serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response("User successfully delete")
    elif request.method == "GET":
        serializer = UserDetailsSerializer(user, many=False)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsOnlySuperUser])
def user_list(request):
    users = User.objects.all()
    serializer = UserDetailsSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def roles_list(request):
#     groups = Group.objects.all()
#     serializer = UserGroupSerializers(groups, many=True)
#     return Response(serializer.data)

