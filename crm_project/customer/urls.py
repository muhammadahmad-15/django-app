
from .views import CustomerCreate, CustomerList, CustomerDetail, CustomerUpdate, CustomerDelete
from django.urls import path, include


urlpatterns = [
    path('create/', CustomerCreate.as_view(), name='create-customer'),
    path('', CustomerList.as_view(), name="list-customers"),
    path('<int:pk>/', CustomerDetail.as_view(), name='retrieve-customer'),
    path('update/<int:pk>/', CustomerUpdate.as_view(), name='update-customer'),
    path('delete/<int:pk>/', CustomerDelete.as_view(), name='delete-customer')
]