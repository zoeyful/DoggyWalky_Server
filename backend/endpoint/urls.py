
from endpoint.views import LoginAPI, MealAPI, MealRecordAPI, RouteAPI
from endpoint.view import account, pet, activity
from django.urls import path

urlpatterns = [
    path('login', LoginAPI.as_view()),
    path('register', account.RegisterAPI.as_view()),

    path('list/account', account.AccountListAPI.as_view()),
    path('list/pet/<account_num>', pet.PetListAPI.as_view()),
    path('list/activity/<account_id>', activity.ActivityListAPI.as_view()),
    path('list/meal/<account_id>', MealAPI.as_view()),
    
    path('detail/account', account.AccountDetailAPI.as_view()),
    path('detail/pet', pet.PetAPI.as_view()),
    path('detail/weight', pet.WeightAPI.as_view()),
    
    path('detail/mealrecord', MealRecordAPI.as_view() ),
    path('detail/activity/<account_id>', activity.ActivityAPI.as_view()),

    path('detail/route/<route_id>', RouteAPI.as_view())
]
