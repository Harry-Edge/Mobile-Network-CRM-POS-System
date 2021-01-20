from django.urls import path
from . import views
from .process_upgrade import delete_cart

urlpatterns = [
    path('dashboard/<str:pk>', views.dashboard, name='dashboard'),

    path('<str:pk>/sim-upgrade/', views.build_sim_only_upgrade, name='buildsimoupgrade'),
    path('<str:pk>/sim-upgrade/finalise-sim/', views.finalise_sim_only_upgrade, name='finalisesimup'),

    path('<str:pk>/handset-upgrade/', views.build_handset_upgrade, name='buildhandsetupgrade'),
    path('<str:pk>/handset-upgrade/select-tariff/', views.choose_handset_tariff, name='choosehandsettariff'),
    path('<str:pk>/handset-upgrade/finalise/', views.finalise_handset_upgrade, name='finalisehandsetup'),

    path('delete_cart/<str:pk>/<str:option>', delete_cart, name='deletecart'),

]