
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from endpoint.models import Account
from django.forms.models import model_to_dict


class AccountListAPI(APIView):
    permission_classes=(AllowAny, )

    
    def get(self, request, *args, **kwargs):
        account_list = Account.objects.all()
        response_data = list(account_list.values())
        return JsonResponse({"status": "okay", "data": response_data}, safe = False)


class AccountDetailAPI(APIView):
    permission_classes=(AllowAny, )

    
    def get(self, request, *args, **kwargs):
        account_id = self.request.query_params.get("id", False)
        if not account_id:
            return JsonResponse({"status": "id not provided"})
        account_object = Account.objects.get(id=account_id)
        account_dict = model_to_dict(account_object)
        account_dict["pw"] = "*****"
        return JsonResponse({"status": "okay", "data": account_dict}, safe = False)


class RegisterAPI(APIView):
    permission_classes=(AllowAny, )

    
    def post(self, request, *args, **kwargs):
        response = {"status": "okay"}
        request_data = request.POST.dict()
        Account.objects.create(**request_data)
        return JsonResponse(response, safe= False)

    def put(self, request, *args, **kwargs):
        response = {"status": "okay"}
        request_data = request.POST.dict()
        account_object = Account.objects.get(id=request_data["id"])
        account_object.pw = request_data["pw"]
        account_object.save()
        return JsonResponse(response, safe= False)
    
    def get(self, request, *args, **kwargs):
        account_id = self.request.query_params.get("id", False)
        if account_id and self.id_exists(account_id):
            return JsonResponse({"status": "cannot use"}, safe = False)
        return JsonResponse({"status": "okay"}, safe = False)
    
    def id_exists(self, user_id):
        return Account.objects.filter(id=user_id).exists()
