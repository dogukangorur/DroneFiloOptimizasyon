
# entities.py
from a_star_solver import a_star_search

class Drone:
    """
    Batarya/KPI metriklerini Prometheus'a yazan ve
    kritik eşikte otomatik Return-Home yapan genişletilmiş Drone sınıfı.
    """
    # Prometheus metrikleri sınıf değişkeni olarak atanacak
    BATTERY_PCT = None
    FAILSAFE_COUNT = None

    def __init__(self, drone_id, max_weight, battery_capacity,
                 speed, start_pos):
        self.drone_id = drone_id
        self.max_weight = max_weight
        self.battery_capacity = battery_capacity
        self.current_battery = battery_capacity
        self.speed = speed
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.current_weight = 0.0
        self.is_busy = False

        # ↪️ Fail-safe alanları
        self.home_pos = start_pos          # Dönüş hedefi
        self.critical_pct = 20             # %20 altı = kritik
        self.last_node_id = f"D{drone_id}_START"
        self.battery_history = []      #  yüzde cinsinden pil seyri
        self.time_ticks      = []      #  anlık simülasyon adımı/süresi

    # ------------------------------------------------------------------ #
    def __str__(self):
        pct = 100 * self.current_battery / self.battery_capacity
        return (f"Drone {self.drone_id} | Ağırlık: {self.max_weight:.1f}kg | "
                f"Pil: {pct:.1f}% | Konum: {self.current_pos}")

    # ------------------------------------------------------------------ #
    def return_home(self, adj_list, nodes_map, nfzs):
        """
        Batarya kritik olduğunda en kısa güvenli rotayla kalkış noktasına döner.
        Dönüş başarılıysa True döner.
        """
        if (self.current_battery / self.battery_capacity) * 100 >= self.critical_pct:
            return False  # hâlâ yeterli pil var

        current_node = self.last_node_id
        goal_node = f"D{self.drone_id}_START"

        path, cost = a_star_search(adj_list, nodes_map, nfzs,
                                   current_node, goal_node)
        if not path:
            return False  # Yol bulunamadı → acil iniş senaryosu vb.

        # Pil düşür ve metriği güncelle
        self.current_battery -= cost * 0.5
        pct = 100 * self.current_battery / self.battery_capacity
        if self.__class__.BATTERY_PCT:
            self.__class__.BATTERY_PCT.labels(drone_id=self.drone_id).set(pct)
        if self.__class__.FAILSAFE_COUNT:
            self.__class__.FAILSAFE_COUNT.labels(drone_id=self.drone_id).inc()

        # Durum güncelle
        self.current_pos = self.home_pos
        self.last_node_id = goal_node
        self.is_busy = False
        print(f"⚠️  Drone {self.drone_id} kritik seviye → Evine döndü (kost = {cost:.1f})")
        return True

class DeliveryPoint:
    def __init__(self, point_id, location, weight, priority, time_window=None, delivered=False):
        self.point_id = point_id
        self.location = location
        self.weight = weight
        self.priority = priority
        self.time_window = time_window
        self.delivered = delivered

    def __str__(self):
        return (f"Teslimat ID: {self.point_id}, Konum: {self.location}, Ağırlık: {self.weight}kg, "
                f"Öncelik: {self.priority}, Zaman Aralığı: {self.time_window}, "
                f"Teslim Edildi: {self.delivered}")


class NoFlyZone:
    def __init__(self, zone_id, coordinates, start_time=None, end_time=None):
        self.zone_id = zone_id
        self.coordinates = coordinates
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return (f"Yasak Bölge ID: {self.zone_id}, Koordinatlar: {self.coordinates}, "
                f"Aktif Zaman: {self.start_time}-{self.end_time}")

