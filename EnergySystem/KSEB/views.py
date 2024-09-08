from django.shortcuts import render,HttpResponse
from Admin.models import *
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.db.models import Q
from django.http import JsonResponse
import paho.mqtt.client as paho

# Create your views here.
def home(request):
    return render(request,"KSEB/home.html")


### create new consumer
def addconsumers(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            address = request.POST.get('address')
            connection_number = request.POST.get('connectionNumber')
            phone_number = request.POST.get('phoneNumber')
            email = request.POST.get('email')
            office_id = KSEBOffice.objects.get(id=request.session["id"])
            connection_date = request.POST.get('connectionDate')
            status = 1
            password = request.POST.get('password')
            
            # Create ElectricityConsumer instance
            consumer = ElectricityConsumer.objects.create(
                name=name,
                address=address,
                connection_number=connection_number,
                phone_number=phone_number,
                email=email,
                office_id=office_id,
                connection_date=connection_date,
                status=status,
                password=password
            )
            
            return render(request,"KSEB/savedpage.html",{"data":"KSEB:home"})
        except Exception as e:
            print(e)
            return render(request,"KSEB/failed_page.html",{"data":"KSEB:home"})
    return render(request,"KSEB/addconsumers.html")

## view consumers detls
def viewconsumers(request):
    consumers=ElectricityConsumer.objects.filter(office_id=request.session["id"])
    return render(request,"KSEB/viewconsumers.html",{"consumers":consumers})


### EDITING CONSUMERS DETLS
def edit_consumer(request, consumer_id):
    
    consumer = ElectricityConsumer.objects.get(id=consumer_id)
    
    if request.method == 'POST':
        try:
            consumer.name = request.POST.get('name')
            consumer.address = request.POST.get('address')
            consumer.connection_number = request.POST.get('connection_number')
            consumer.phone_number = request.POST.get('phone_number')
            consumer.email = request.POST.get('email')
            
            consumer.save()
       
            return render(request,"KSEB/savedpage.html",{"data":"KSEB:viewconsumers"})
        except Exception as e:
            print(e)
            return render(request, 'KSEB/failed_page.html', {"data":"KSEB:viewconsumers"})

    return render(request, 'KSEB/edit_consumer.html', {'consumer': consumer})
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def block_consumer(request, consumer_id):
    
    if request.method == 'POST':
        
        try:
            consumer = ElectricityConsumer.objects.filter(id=consumer_id).first()
            consumer.status = 1 if consumer.status == 0 else 0
            consumer.save()
            print(consumer.status)
            
            return render(request,"KSEB/savedpage.html",{"data":"KSEB:viewconsumers"})
        except Exception as e:
            print(e)
            return render(request,"KSEB/failed_page.html",{"data":"KSEB:viewconsumers"})


def Feedback1(request):
    if request.method == 'POST':
        
        message = request.POST.get('msg')
        
        user_id=ElectricityConsumer.objects.get(id=request.POST.get('user'))
        
        authority=2
        direction=1
        
        office=request.session["id"]
        office=KSEBOffice.objects.get(id=office)
        try:
            ele=ElectricityConsumer.objects.get(id=request.POST.get('user'),office_id=office)
            feedback = Feedback(user=user_id, authority=authority, msg=message, view_sts=0, direction=direction)
            feedback.save()
        except Exception as e:
            pass

            
        return redirect('KSEB:Feedback')
    
    office=request.session["id"]
    office=KSEBOffice.objects.get(id=office)    
    list1=[]
    received_messages_to_update = Feedback.objects.filter(authority=2, direction=2)
    for i in received_messages_to_update:
        if i.user.office_id.id==request.session["id"]:
            i.view_sts=1
            i.save()
            
    received_messages_to_update = Feedback.objects.filter(authority=2).order_by('-id')
    for i in received_messages_to_update:
        if i.user.office_id.id==request.session["id"]:
            list1.append(i)
    return render(request, 'KSEB/Feedback.html',{"data":list1})     



def ANNOUNCEMENT(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        office_id = request.session["id"]
        announcement = Annoucement.objects.create(office_id=office_id, msg=msg)
        return redirect('KSEB:ANNOUNCEMENT')
    office=KSEBOffice.objects.get(id=request.session["id"])
    ob=Annoucement.objects.filter(office=office)
    return render(request, 'KSEB/ANNOUNCEMENT.html',{"data":ob})

def delete_announcement(request,announcement_id):
    if request.method == 'POST':
        announcement = Annoucement.objects.get(id=announcement_id)
        announcement.delete()
    return redirect('KSEB:ANNOUNCEMENT')

from previousmonth import *
from currentmonth import *
from currentusage import Usage as u

def Payments(request):
    Bills = Bill.objects.filter(user__office_id=request.session["id"])
    return render(request, 'KSEB/Payments.html',{"bills":Bills})

def Usage(request):
    consumers=ElectricityConsumer.objects.filter(office_id=request.session["id"])
    return render(request, 'KSEB/Usage.html',{"consumers":consumers})

def view_more(request,consumer_id):
    data1=u()
    data2=str(float(CurrentMonth())/1000)+" KWH"
    current_date = datetime.datetime.now()
    previous_month_date = current_date - relativedelta(months=1)
    previous_month_name = previous_month_date.strftime("%B")
    if Bill.objects.filter(month=previous_month_name,user=ElectricityConsumer.objects.get(id=consumer_id)).first() == None:
        data3=float(previousmonth())+240
        sts=0
    else:
        data3=float(previousmonth())+240
        sts=1
    consumers=ElectricityConsumer.objects.filter(id=consumer_id).first()
    Bills=Bill.objects.filter(user=ElectricityConsumer.objects.get(id=consumer_id))
    return render(request, 'KSEB/view_more.html',{"consumer":consumers,"data1":data1,"data2":data2,"data3":data3,"sts":sts,"bills":Bills})

import datetime
import os
from django.conf import settings

from django.shortcuts import redirect
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from dateutil.relativedelta import relativedelta
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter


import datetime

def GenerateBill(request, consumer_id):
    try:
        # Calculate usage and rate
        
        data2 = (float(previousmonth()) + 240) / 1000
        rate = data2 * 12

        # Get previous month name
        current_date = datetime.datetime.now()
        previous_month_date = current_date - relativedelta(months=1)
        previous_month_name = previous_month_date.strftime("%B")
        if Bill.objects.filter(month=previous_month_name,user=ElectricityConsumer.objects.get(id=consumer_id)).first() == None:
        # Get current date
            current_date = current_date.date()

            # Get consumer
            consumer = ElectricityConsumer.objects.get(id=consumer_id)

            # Create Bill object
            ob = Bill.objects.create(user=consumer, kwh=data2, status=0, rate=rate, month=previous_month_name, BillGenerationdate=current_date)
            BillID = ob.id

            # Generate PDF
            filename = f"INVOICE{ob.id}.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'bills', filename)
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Add logo
            logo_path = "static/kseb-logo.png"
            logo = Image(logo_path, width=200, height=100)  # Adjust width and height as needed
            story.append(logo)

            # Add content to the PDF
            heading = Paragraph("Bill Receipt", styles['Heading1'])
            story.append(heading)
            # Add spacer for center alignment

            # Add line breaks


            story.append(Paragraph(f"Month: {previous_month_name}", styles['Normal']))
            story.append(Paragraph(f"Date: {current_date}", styles['Normal']))
            story.append(Paragraph(f"Payment ID: {ob.id}", styles['Normal']))
            story.append(Paragraph(f"Consumer Name: {consumer.name}", styles['Normal']))
            story.append(Paragraph(f"Consumer ID: {consumer.id}", styles['Normal']))
            story.append(Paragraph(f"Address: {consumer.address}", styles['Normal']))
            office_id = consumer.office_id
            story.append(Paragraph(f"OFFICE NAME: {office_id.name}", styles['Normal']))
            story.append(Paragraph(f"Total KWH: {data2}", styles['Normal']))
            story.append(Paragraph(f"Amount: {rate}", styles['Normal']))

            # Build the PDF document
            doc.build(story)

            # Save the file path to the Bill object
            ob.file.name = os.path.relpath(file_path, settings.MEDIA_ROOT)
            ob.save()
    except Exception as e:
        print(e)
    return redirect('KSEB:view_more', consumer_id=consumer_id)
