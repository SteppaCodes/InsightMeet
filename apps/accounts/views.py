#django imports 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

#third party imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
#local imports
from .serializers import (
                        RegisterSerializer, 
                        VerifyOtpSerializer, 
                        ResendOtpSerializer,
                        LoginSerializer, 
                        UserSerializer, 
                        LogoutSerializer,
                        ResetPasswordSerializer, 
                        SetNewPasswordSerializer
                    )
from .email import SendMail
from . models import OneTimePassword, User
from apps.common.response import CustomResponses

tags = ["Auth"]


class RegisterUserView(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
            summary = "Register user",
            description="""
             This endpoint creates a new user & sends an otp to the user's email for verification
            """,
            tags=tags,
            request=RegisterSerializer,
            responses={"201": RegisterSerializer},
    )
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            SendMail.send_otp(user['email'])

            return CustomResponses.success(
                message=f"Hi {user['first_name']} thank you for signing up, please check your email for an otp",
                data=serializer.data,
                status_code=201
            )


class VerifyEmail(APIView):
    serializer_class = VerifyOtpSerializer

    @extend_schema(
            summary = "Verify Email",
            description="""
            This endpoint verifies a user's email.
            Note:
             - retreive the otp provided by user, add to request
             - The API verifies the otp and you get either a success or an error status
             - if error, resend email using the `resend-email` endpoint
            """,
            tags=tags,
            request=VerifyOtpSerializer,
            responses={"200": VerifyOtpSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_otp = serializer.data['otp']
        
        try:
            user_code_object = OneTimePassword.objects.get(code=user_otp)
            user = user_code_object.user

            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                SendMail.welcome(user.email)

                #Serialize the user model before passing it to the response
                serialized_user = UserSerializer(user).data
                return CustomResponses.success(
                    message="Email verified successfully",
                    data=serialized_user
                )
  
            return CustomResponses.success(message="Email already verified")
        except OneTimePassword.DoesNotExist:
            return CustomResponses.error(message="Code is invalid, please try again")
            


class ResendEmail(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
            summary = "Resend verification Email",
            description="""
            This endpoint resends verification email for cases where user link is invalid or expired
            To verify a user's email, after the email has been sent, call the `verify-email` endpoint and request for the otp sent to user
            
            """,
            tags=tags,
            request=ResendOtpSerializer,
            responses={"200": ResendOtpSerializer},
    )
    def post(self, request): 
 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            
            SendMail.send_otp(self, user.email)

            return CustomResponses.success(
                message="Verification email sent"
            )

        except User.DoesNotExist:
            return CustomResponses.error(message="User not found", status_code=404)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
            summary = "Login a user",
            description="""
             This endpoint logs in a user
             Note:
             - This endpoint validates user credentials and returns user information and most importantly, the access and refresh tokens
             - The accesss token is used to allow user to perform actions that requires user to be authenticated
             - The refresh token is used get a new access token when token expires
            """,
            tags=tags,
            request=LoginSerializer,
            responses={"200": LoginSerializer},
            examples=[
            OpenApiExample(
                name="Login User example",
                value={
                    "email": "steppaapitestuser@gmail.com",
                    "password": "testuser",
                },
                description="Example request for authenticating a user",
            )
        ],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return CustomResponses.success(
            message="Login successful",
            data=serializer.data
        )

class ResetPasswordRequestView(APIView):
    serializer_class = ResetPasswordSerializer

    @extend_schema(
            summary = "Request to Reset a user's password",
            description="""
                This endpoint sends a reset password email with link to reset password
                Note
                 - A link to reset password is sent to user, embedded in the link is an encoding of the user's id
                 and a token 
                 - The link calls the 'reset-password-confirm` endpoint
                """,
            tags=tags, 
            request=ResetPasswordSerializer,
            responses={"200": ResetPasswordSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        SendMail.resetpassword(request, email)
        return CustomResponses.success(message="An email with a link to reset your password has been sent to you")


class ResetPasswordConfirm(APIView):

    @extend_schema(
            summary = "Confirm passsword request",
            description="""
            This endpoint confirms a user's password reset link
            Note:
             - The link in the email calls this endpoint, you have to redirect to the page for user to set new password 
             if the response returned is success
             - If not success, allow user request link again or handle it in whichever way you see fit
            """,
            tags=tags
    )
    def get(self,request, uidb64, token):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(id=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                data = {
                    "token": token,
                    "uidb64": uidb64
                }

                return CustomResponses.success(
                    message="Credentials validated successfully",
                    data=data
                )
            return CustomResponses.error(message="Token is invalid or expired")
        
        except DjangoUnicodeDecodeError:
            return CustomResponses.error(message="User not found", status_code=404)


class SetNewPassswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    @extend_schema(
            summary = "Reset Password",
            description="""
            This endpoint changes the user's password
            Note: 
            - this is the final step in the password reset. User's password gets changed
            """,
            tags=tags
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)   

        return CustomResponses.success(message="Password reset successfully")

class LogoutUserView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary = "logout user",
            description="This endpoint logs out a user",
            tags=tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponses.success(message="Logged out successfully")
        