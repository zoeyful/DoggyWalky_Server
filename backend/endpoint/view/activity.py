import os
import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from endpoint.models import Account, ActivityRecord
from math import floor
import gpxpy
import haversine

GPX_BASEDIR = os.path.join("Data", "gpx")


class ActivityListAPI(APIView):
    permission_classes=(AllowAny, )

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('account_id')
        if Account.objects.filter(id=user_id).exists():
            user_object = Account.objects.get(id=user_id)
            response_data = {"status": "okay"}
            activity_data = ActivityRecord.objects.all()
            response_data['data'] = list(activity_data.values())
            return JsonResponse(response_data, safe = False)
        return JsonResponse({"status": "id does not exists"}, safe=False)

# Create your views here.
class ActivityAPI(APIView):
    permission_classes=(AllowAny, )
    
    def calculate_gpx(self, data):
        time_dif = [0]
        dist_hav_no_alt = [0]
        dist_dif_hav_2d = [0]
        
        for index in range(len(data)):
            if index == 0:
                pass
            else:
                start = data[index-1]
                stop = data[index]
                
                distance_hav_2d = haversine.haversine((start.latitude, start.longitude), (stop.latitude, stop.longitude))*1000
                
                dist_dif_hav_2d.append(distance_hav_2d)
                dist_hav_no_alt.append(dist_hav_no_alt[-1] + distance_hav_2d)
                time_delta = (stop.time - start.time).total_seconds()
                time_dif.append(time_delta)

        travel_distance  =  dist_hav_no_alt[-1]        
        total_time = "{} min {} sec".format(floor(sum(time_dif)/60), int(sum(time_dif)%60))
        print('Haversine 2D : ', travel_distance)
        print('Total Time : ', total_time)
        return travel_distance, total_time


    def post(self, request, *args, **kwargs):
        activity_id = uuid.uuid4()
        gpx_filename = "{}.gpx".format(activity_id)
        user_id = kwargs.get('account_id')
        user_object = Account.objects.get(id="test1")

        response = {}
        
        xml_data = request.body.decode("utf-8") 
        
        os.makedirs(GPX_BASEDIR, exist_ok=True)
        with open( os.path.join(GPX_BASEDIR, gpx_filename), 'w') as xml_file:
            xml_file.write(xml_data)
        
        with open( os.path.join(GPX_BASEDIR, gpx_filename) , 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        
        data = gpx.tracks[0].segments[0].points
        
        travel_distance, total_time = self.calculate_gpx(data)
        
        activity_object = ActivityRecord(
            id = activity_id,
            name = "test",
            activity_duration = total_time,
            total_distnace = travel_distance,
            gpx_file = os.path.join(GPX_BASEDIR, gpx_filename),
            account = user_object
        )
        activity_object.save()

        response["result"] = "okay"
        response["data"] = {"travel_distance" : travel_distance, "total_time" :  total_time}
        return JsonResponse(response, safe = False)
    

    
