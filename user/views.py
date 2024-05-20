from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token

from utils.otp_handler import OTPHandler
import traceback
from .models import User
from .forms import RegistrationForm
from .serializers import UserSerializer
import environ
env = environ.Env()



def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')


def register_page(request):
    form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def registeration_form(request):
    otp = request.POST.get('otp')
    fullname = request.POST.get('fullname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    address = request.POST.get('address')
    password = request.POST.get('password')
    try:
        if request.method != 'POST':
            raise ValueError("Only POST Method Allowed")

        # Check if user exists with same phone number
        user = User.objects.filter(mobile=mobile).first()
        if user:
            messages.success(request, "You're already a registered User. Please sign-in. ")
            return redirect('/login/')

        # verify otp 
        OTPHandler.verifyOTP(email, "registration", otp)
        
        # Create new user
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
        else:
            raise ValueError(form.errors)

        messages.success(request, 'Form Registeration Successfull')
        return redirect('/login/')
    except Exception as e:
        print(traceback.format_exc())

        messages.error(request, str(e))
        form = RegistrationForm(initial={'fullname': fullname, 'email': email, 'mobile': mobile, 'address': address, 'password':password})
        return render(request, 'register.html', {'form': form})


def login_form(request):
    mobile = request.POST.get('mobile')
    password = request.POST.get('password')
    try:
        if request.method != 'POST':
            raise ValueError("Only POST Method Allowed")
        
        user = User.objects.filter(mobile=mobile).first()
        if not user:
            raise ValueError("User Not Found")
        
        if not user.check_password(password):
            raise ValueError('Invalid user & password combination')
        
        auth = authenticate(mobile=mobile, password=password) 
        if auth is None:
            raise ValueError("Authentication Failed")
        login(request, user)
        return redirect('/')
    except Exception as e:
        print(traceback.format_exc())

        messages.error(request, str(e))
        return render(request, 'login.html', {'mobile': mobile})


def logout(request):
    auth_logout(request)
    return redirect("/login/")


# ** APIs **

class GetOTP(APIView):
    
    def post(self, request):   
        # can be accessed from ajax or postman 
        email = request.POST.get("email") or request.data.get("email")
        print("email::", email)
        try:            
            otp = OTPHandler.generate_otp(email) 
            print("OTP: ",otp)
            return Response(otp, status=status.HTTP_200_OK)       
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    def post(self, request):
        data = request.data
        print(data.get('email'), "registration", data.get('otp'))
        try:
            OTPHandler.verifyOTP(data.get('email'), data.get('otp'))
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data = data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data 
        mobile = data.get('mobile')
        password = data.get('password')
        try:            
            user = User.objects.filter(mobile = mobile).first()
            pass_check = user.check_password(password)
            auth = authenticate(request, mobile=mobile, password=password)              
            print(user,pass_check, auth)
            if not (user or pass_check) or auth is None:
                raise ValueError('Invalid user & password combination')

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except Exception as e:
            print(traceback.format_exc())
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class ForgetPasswordView(APIView):

    def post(self, request):
        data = request.data 
        mobile = data.get('mobile')
        password = data.get('password')
        try:
            user = User.objects.filter(mobile = mobile).first()
            if not user:
                raise ValueError("User not found")
            elif user.check_password(password):
                raise ValueError('Password must not be same as Old Password')

            OTPHandler.verifyOTP(user.email, data.get('otp'))

            user.set_password(password) 
            user.save()

            return Response({'Success': "Password Updated Successfully"})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)        
        token.delete()                
        # request.session.flush()
        return Response({'success': 'Logout successful'})   
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_superuser and user != request.user:
            return Response({'error': 'Permission Denied'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(user, data=request.data, partial=kwargs.get('partial', False))
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

