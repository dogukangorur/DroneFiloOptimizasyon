
# csp_solver.py

from utils import calculate_distance
from a_star_solver import a_star_search
from datetime import datetime
from utils import parse_time_str, is_time_in_range

class CSPSolver:
    def __init__(self, deliveries, drones, adj_list, nodes_map, nfzs):
        self.deliveries = deliveries
        self.drones = drones
        self.adj_list = adj_list
        self.nodes_map = nodes_map
        self.nfzs = nfzs
        self.build_connectivity_graph()

    def build_connectivity_graph(self):
        """
        Grafı oluşturur ve her düğüm arasındaki bağlantıları ve mesafeleri hesaplar.
        """
        # Düğümler arası bağlantıları hesapla
        for node_id_1, details_1 in self.nodes_map.items():
            coords_1 = details_1['coords']
            for node_id_2, details_2 in self.nodes_map.items():
                if node_id_1 != node_id_2:
                    coords_2 = details_2['coords']
                    distance = calculate_distance(coords_1, coords_2)
                    self.adj_list[node_id_1].append((node_id_2, distance))

        print(f"Graf oluşturuldu, {len(self.nodes_map)} düğüm ve {sum(len(neighbors) for neighbors in self.adj_list.values())} bağlantı var.")
        
    def check_path_validity(self, drone_node, delivery_node):
        """
        Belirli bir dron ve teslimat noktası arasındaki yolun geçerli olup olmadığını kontrol eder.
        """
        path, cost = a_star_search(self.adj_list, self.nodes_map, self.nfzs, drone_node, delivery_node)
        return len(path) > 0, cost
    
    def check_drone_capacity(self, drone, delivery):
        """
        Dronun teslimatı taşıyabilecek kapasitede olup olmadığını kontrol eder.
        """
        return drone.max_weight >= delivery.weight
    
    def estimate_battery_usage(self, distance, drone, delivery_weight):
        """
        Belirli bir mesafe ve yük için tahmini pil kullanımını hesaplar.
        """
        # Basit bir pil kullanımı hesaplaması:
        # Mesafe, yük ve dronun kendi ağırlığını hesaba katar
        base_usage = distance * 0.5  # Her birim mesafe başına 0.5 birim pil
        weight_factor = 1.0 + (delivery_weight / drone.max_weight) * 0.5  # Ağırlık faktörü
        return base_usage * weight_factor
    
    def solve(self):
        print("CSP çözümü başlatılıyor...")
        assignments = {}
        unassigned_deliveries = list(self.deliveries)
        
        unassigned_deliveries.sort(key=lambda d: d.priority, reverse=True)
        
        now = datetime.now().replace(year=1900, month=1, day=1)

        for delivery in unassigned_deliveries:
            # ⏱ Zaman kontrolü
            if delivery.time_window:
                start_time = parse_time_str(delivery.time_window[0])
                end_time = parse_time_str(delivery.time_window[1])
                if not is_time_in_range(start_time, end_time, now):
                    print(f"  ⏱ Teslimat {delivery.point_id} zaman aralığında değil, atlanıyor.")
                    continue

            best_drone = None
            best_cost = float('inf')
            
            for drone in self.drones:
                if drone.is_busy or not self.check_drone_capacity(drone, delivery):
                    continue
                
                drone_node = f"D{drone.drone_id}_START"
                delivery_node = str(delivery.point_id)
                
                path_valid, cost = self.check_path_validity(drone_node, delivery_node)
                if not path_valid:
                    continue
                
                battery_usage = self.estimate_battery_usage(cost, drone, delivery.weight)
                if battery_usage > drone.current_battery:
                    continue
                
                if cost < best_cost:
                    best_cost = cost
                    best_drone = drone
            
            if best_drone:
                best_drone.is_busy = True
                best_drone.current_battery -= self.estimate_battery_usage(best_cost, best_drone, delivery.weight)
                assignments[delivery.point_id] = best_drone.drone_id
                delivery.delivered = True
                print(f"Teslimat {delivery.point_id} → Dron {best_drone.drone_id}, Maliyet: {best_cost:.2f}, Pil: {self.estimate_battery_usage(best_cost, best_drone, delivery.weight):.2f}")

        print(f"Toplam {len(assignments)} teslimat atandı. {len(unassigned_deliveries) - len(assignments)} teslimat atanamadı.")
        return assignments

