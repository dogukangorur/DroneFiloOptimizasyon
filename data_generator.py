import random
from entities import Drone, DeliveryPoint, NoFlyZone
from utils import is_point_in_polygon

# No-Fly Zone'lar için sabit koordinat tanımlamaları
FIXED_NFZ_1 = [
    (200, 200),
    (300, 200),
    (300, 300),
    (200, 300)
]

FIXED_NFZ_2 = [
    (600, 500),
    (700, 500),
    (750, 600),
    (650, 650),
    (550, 600)
]

FIXED_NFZ_3 = [
    (300, 600),
    (200, 400),
    (400, 400)
]

def generate_random_drones(num_drones, max_x, max_y):
    drones = []
    for i in range(num_drones):
        # Sabit alan içinde drone başlangıç konumu oluştur (x: 400-600, y: 0-200)
        start_pos = (random.randint(400, 600), random.randint(0, 200))
        
        max_weight = random.uniform(1.0, 5.0)
        battery = random.randint(1000, 3000)
        speed = random.uniform(10.0, 30.0)
        
        drones.append(Drone(i+1, max_weight, battery, speed, start_pos))
    return drones

def generate_random_delivery_points(num_points, max_x, max_y):
    delivery_points = []
    nfzs = generate_fixed_no_fly_zones()  # No-fly zone'ları al
    
    point_id = 101
    while len(delivery_points) < num_points:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        location = (x, y)
        
        # No-fly zone kontrolü
        is_in_nfz = False
        for nfz in nfzs:
            if is_point_in_polygon(location, nfz.coordinates):
                is_in_nfz = True
                break
                
        if is_in_nfz:
            continue  # No-fly zone içindeyse bu konumu atla
            
        weight = random.uniform(0.5, 3.0)
        priority = random.randint(1, 5)
        
        # Zaman aralığı (opsiyonel)
        if random.random() > 0.5:
            start_hour = random.randint(8, 18)
            end_hour = min(start_hour + random.randint(1, 4), 22)
            time_window = (f"{start_hour:02d}:00", f"{end_hour:02d}:00")
        else:
            time_window = None
            
        delivery_points.append(DeliveryPoint(point_id, location, weight, priority, time_window))
        point_id += 1
        
    return delivery_points

def generate_fixed_no_fly_zones():
    """Sabit No-Fly Zone nesneleri üretir."""
    no_fly_zones = []
    
    # İlk No-Fly Zone
    zone_id_1 = 1001  # Diğer ID'lerle karışmaması için
    active_time_1 = ("09:30", "11:00")  # Sabit zaman aralığı
    no_fly_zones.append(NoFlyZone(zone_id_1, FIXED_NFZ_1, active_time_1[0], active_time_1[1]))
    
    # İkinci No-Fly Zone
    zone_id_2 = 1002
    active_time_2 = ("13:00", "15:30")  # Sabit zaman aralığı
    no_fly_zones.append(NoFlyZone(zone_id_2, FIXED_NFZ_2, active_time_2[0], active_time_2[1]))

    zone_id_3 = 1003
    active_time_3 = ("14:00", "14:30")  # Sabit zaman aralığı
    no_fly_zones.append(NoFlyZone(zone_id_3, FIXED_NFZ_3, active_time_3[0], active_time_3[1]))
    
    return no_fly_zones

if __name__ == '__main__':
    # Sabit değerlerle test
    num_drones = 5
    num_deliveries = 20
    
    drones_list = generate_random_drones(num_drones)
    deliveries_list = generate_random_delivery_points(num_deliveries)
    nfzs_list = generate_fixed_no_fly_zones()
    
    print(f"-- {num_drones} Drone Oluşturuldu --")
    for drone in drones_list:
        print(drone)
        
    print(f"\n--- {num_deliveries} Teslimat Noktası Oluşturuldu ---") 
    for point in deliveries_list:
        print(point)
        
    print(f"\n-- {len(nfzs_list)} NoFly Zone Oluşturuldu --")
    for nfz in nfzs_list:
        print(nfz)

