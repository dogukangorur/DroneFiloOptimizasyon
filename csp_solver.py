
# csp_solver.py

from utils import calculate_distance, is_point_in_polygon
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
        
    def check_path_validity(self, start_node, end_node):
        """İki düğüm arasında geçerli bir yol olup olmadığını kontrol eder."""
        if start_node not in self.adj_list or end_node not in self.adj_list:
            return False, float('inf')
            
        path, cost = a_star_search(self.adj_list, self.nodes_map, self.nfzs, start_node, end_node)
        
        if not path or cost == float('inf'):
            return False, float('inf')
            
        return True, cost
    
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
        
        # Teslimat noktalarını NFZ içinde olmayanlarla sınırla ve önceliğe göre sırala
        valid_deliveries = []
        for delivery in self.deliveries:
            is_in_nfz = False
            for nfz in self.nfzs:
                if is_point_in_polygon(delivery.location, nfz.coordinates):
                    is_in_nfz = True
                    break
                    
            if not is_in_nfz:
                valid_deliveries.append(delivery)
                
        valid_deliveries.sort(key=lambda d: d.priority, reverse=True)
        
        now = datetime.now().replace(second=0, microsecond=0)
        
        for delivery in valid_deliveries:
            # Zaman kontrolü
            if delivery.time_window:
                start_time_str, end_time_str = delivery.time_window
                
                # Sadece saati kontrol edelim
                current_hour = now.hour
                start_hour = int(start_time_str.split(':')[0])
                end_hour = int(end_time_str.split(':')[0])
                
                if not (start_hour <= current_hour <= end_hour):
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
                print(f"Teslimat {delivery.point_id} → Dron {best_drone.drone_id}, Maliyet: {best_cost:.2f}, Pil: {best_drone.current_battery:.2f}")
                
        print(f"Toplam {len(assignments)} teslimat atandı. {len(valid_deliveries) - len(assignments)} teslimat atanamadı.")
        return assignments

