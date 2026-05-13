from datetime import timedelta
from django.utils import timezone
from django.db import connection
from django.contrib.gis.geos import Point

from apps.common.constants import RESTAURANT_LAT,RESTAURANT_LNG

def calculate_distance(point1:Point, point2:Point):
    distance = point1.distance(point2)
    return distance
    


#har 5 minutda 4 ta taom va 1km -> 3minut
def calculating_imaginary_devilery_time(count_of_preparing_meats,point):
    dish_prepare_time = (count_of_preparing_meats+1)*5/4
    road_distance = calculate_distance(point,Point(RESTAURANT_LAT,RESTAURANT_LNG))
    print(road_distance,"1111111111111111111111111111")
    road_time = road_distance/1000*3
   
    print(dish_prepare_time)
    total_time_in_minutes = road_time+dish_prepare_time
    return timezone.localtime()+timedelta(minutes=total_time_in_minutes)