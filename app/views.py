# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from smart_agro.core.models import CropsData, Land, SoilData, Farmer
from smart_agro.core.utils import getCropsSuggestion
from django.forms.models import model_to_dict
from datetime import datetime, time, timedelta
from django.utils import timezone




@login_required(login_url="/login/")
def dashboard(request):
    
    statistics = getStatistics(request)
    lands =  list(Land.objects.filter(farmer=request.user.farmer.id))

    if len(lands) > 0:
        return redirect(f"/dashboard/soil-data/{lands[-1].id}")
    else:
        return render(request, "dashboard.html", {'statistics': statistics,'lands': lands})


@login_required(login_url="/login/")
def soil_data(request,land_id):
    statistics = getStatistics(request)
    lands =  list(Land.objects.filter(farmer=request.user.farmer.id))
    selected_land = Land.objects.get(id=land_id)
    soil_data = get_soil_data(land_id= land_id, date= datetime.now().strftime("%d-%m-%Y"))


    print(soil_data)
    return render(request, "dashboard.html", {'statistics': statistics,\
    'lands': lands,'selected_land': selected_land,'soil_data': soil_data})


@login_required(login_url="/login/")
def soil_data_by_date(request,land_id,date):
    statistics = getStatistics(request)
    lands =  list(Land.objects.filter(farmer=request.user.farmer.id))
    selected_land = Land.objects.get(id=land_id)
    soil_data = get_soil_data(land_id= land_id, date= date)
    print(soil_data)
    return render(request, "dashboard.html", {'statistics': statistics,\
    'lands': lands,'selected_land': selected_land,'selected_date': date, 'soil_data': soil_data})


@login_required(login_url="/login/")
def profile(request):
    
    return render(request, "profile.html",)

@login_required(login_url="/login/")
def edit_profile(request):
    if request.method == "POST":
        print('======= form submitted =====')
        print(list(request.POST.items()))
        print('======= file submitted =====')
        print(list(request.FILES.items()))

        User.objects.filter(id = request.user.id).update(
                    first_name = request.POST.get("first_name", ""), \
                    last_name =  request.POST.get("last_name", ""))

        farmer = Farmer.objects.get(user = request.user)
        farmer.address = request.POST.get("address", "")
        farmer.phone =  request.POST.get("phone", "")
        farmer.city =  request.POST.get("city", "")
        farmer.country =  request.POST.get("country", "")
        farmer.postal_code =  request.POST.get("postal_code", "")
        farmer.about_me =  request.POST.get("about_me", "")

        if len(list(request.FILES.items())) > 0:
            farmer.profile_image = request.FILES.get("image_file") 
        farmer.save()

        return redirect("/profile/")

    else:
        return render(request, "edit-profile.html",)

@login_required(login_url="/login/")
def lands(request):
        statistics = getStatistics(request)

        lands =  list(Land.objects.filter(farmer=request.user.farmer.id))

        return render(request, "lands.html", {'statistics': statistics,'lands': lands})

@login_required(login_url="/login/")
def add_land(request):

    if request.method == "POST":
        print('======= form submitted =====')
        print(list(request.POST.items()))
        
        land = Land.objects.create(
                    name = request.POST.get("name", ""), \
                    area =  request.POST.get("area", 0.0), \
                    currentCrops=  request.POST.get("currentCrops", ""),\
                    address= request.POST.get("address", ""))
        land.farmer.add(request.user.farmer)

        return redirect("/lands/")

    else:
        statistics = getStatistics(request)
        lands =  list(Land.objects.filter(farmer=request.user.farmer.id))
        return render(request, "add-land.html", {'statistics': statistics,'lands': lands})

@login_required(login_url="/login/")
def edit_land(request,land_id):

    if request.method == "POST":
        print('======= form submitted =====')
        print(list(request.POST.items()))

        Land.objects.filter(id = land_id).update(
                    name = request.POST.get("name", ""), \
                    area =  request.POST.get("area", 0.0), \
                    currentCrops=  request.POST.get("currentCrops", ""),\
                    address= request.POST.get("address", ""))

        return redirect("/lands/")

    else:

        land_qs =  Land.objects.filter(id=land_id)
        print("===== edit land id=====")
        print(land_id)
        print(land_qs)
        try:
            land = land_qs[0]
        except:
            print('Land query set is None')

        return render(request, "edit-land.html", {'land': land})


@login_required(login_url="/login/")
def delete_land(request,land_id):

    Land.objects.filter(id=land_id).delete()
    return redirect("/lands/")

        

