import random
from entities import Drone, DeliveryPoint, NoFlyZone
from utils import is_point_in_polygon

NFZS = [
    [(250, 650),(250, 750),(350, 750),(350, 650)],
    [(600, 500),(600, 400),(750, 400),(750, 500)],
    [(300, 600),(200, 400),(400, 400),(500, 600)],
    [(700, 300),(700, 100),(900, 100),(900, 300)],
    [(250, 650),(250, 750),(350, 650),(350, 750)],
    [(300, 200),(300, 300),(400, 300),(400, 200)]
]

def generate_random_drones(num_drones, max_x, max_y):
    drones = []
    for i in range(num_drones):
        # Sabit alan içinde drone başlangıç konumu oluştur
        start_pos = (random.randint(400, 600), random.randint(0, 200))
        
        max_weight = random.uniform(2.0, 6.0)
        battery = random.randint(8000, 20000)
        speed = random.uniform(8.0, 15.0)
        
        drones.append(Drone(i+1, max_weight, battery, speed, start_pos))
    return drones

def generate_random_delivery_points(num_points, max_x, max_y):
    delivery_points = []
    nfzs = generate_fixed_no_fly_zones()  
    
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
            continue  
            
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
    is_exists =[]
    while len(is_exists) < 3:
            new_num = random.randint(0, 5)
            if new_num not in is_exists:
                is_exists.append(new_num)

    POSSIBLE_ACTIVE_TIMES = [
    ("08:00", "08:30"), ("09:00", "09:45"), ("10:15", "11:00"),
    ("11:30", "12:00"), ("13:00", "13:45"), ("14:00", "15:00"),
    ("15:30", "16:15"), ("17:00", "17:30"),("18:00", "19:00"),("19:30", "20:30"),("19:00", "19:45")
    ]

    for i in range(0,3):
        zone_id = 1000 + i
        active_time = POSSIBLE_ACTIVE_TIMES[random.randint(0,9)] 
        NFZ = NFZS[is_exists[i]]
        no_fly_zones.append(NoFlyZone(zone_id, NFZ, active_time[0], active_time[1]))


    """
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
    """
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

