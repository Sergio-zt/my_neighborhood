from django.urls import path
from neighborhood.views import (
    index,
    DistrictListView,
    DistrictCreateView,
    DistrictUpdateView,
    DistrictDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("district/", DistrictListView.as_view(), name="district-list"),
    path("district/create", DistrictCreateView.as_view(), name="district-create"),
    path("district/<int:pk>/update", DistrictUpdateView.as_view(), name="district-update"),
    path("district/<int:pk>/delete", DistrictDeleteView.as_view(), name="district-delete"),
    path(
        "districts/<int:pk>/toggle-membership/",
        DistrictListView.toggle_district_membership,
        name="toggle-district-membership"
    ),
]


app_name = "neighborhood"
