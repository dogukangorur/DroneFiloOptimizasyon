
# utils.py

import math
from datetime import datetime

def calculate_distance(coord1, coord2):
    """
    İki koordinat arasındaki düz mesafeyi hesaplar.
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def is_time_in_range(start_time, end_time, current_time=None):
    """
    Zamanın belirli bir aralıkta olup olmadığını kontrol eder.
    """
    if current_time is None:
        current_time = datetime.now()
    
    if start_time and end_time:
        return start_time <= current_time <= end_time
    return True


def is_point_in_polygon(point, polygon_coords):
    """
    Bir noktanın belirli bir çokgenin içinde olup olmadığını kontrol eder.
    Ray casting algoritması kullanılır.
    """
    x, y = point
    num = len(polygon_coords)
    j = num - 1
    inside = False
    for i in range(num):
        xi, yi = polygon_coords[i]
        xj, yj = polygon_coords[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def segment_crosses_polygon(pt1, pt2, polygon_coords):
    """
    Bir hattın herhangi bir çokgenin kenarlarını kesip kesmediğini kontrol eder.
    """
    # Eğer herhangi bir uç nokta çokgen içindeyse, hat kesişiyor demektir
    if is_point_in_polygon(pt1, polygon_coords) or is_point_in_polygon(pt2, polygon_coords):
        return True
    
    num = len(polygon_coords)
    for i in range(num):
        poly_pt1 = polygon_coords[i]
        poly_pt2 = polygon_coords[(i + 1) % num]
        
        if do_segments_intersect(pt1, pt2, poly_pt1, poly_pt2):
            return True
    
    return False


def do_segments_intersect(p1, p2, p3, p4):
    """
    İki çizgi parçasının kesişip kesişmediğini kontrol eder.
    """
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

