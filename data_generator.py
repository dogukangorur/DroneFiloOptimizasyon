import random
from entities import Drone, DeliveryPoint, NoFlyZone

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

def generate_random_drones(num_drones=5, max_x=1000, max_y=1000):
    drones = []
    for i in range(num_drones):
        drone_id = i + 1
        max_weight = round(random.uniform(2.0, 10.0), 1)  # Örnek: 2.0 ile 10.0 kg arası
        # Pil değeri üretiliyor ve Drone nesnesine iletiliyor
        battery_capacity = random.randint(5000, 20000)  # Örnek: 5000 ile 20000 birim arası pil
        speed = round(random.uniform(5.0, 20.0), 1)  # Örnek: 5.0 ile 20.0 birim/sn arası
        location = (random.randint(0, max_x), random.randint(0, max_y))  # Başlangıç konumları
        # Drone nesnesi oluşturulurken battery değeri battery_capacity olarak iletiliyor
        drones.append(Drone(drone_id, max_weight, battery_capacity, speed, location))
    return drones

def generate_random_delivery_points(num_points=20, max_x=1000, max_y=1000):
    delivery_points = []
    base_id = 101  # Teslimat ID'leri için başlangıç değeri
    for i in range(num_points):
        point_id = base_id + i
        location = (random.randint(0, max_x), random.randint(0, max_y))
        # Ağırlık değeri üretiliyor ve DeliveryPoint'e iletiliyor
        weight = round(random.uniform(1.0, 5.0), 1)  # Örnek: 1.0 ile 5.0 kg arasında rastgele ağırlık
        priority = random.randint(1, 5)  # Örnek: 1 (en düşük) ile 5 (en yüksek) arasında öncelik
        # Zaman aralığı rastgele belirleniyor (örneğin None veya belirli bir aralık)
        time_window = None  # İsteğe bağlı olarak zaman aralığı eklenebilir
        if random.random() > 0.7:  # %30 ihtimalle zaman aralığı olsun
            start_hour = random.randint(9, 15)
            end_hour = random.randint(start_hour, 17)
            start_minute = random.randint(0, 59)
            end_minute = random.randint(0, 59)
            time_window = (f"{start_hour:02d}:{start_minute:02d}", f"{end_hour:02d}:{end_minute:02d}")
        delivery_points.append(DeliveryPoint(point_id, location, weight, priority, time_window))
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

