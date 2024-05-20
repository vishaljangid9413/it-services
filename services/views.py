from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import viewsets, permissions

from .serializers import*
from .models import *
from .forms import ServiceForm

import razorpay
import traceback
import environ
env = environ.Env()

# Create your views here.

@login_required
def home_page(request):
    service = request.GET.get('service', None)
    page = request.GET.get('page')
    if service is None:
        service_obj = Service.objects.all().order_by('-date')
        if not request.user.is_superuser:
            service_obj= service_obj.filter(is_active=True)
        paginator = Paginator(service_obj, 3) 
        page_obj = paginator.get_page(page)
        return render(request, 'home.html', {'page_obj':page_obj})
    else:
        service_obj = Service.objects.filter(name__icontains = service).order_by('-date')
        if not request.user.is_superuser:
            service_obj= service_obj.filter(is_active=True)
        data = [{
                'id':service_obj.id, 
                'name':service_obj.name, 
                'image':service_obj.image.url, 
                'price':service_obj.price, 
                'is_active':service_obj.is_active
                } for service_obj in service_obj]
        return JsonResponse({'page_obj':data})
    

@login_required
def subscription_page(request):
    page = request.GET.get('page')
    subscription_obj = Subscription.objects.filter(payment_status__in = ['success', 'failed']).order_by('-date')
    if not request.user.is_superuser:
        subscription_obj= subscription_obj.filter(user=request.user)
    paginator = Paginator(subscription_obj, 10) 
    page_obj = paginator.get_page(page)
    return render(request, 'subscription.html', {'page_obj':page_obj})


@login_required
def service_page(request, id):
    try:
        service_obj = Service.objects.get(id=id)
        if not request.user.is_superuser:
            service_obj = Service.objects.get(id=id,is_active=True)
        subscribed_obj = request.user.subscriptions.filter(service =service_obj)
        if subscribed_obj.exists():
            subscribed = True
        else:
            subscribed = False
        return render(request, 'service.html', {'service':service_obj, 'subscribed':subscribed})
    except Exception as e:
        print(str(e), traceback.format_exc())
        messages.error(request, "Invalid Service Request")
        return redirect('/')
                

@login_required
def create_service_page(request):
    if not request.user.is_superuser:
        messages.error(request, "Doesn't have Required Permission")
        return redirect('/')
    form = ServiceForm()
    return render(request, 'service_create.html', {'form':form})

    
@login_required
def service_create_form(request):
    name = request.POST.get('name')
    payment_terms = request.POST.get('payment_terms')
    price = request.POST.get('price')
    package = request.POST.get('package')
    tax = request.POST.get('tax')
    is_active = request.POST.get('is_active')
    try:
        if not request.user.is_superuser or request.method != 'POST':
            raise ValueError('Creation Failed')

        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            messages.success(request, "Service Created Successfully")
            return redirect("/")
        else:
            raise ValueError(form.errors)
    except Exception as e:
        messages.error(request, str(e))
        form = ServiceForm(initial={
            'name': name, 
            'payment_terms': payment_terms, 
            'price': price, 
            'package': package, 
            'tax':tax, 
            'is_active':is_active
            })
        return render(request, 'service_create.html', {'form':form})       


@login_required
def update_service_page(request, id):
    try:
        if not request.user.is_superuser:
            raise ValueError("Not allowed")
        obj = Service.objects.get(id=id)
        form = ServiceForm(initial={
            'name': obj.name, 
            'payment_terms': obj.payment_terms, 
            'price': obj.price, 
            'package': obj.package, 
            'tax':obj.tax, 
            'image':obj.image.url, 
            'is_active':obj.is_active
            })
        return render(request, 'update_service.html', {'form':form, 'service':id})
    except Exception as e:
        print(str(e), traceback.format_exc())
        messages.error(request, "Failed to Update Service")
        return redirect(f"/service/{id}/")

    
@login_required
def service_update_form(request, id):
    name = request.POST.get('name')
    payment_terms = request.POST.get('payment_terms')
    price = request.POST.get('price')
    package = request.POST.get('package')
    tax = request.POST.get('tax')
    is_active = request.POST.get('is_active')
    try:
        if not request.user.is_superuser or request.method != 'POST':
            raise ValueError('Updation Failed')
        service = Service.objects.get(id=id)

        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save(commit=False)
            messages.success(request, "Service updated Successfully")
            return redirect(f"/service/{id}/")
        else:
            raise ValueError(form.errors)
    except Exception as e:
        messages.error(request, str(e))
        form = ServiceForm(initial={
            'name': name, 
            'payment_terms': payment_terms, 
            'price': price, 
            'package': package, 
            'tax':tax, 
            'is_active':is_active
            })
        return render(request, 'update_service.html', {'form':form, 'service':id})
 

@login_required
def service_delete(request, id):
    try:
        if not request.user.is_superuser:
            raise ValueError("Permission Denied")
        Service.objects.get(id=id).delete()
        messages.success(request, "Service Deleted Successfully")
        return redirect("/")
    except Exception as e:
        print(str(e), traceback.format_exc())
        messages.error(request, "Service Deletion Failed")
        return redirect(f"/service/{id}/")
        
    
@login_required
def checkout_page(request, id):
    try:
        service_obj = Service.objects.filter(id=id).first()
        if not service_obj:
            raise ValueError("Can't find the service")
        verify_obj = Subscription.objects.filter(user = request.user, service = service_obj, payment_status="success").order_by('-date')
        if verify_obj.exists():
            messages.success(request, 'Service is already Subscribed')
            return redirect(f"/service/{id}/")

        amount_inc_tax = round((int(service_obj.price) + (int(service_obj.price) * float(service_obj.tax) / 100)))
        
        client = razorpay.Client(auth=(env('KEY'), env('SECRET_KEY')))
        if not client:
            raise ValueError("Error while creating client")

        order_data = { "amount": (amount_inc_tax * 100), "currency": "INR", "receipt": f"subscription_order_{service_obj.id}" }
        payment = client.order.create(data=order_data)
        if not payment:
            raise ValueError("Error while creating order")

        sub_obj, _ = Subscription.objects.get_or_create(
            user = request.user,
            service = service_obj,
            payment_status = "pending"
        )
        sub_obj.amount = amount_inc_tax
        sub_obj.razorpay_order_id = payment['id']
        sub_obj.save()

        data={
            'key':env('KEY'),
            'subscription':sub_obj,
            'payment':payment
        }
        return render(request, 'checkout.html', {'data':data})
    except Exception as e:
        print(str(e), traceback.format_exc())
        messages.error(request, 'Error in Service Checkout')
        return redirect(f"/service/{id}/")


@login_required
def thank_you_page(request):
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')

    sub_obj = Subscription.objects.filter(razorpay_order_id = razorpay_order_id).first()
    if not sub_obj:
        messages.error(request, 'Payment Failed, cannot find the required IDs')
        return redirect("/")
    try:
        data={}
        if razorpay_payment_id and razorpay_order_id and razorpay_signature:
            sub_obj.razorpay_payment_id = razorpay_payment_id
            sub_obj.razorpay_signature = razorpay_signature
            sub_obj.payment_status = "success"
            sub_obj.save()

            data["response"]="success"
        else:
            reason = request.GET.get('reason')
            description = request.GET.get('description')
            print("Payment failed:::", reason, description)
            sub_obj.payment_status = "failed"
            sub_obj.save()

            data["response"]="failed"
            data["reason"]=reason
        return render(request, 'thank_you.html', {'data':data})
    except Exception as e:
        print(str(e), traceback.format_exc())
        messages.error(request, str(E))
        return redirect("/")




# ** APIs **
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


