from django.shortcuts import render
from Admin.models import *
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.
 
def home(request):
    consumer = request.session['id']
    consumer=ElectricityConsumer.objects.get(id=consumer)
    ob=Annoucement.objects.filter(office=consumer.office_id)
    if ob!=None:
        return render(request,"User/home.html",{"data":ob})
    return render(request,"User/home.html")


def myprofile(request):

    if request.method == 'POST':
        
        consumer = request.session['id']
        consumer=ElectricityConsumer.objects.get(id=consumer)
        # Update profile fields with the submitted form data
        consumer.name = request.POST.get('name')
        consumer.address = request.POST.get('address')
        
        consumer.phone_number = request.POST.get('phone_number')
        consumer.email = request.POST.get('email')
        
        consumer.save()

        
        return redirect('User:myprofile')

    else:
        
        consumer = request.session['id']
        consumer=ElectricityConsumer.objects.get(id=consumer)

        return render(request, 'User/myprofile.html', {'consumer': consumer})


    return render(request,"User/myprofile.html")


#### feedback

def feedback(request):
    if request.method == 'POST':
        user_id = request.session['id']
        message = request.POST.get('msg')
        
        user_id=ElectricityConsumer.objects.get(id=user_id)
        authority = request.POST.get('user')  

        direction=2
        
        feedback = Feedback(user=user_id, authority=authority, msg=message, view_sts=0, direction=direction)
        feedback.save()

            
        return redirect('User:feedback')
    user_id = request.session['id']
    user_id=ElectricityConsumer.objects.get(id=user_id)
    received_messages = Feedback.objects.filter(user=user_id,direction=1)
    received_messages.update(view_sts=1)
    received_messages = Feedback.objects.filter(user=user_id).order_by('-id')

    return render(request,"User/feedback.html",{"data":received_messages})

def bills(request):
    Bills = Bill.objects.filter(user=ElectricityConsumer.objects.get(id=request.session["id"]),status=0)
    return render(request,"User/Bills.html",{"bills":Bills})

def bills2(request,id):
    bill=Bill.objects.get(id=id)
    bill.status=1
    bill.save()
    return render(request,"User/Pay.html",{"bills":bill})



def payments(request):
    Bills = Bill.objects.filter(user=ElectricityConsumer.objects.get(id=request.session["id"]),status=1)
    return render(request,"User/Payments.html",{"bills":Bills})

from currentusage import *
def getelectricityusage(request):
    print("rreecc")
    try:
        current_usage = Usage()
        return JsonResponse({'usage': current_usage})
    except Exception as e:
        print(e)
        return JsonResponse({'usage': "Server Issue"})


from currentmonth import *
def getelectricityusage2(request):
    print("rreecccccccc")
    try:
        current_usage = float(CurrentMonth())/1000
        rate="%.2f" % (current_usage*12)
        return JsonResponse({'usage': current_usage,"rate":rate})
    except Exception as e:
        print(e)
        return JsonResponse({'usage': "Server Issue","rate":"Server Issue"})
