import uuid
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from endpoint.models import Account, Pet, WeightRecord
from django.forms.models import model_to_dict
from django.core.files import File as DjangoFile


class PetListAPI(APIView):
    permission_classes=(AllowAny, )

    
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('account_num')
        user_object = Account.objects.get(id=user_id)
        pet_list = Pet.objects.all().filter(account=user_object)
       
        response_data = list(pet_list.values())
        return JsonResponse({"status": "okay", "data": response_data}, safe = False)


class WeightAPI(APIView):
    permission_classes=(AllowAny, )


    def post(self, request, *args, **kwargs):
        response = {"status": "okay"}
        request_data = request.POST.dict()
        request_data["id"] = str(uuid.uuid4())
        request_data["pet"] = Pet.objects.get(id=request_data["pet"])
        WeightRecord.objects.create(**request_data)
        return JsonResponse(response, safe= False)


class PetAPI(APIView):
    permission_classes=(AllowAny, )

    def post(self, request, *args, **kwargs):
        response = {"status": "okay"}
        request_data = request.POST.dict()
        request_data["id"] = str(uuid.uuid4())
        request_data["account"] = Account.objects.get(id=request_data["account"])
        try:
            img_file = request.FILES["image"]
            request_data["profile_img"] = img_file
        except:
            request_data["profile_img"] = "no image"
        Pet.objects.create(**request_data)
        return JsonResponse(response, safe= False)

    def put(self, request, *args, **kwargs):
        pet_id = self.request.query_params.get("id", False)
        remove_pic = self.request.query_params.get("delete", False)
        response = {"status": "okay"}
        if remove_pic == bool(remove_pic):
            # request_data = request.POST.dict()
            img_file = request.FILES["image"]
            pet_obj = Pet.objects.get(id = pet_id)
            try:
                pet_obj.profile_img = img_file
            except Exception as e:
                print(e)
            pet_obj.save()
            return JsonResponse(response, safe= False)
        else:
            pet_obj = Pet.objects.get(id = pet_id)
            pet_obj.profile_img = "no image"
            pet_obj.save()
            return JsonResponse(response, safe= False)
    
    def get(self, request, *args, **kwargs):
        pet_id = self.request.query_params.get("id", False)
        if pet_id:
            response = {"status": "okay"}
            pet_object = Pet.objects.get(id=pet_id)
            pet_dict = model_to_dict(pet_object)
            pet_dict["profile_img"] = str(pet_object.profile_img)
            weight_objects = WeightRecord.objects.filter(pet=pet_object).order_by("created_date")
            pet_dict["weight_list"] = list(weight_objects.values('id', 'weight', 'created_date'))
            response["data"] = pet_dict
            return JsonResponse(response)
        return JsonResponse({"status": "pet id not provided"}, safe = False)
