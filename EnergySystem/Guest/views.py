from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Admin.models import *

# Create your views here.
def home(request):
    return render(request,"Guest/index.html")


@csrf_exempt
def Login(request):
    if request.method == 'POST':
        print("------ Login Request Processing -------")
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        type=request.POST.get('type')
        print(request.POST)
        try:
            if userid=="admin" and password=="admin" and type=="Admin":
                return JsonResponse({'status': 1})
            elif type=="KSEB_Office":
                ob=KSEBOffice.objects.get(id=userid,password=password)
                request.session['id']=ob.id
                return JsonResponse({'status': 2})
            elif type=="User":
                ob=ElectricityConsumer.objects.get(email=userid,password=password,status=1)
                request.session['id']=ob.id
                return JsonResponse({'status': 3})
            else:
                ob=UserRegTbl.objects.get(email=userid,password=password)
                request.session['gmail']=ob.email
                return JsonResponse({'status': 4})
        except Exception as e:
            print(e)
            return JsonResponse({'status': "failed"})
    return render(request,"Guest/login.html")