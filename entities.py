
# entities.py

class Drone:
    def __init__(self, drone_id, max_weight, battery_capacity, speed, start_pos):
        self.drone_id = drone_id
        self.max_weight = max_weight
        self.battery_capacity = battery_capacity
        self.current_battery = battery_capacity
        self.speed = speed
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.current_weight = 0.0
        self.is_busy = False

    def __str__(self):
        return (f"Drone ID: {self.drone_id}, Max Ağırlık: {self.max_weight}kg, "
                f"Pil: {self.current_battery}/{self.battery_capacity}, Hız: {self.speed}, "
                f"Konum: {self.current_pos}, Yük: {self.current_weight}kg, "
                f"Meşgul: {'Evet' if self.is_busy else 'Hayır'}")


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

