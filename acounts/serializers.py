from rest_framework import serializers
from acounts.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str,force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from acounts.utils import EmailUtils


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ['email', 'dob', 'name', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'dob': {'required': True},
            'name': {'required': True},
            'tc': {'required': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password and Confirm Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):  
    email = serializers.EmailField(required=True, max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password',]
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        if not user.is_active:
            raise serializers.ValidationError({"email": "This account is inactive."})

        attrs['user'] = user  
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'dob','phone_number', 'name', 'tc', 'user_profile']
        extra_kwargs = {
            'email': {'read_only': True},
            'dob': {'required': True},
            'name': {'required': True},
            'tc': {'required': False},
            'phone_number': {'required': True},
            'user_profile': {'required': False},
        }
    def update(self, instance, validated_data):
        instance.dob = validated_data.get('dob', instance.dob)
        instance.name = validated_data.get('name', getattr(instance, 'name', None))
        instance.phone_number = validated_data.get('phone_number', getattr(instance, 'phone_number', None))
        instance.tc = validated_data.get('tc', instance.tc)
        user_profile = validated_data.get('user_profile')
        if user_profile:
            instance.user_profile = user_profile
        instance.save()
        return instance 
    
class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['old_password','password','password2']
        extra_kwargs = {
            'password': {'write_only': True,'required':True,'style': {'input_type': 'password'}},
        }

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Password and Confirm Password fields didn't match."})
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('old_password', None)
        validated_data.pop('password2', None)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        if not User.objects.get(email=email).is_active:
            raise serializers.ValidationError({"email": "This account is inactive."})
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("token for reset password ",token)
            link  = f"http://localhost:8000/api/reset-password-confirm/{uid}/{token}/"
            print("link",link)
            ###### send Email code here ######
            data={
                'subject': 'Password Reset',
                'message': f'Click the link to reset your password: {link}',
                'to': user.email
            }
            EmailUtils.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
    
class SetResetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID."})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"token": "Token is invalid or expired."})

        self.context['user'] = user  # Pass user for use in `save`
        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        user = self.context.get('user')
        user.set_password(password)
        user.save()
        return user

    

   