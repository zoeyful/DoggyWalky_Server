import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from endpoint.models import Account, Pet, Meal, MealRecord
from django.forms.models import model_to_dict

# Create your views here.
class LoginAPI(APIView):
    permission_classes=(AllowAny, )
    
    
    def post(self, request, *args, **kwargs):
        response = {}
        request_data = request.POST.dict()
        response["result"] = "does not exsits"
        if self.account_exists(request_data):
            response["result"] = "success"
            response["id"] = request_data["id"]
        return JsonResponse(response, safe = False)
    

    def account_exists(self, user_data):
        return Account.objects.filter(id=user_data["id"]).filter(pw=user_data["pw"]).exists()


class MealAPI(APIView):
    permission_classes=(AllowAny, )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('account_id')
        if Account.objects.filter(id=user_id).exists():
            user_object = Account.objects.get(id=user_id)
            request_data = request.POST.dict()
            request_data["id"] = str(uuid.uuid4())
            request_data["account"] = user_object
            Meal.objects.create(**request_data)
            response_data = {"status": "okay"}
            
            return JsonResponse(response_data, safe = False)
        return JsonResponse({"status": "id does not exists"}, safe=False)

    def delete(self, request, *args, **kwargs):
        response_data = {"status": "okay"}
        request_data = request.POST.dict()
        meal_obj = Meal.objects.get(id = request_data["id"])
        meal_obj.delete()
        return JsonResponse(response_data, safe = False)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('account_id')
        if Account.objects.filter(id=user_id).exists():
            user_object = Account.objects.get(id=user_id)
            response_data = {"status": "okay"}
            activity_data = Meal.objects.filter(account=user_object).all()
            response_data['data'] = list(activity_data.values())
            return JsonResponse(response_data, safe = False)
        return JsonResponse({"status": "id does not exists"}, safe=False)

class MealRecordAPI(APIView):
    permission_classes=(AllowAny, )

    def post(self, request, *args, **kwargs):
        request_data = request.POST.dict()
        print(request_data)
        request_data["id"] = str(uuid.uuid4())
        request_data["meal"] = Meal.objects.get(id=request_data["meal"])
        request_data["pet"] = Pet.objects.get(id=request_data["pet"])
        MealRecord.objects.create(**request_data)
        response_data = {"status": "okay"}
        return JsonResponse(response_data, safe = False)

    def put(self, request, *args, **kwargs):
        response_data = {"status": "okay"}
        request_data = request.POST.dict()
        meal_obj = MealRecord.objects.get(id=request_data["id"])
        meal_obj.delete()
        return JsonResponse(response_data, safe = False)

    def get(self, request, *args, **kwargs):
        pet_id = self.request.query_params.get("id", False)
        if pet_id and Pet.objects.filter(id=pet_id).exists():
            meal_record_list = MealRecord.objects.filter(pet=pet_id)
            return_data_list = []
            for meal_record_item in meal_record_list:
                return_item = model_to_dict( Meal.objects.get(id= meal_record_item.meal_id ) )
                return_item["record_date"] = meal_record_item.created_date
                return_data_list.append(return_item)
            response_data = {"status": "okay"}
            response_data['data'] = return_data_list
            return JsonResponse(response_data, safe = False)
        return JsonResponse({"status": "pet id does not exists"}, safe=False)

class RouteAPI(APIView):
    permission_classes=(AllowAny, )


    def get(self, request, *args, **kwargs):
        route_id = kwargs.get('route_id')

        gpx_file = open('Data/gpx/demo.gpx', "rt")
        
        response = {"result": "okay", "data": gpx_file.read()}
        return JsonResponse(response, safe=False)
