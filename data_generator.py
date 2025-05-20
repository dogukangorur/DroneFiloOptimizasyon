# data_generator.py
import random
from entities import Drone, DeliveryPoint, NoFlyZone # entities.py dosyanızdan import ediyoruz
# Eğer utils.py'deki fonksiyonlar gerekirse (örn: NFZ koordinatları üretirken):
# from utils import calculate_distance 

def generate_random_drones(num_drones, max_x, max_y):
    drones = []
    for i in range(num_drones):
        drone_id = i + 1
        max_weight = round(random.uniform(2.0, 10.0), 1) # Örnek: 2.0 ile 10.0 kg arası
        
        # Pil değeri üretiliyor ve Drone nesnesine iletiliyor
        # Pil değeri genellikle maksimum kapasite olarak başlar
        battery_capacity = random.randint(5000, 20000) # Örnek: 5000 ile 20000 birim arası pil
        battery = battery_capacity # Başlangıçta pil tam dolu
        
        speed = round(random.uniform(5.0, 20.0), 1) # Örnek: 5.0 ile 20.0 birim/sn arası
        location = (random.randint(0, max_x), random.randint(0, max_y)) # Başlangıç konumları
        # Drone nesnesi oluşturulurken battery değeri 3. parametre olarak iletiliyor
        drones.append(Drone(drone_id, max_weight, battery, speed, location)) 
        
    return drones

def generate_random_delivery_points(num_points, max_x, max_y):
    delivery_points = []
    base_id = 101 # Teslimat ID'leri için başlangıç değeri
    for i in range(num_points):
        point_id = base_id + i
        location = (random.randint(0, max_x), random.randint(0, max_y))
        
        # Ağırlık değeri üretiliyor ve DeliveryPoint'e iletiliyor
        weight = round(random.uniform(1.0, 5.0), 1) # Örnek: 1.0 ile 5.0 kg arasında rastgele ağırlık
        
        priority = random.randint(1, 5) # Örnek: 1 (en düşük) ile 5 (en yüksek) arasında öncelik
        
        # Zaman aralığı rastgele belirleniyor (örneğin None veya belirli bir aralık)
        time_window = None
        # İsteğe bağlı olarak zaman aralığı eklenebilir
        # if random.random() > 0.7: # %30 ihtimalle zaman aralığı olsun
        #     start_hour = random.randint(9, 15)
        #     end_hour = random.randint(start_hour, 17)
        #     start_minute = random.randint(0, 59)
        #     end_minute = random.randint(0, 59)
        #     time_window = (f"{start_hour:02d}:{start_minute:02d}", f"{end_hour:02d}:{end_minute:02d}")
        delivery_points.append(DeliveryPoint(point_id, location, weight, priority, time_window))
        
    return delivery_points

def generate_random_no_fly_zones(count: int, max_coord_x=1000, max_coord_y=1000) -> list[NoFlyZone]:
    """Rastgele No-Fly Zone nesneleri üretir."""
    no_fly_zones = []
    for i in range(count):
        zone_id = i + 1001 # Diğer ID'lerle karışmaması için
        num_vertices = random.randint(3, 6) # Poligon için köşe sayısı
        coordinates = []
        # Basit bir rastgele poligon oluşturma (dışbükey olmayabilir, daha gelişmiş algoritmalar gerekebilir)
        # Şimdilik basitçe rastgele noktalar üretiyoruz
        for _ in range(num_vertices):
            x = random.randint(0, max_coord_x // 2) + (max_coord_x // 4) # Alanın ortasına yakın
            y = random.randint(0, max_coord_y // 2) + (max_coord_y // 4)
            coordinates.append((x,y))
        
        # Zaman aralığı (PDF'deki (09:30, 11:00) formatına dikkat)
        # Yine string veya dakika cinsinden int olarak tutulabilir
        active_time_start_options = [None, "09:30", "10:30"]
        active_time_end_options = [None, "11:00", "12:00"]
        start_time_str = random.choice(active_time_start_options)
        end_time_str = random.choice(active_time_end_options)
        active_time = (start_time_str, end_time_str) if start_time_str and end_time_str else (None, None)

        no_fly_zones.append(NoFlyZone(zone_id, coordinates, active_time[0], active_time[1])) # entities.py'deki __init__'e göre
    return no_fly_zones


if __name__ == '__main__':
    # Test için
    num_drones = 5
    num_deliveries = 20
    num_nfzs = 2

    drones_list = generate_random_drones(num_drones)
    deliveries_list = generate_random_delivery_points(num_deliveries)
    nfzs_list = generate_random_no_fly_zones(num_nfzs)

    print(f"--- {num_drones} Drone Oluşturuldu ---")
    for drone in drones_list:
        print(drone)

    print(f"\n--- {num_deliveries} Teslimat Noktası Oluşturuldu ---")
    for point in deliveries_list:
        print(point)

    print(f"\n--- {num_nfzs} No-Fly Zone Oluşturuldu ---")
    for nfz in nfzs_list:
        print(nfz)