@login_required(login_url="/login/")
def maps(request):
    
    statistics = getStatistics(request)

    return render(request, "maps.html", {'statistics': statistics})

@login_required(login_url="/login/")
def suggestion(request):
    
    statistics = getStatistics(request)

    lands =  list(Land.objects.filter(farmer=request.user.farmer.id))
    land_data_map_list = []

    for land in lands:
        soil_data_list = list(SoilData.objects.filter(land=land.id))
       
        mos = 0
        pH = 0.0
        N = 0
        P = 0
        K = 0

        if(len(soil_data_list) > 0):
            for soil_data in soil_data_list:
                mos += soil_data.moisture
                pH += soil_data.pH
                N += soil_data.N
                P += soil_data.P
                K += soil_data.K

            mos /= len(soil_data_list)
            pH /= len(soil_data_list)
            N /= len(soil_data_list)
            P /= len(soil_data_list)
            K /= len(soil_data_list)

        land_data_map_list.append({'id': land.id,'name': land.name,'mos': round(mos) ,'pH': pH,'N': round(N),'P': round(P),'K': round(K)})

    

    return render(request, "suggestion.html", {'statistics': statistics,'land_data_map_list': land_data_map_list})

@login_required(login_url="/login/")
def get_suggestion(request,land_id):
    
    statistics = getStatistics(request)

    suggestion_data =  getCropsSuggestion(land_id)

    return render(request, "get-suggestion.html", {'statistics': statistics,'suggestion_data': suggestion_data})




def getStatistics(request):
  user = request.user
  farmer_id = user.farmer.id
  lands = list(Land.objects.filter(farmer=farmer_id))
  soid_data = 0
  for land in lands:
      soid_data += len(list(SoilData.objects.filter(land= land.id)))
  crops = len(list(CropsData.objects.all()))

  return {'lands': len(lands),'soil_data': soid_data,'crops': crops }


def get_soil_data(land_id,date):
    print("date=",datetime.strptime(date, '%d-%m-%Y'))
    print("date=",datetime.today)

    soil_data_list = list(SoilData.objects.filter(land=land_id,time__date=datetime.strptime(date, '%d-%m-%Y')))
    print("soil data object length=",len(soil_data_list))
    
    mos =[]
    pH = []
    N = []
    P = []
    K = []

    if len(soil_data_list) > 0:
        min_date_time = datetime.combine(datetime.strptime(date, '%d-%m-%Y'), time.min,timezone.get_default_timezone()) 
        max_date_time = datetime.combine(datetime.strptime(date, '%d-%m-%Y'), time.max,timezone.get_default_timezone()) 
        time_delta = timedelta(hours=2,minutes=59,seconds= 59,milliseconds=999,microseconds=999)
        print("today min max time=",min_date_time,max_date_time) 
        
        while((min_date_time + time_delta) <= max_date_time):
            three_hours_data = []
            for data in soil_data_list:
                if(data.time >= min_date_time and data.time <= (min_date_time + time_delta)):
                    three_hours_data.append(data)

            if len(three_hours_data) > 0:
                avg_mos = 0
                avg_pH = 0.0
                avg_N = 0
                avg_P = 0
                avg_K = 0
                for data in three_hours_data:
                    avg_mos += data.moisture
                    avg_pH += data.pH
                    avg_N += data.N
                    avg_P += data.P
                    avg_K += data.K
                
                avg_mos /= len(three_hours_data)
                avg_pH /= len(three_hours_data)
                avg_N /= len(three_hours_data)
                avg_P /= len(three_hours_data)
                avg_K /= len(three_hours_data)
                
                mos.append(int(avg_mos))
                pH.append(avg_pH)
                N.append(int(avg_N))
                P.append(int(avg_P))
                K.append(int(avg_K))

            else:
                mos.append(-99)
                pH.append(-14)
                N.append(-100)
                P.append(-100)
                K.append(-100)
                
            

            min_date_time += time_delta
            print("today min max time=",min_date_time,max_date_time)


    soil_data = {
        # 'mos': [20,10,50,-99,99,-99,60,10],
        # 'pH': [-14,-14,-14,-14,6,6.5,7.5,7],
        # 'N': [-1,-1,-1,158,-1,174,-1,-1],
        # 'P': [130,-1,127,200,-1,124,155,122],
        # 'K': [-10,-10,127,158,-1,145,155,-1]   
        'mos': mos,
        'pH': pH,
        'N': N,
        'P': P,
        'K': K  
    }

    return soil_data
