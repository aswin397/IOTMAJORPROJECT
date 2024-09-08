from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Admin.models import *
# Create your views here.


def home(request):
    return render(request,"Admin/home.html")

@csrf_exempt
def Addoffice(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            location = request.POST.get('location')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email', None)
            office_code = request.POST.get('office_code')
            password = request.POST.get('password')
            
            # Create KSEBOffice object and save to the database
            new_office = KSEBOffice.objects.create(
                name=name,
                location=location,
                phone_number=phone_number,
                email=email,
                office_code=office_code,
                password=password
            )
            data={"data":'Admin:Addoffice'}
            return render(request,"Admin/savedpage.html",data)
        except Exception as e:
            print(e)
            data={"data":'Admin:Addoffice'}
            return render(request,"Admin/failed_page.html",data)
    return render(request,"Admin/Addoffice.html")

def Viewusers(request):
    ob=ElectricityConsumer.objects.all()
    return render(request,"Admin/Viewusers.html",{"consumers":ob})

def Payments(request):
    Bills = Bill.objects.all()
    return render(request,"Admin/Payments1.html",{"bills":Bills})
@csrf_exempt
def Feedback1(request):

    if request.method == 'POST':
        try:
        
            message = request.POST.get('msg')
            
            user_id=ElectricityConsumer.objects.get(id=request.POST.get('user'))
            
            authority=1
            direction=1
            
            feedback = Feedback(user=user_id, authority=authority, msg=message, view_sts=0, direction=direction)
            feedback.save()
        except Exception as e:
            pass

            
        return redirect('Admin:Feedback')
    
    
    
    received_messages_to_update = Feedback.objects.filter(authority=1, direction=2)
    received_messages_to_update.update(view_sts=1)
    received_messages = Feedback.objects.filter(authority=1).order_by('-id')
    return render(request,"Admin/Feedback.html",{"data":received_messages})


@csrf_exempt
def viewoffice(request):
    offices = KSEBOffice.objects.all()
    return render(request, 'Admin/viewoffice.html', {'offices': offices})    