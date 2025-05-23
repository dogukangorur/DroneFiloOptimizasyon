
# utils.py

import math
from datetime import datetime

def heuristic(point1, point2):
    """İki nokta arasındaki Öklid mesafesini hesaplar."""
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5


def is_time_in_range(start_time, end_time, current_time=None):
    """
    Zamanın belirli bir aralıkta olup olmadığını kontrol eder.
    """
    if current_time is None:
        current_time = datetime.now()
    
    if start_time and end_time:
        return start_time <= current_time <= end_time
    return True


def is_point_in_polygon(point, polygon):
    """Check if a point is inside a polygon."""
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def segment_crosses_polygon(segment, polygon):
    """Check if a line segment crosses or is inside a polygon."""
    p1, p2 = segment
    
    # Check if either endpoint is inside the polygon
    if is_point_in_polygon(p1, polygon) or is_point_in_polygon(p2, polygon):
        return True
    
    # Check if the segment intersects any polygon edge
    for i in range(len(polygon)):
        poly_p1 = polygon[i]
        poly_p2 = polygon[(i + 1) % len(polygon)]
        
        if segments_intersect(p1, p2, poly_p1, poly_p2):
            return True
    
    return False
        
    return False
def segments_intersect(p1, p2, p3, p4):
    """Check if two line segments (p1,p2) and (p3,p4) intersect."""
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or Counterclockwise
    
    def on_segment(p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))
    
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)
    
    # General case
    if o1 != o2 and o3 != o4:
        return True
    
    # Special Cases
    if o1 == 0 and on_segment(p1, p3, p2): return True
    if o2 == 0 and on_segment(p1, p4, p2): return True
    if o3 == 0 and on_segment(p3, p1, p4): return True
    if o4 == 0 and on_segment(p3, p2, p4): return True
    
    return False


def do_segments_intersect(p1, p2, p3, p4):
    """İki doğru parçasının kesişip kesişmediğini kontrol eder."""
    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
    
    d1 = cross_product(p3, p4, p1)
    d2 = cross_product(p3, p4, p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1, p2, p4)
    
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    
    if d1 == 0 and is_point_on_segment(p3, p4, p1):
        return True
    if d2 == 0 and is_point_on_segment(p3, p4, p2):
        return True
    if d3 == 0 and is_point_on_segment(p1, p2, p3):
        return True
    if d4 == 0 and is_point_on_segment(p1, p2, p4):
        return True
    
    return False

def is_point_on_segment(p1, p2, p):
    """Bir noktanın bir doğru parçası üzerinde olup olmadığını kontrol eder."""
    return (min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and
            min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1]))

def parse_time_str(time_str):
    from datetime import datetime
    return datetime.strptime(time_str, "%H:%M") if time_str else None

