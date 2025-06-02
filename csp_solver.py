# csp_solver.py

from utils import calculate_distance, is_point_in_polygon
from a_star_solver import a_star_search
from datetime import datetime
from entities import Drone


class CSPSolver:
    def __init__(self, deliveries, drones, adj_list, nodes_map, nfzs):
        self.deliveries = deliveries      # Liste[DeliveryPoint]
        self.drones = drones              # Liste[Drone]
        self.adj_list = adj_list          # nodes_map ve NFZ kontrolleriyle oluşturuldu
        self.nodes_map = nodes_map
        self.nfzs = nfzs

        # Her dronun başlangıç konumu ve bataryası
        for dr in self.drones:
            dr.current_location = dr.start_pos  
           

    def check_path_validity(self, start_node, end_node):
        """
        start_node ve end_node string ID (ör. "D1_START" veya "105").
        Eğer NFZ engel yoksa ve A* bir yol bulduysa (path, cost) döner.
        """
        if start_node not in self.adj_list or end_node not in self.adj_list:
            return False, float("inf")

        path, cost = a_star_search(self.adj_list, self.nodes_map, self.nfzs, start_node, end_node)
        if not path or cost == float("inf"):
            return False, float("inf")

        return True, cost

    def check_drone_capacity(self, drone, delivery):
        """Dronun, teslimatın ağırlığını taşıyıp taşımayacağını kontrol eder."""
        return drone.max_weight >= delivery.weight

    def estimate_battery_usage(self, distance, drone, delivery_weight):
        """
        Pil kullanımı: mesafe ve ağırlığa basit bir katsayı uygular.
        (Daha önce base_usage=distance*0.5 idi; bu değeri koruyabilirsiniz.)
        """
        base_usage = distance * 0.5
        weight_factor = 1.0 + (delivery_weight / drone.max_weight) * 0.5
        return base_usage * weight_factor

    def solve(self):
      
        print("CSP çözümü başlatılıyor...")
        assignments = {}  # {delivery_id: drone_id}
        unassigned = [d for d in self.deliveries if not is_point_in_polygon(d.location, self.nfzs[0].coordinates) 
                      if self.nfzs] if self.nfzs else list(self.deliveries)
        
        unassigned.sort(key=lambda t: t.priority, reverse=True)

      
        while True:
            atama_yapildi = False

           

            for delivery in unassigned[:]:  
                best_drone = None
                best_cost = float("inf")

                for drone in self.drones:
                    #  Ağırlık kapasitesi kontrolü
                    if not self.check_drone_capacity(drone, delivery):
                        continue

                    if hasattr(drone, "last_node_id"):
                        start_node = drone.last_node_id
                    else:
                        start_node = f"D{drone.drone_id}_START"

                    delivery_node = str(delivery.point_id)

                    #  A* ile yol ve cost kontrolü
                    path_valid, cost = self.check_path_validity(start_node, delivery_node)
                    if not path_valid:
                        continue

                    #  Pil kullanımı kontrolü
                    battery_usage = self.estimate_battery_usage(cost, drone, delivery.weight)
                    if battery_usage > drone.current_battery:
                        continue

                    #  En düşük maliyetli dron araması
                    if cost < best_cost:
                        best_cost = cost
                        best_drone = drone

                # Eğer bu teslimata atanabilecek bir dron bulunduysa kaydedelim
                if best_drone:
                    #  Atama işlemi
                    drone = best_drone
                    usage = self.estimate_battery_usage(best_cost, drone, delivery.weight)
                    drone.current_battery -= usage
                    
                    pct = 100 * drone.current_battery / drone.battery_capacity
                    drone.battery_history.append(pct)            
                    drone.time_ticks.append(len(drone.battery_history))  

                    
                    drone.last_node_id = str(delivery.point_id)

                    assignments[delivery.point_id] = drone.drone_id
                    delivery.delivered = True

                    print(f"Teslimat {delivery.point_id} → Dron {drone.drone_id} | Maliyet: {best_cost:.2f} | Pil Kalan: {drone.current_battery:.2f}")

                   
                    unassigned.remove(delivery)
                    atama_yapildi = True

           
            if not atama_yapildi or not unassigned:
                break

        print(f"Sonuç: Toplam {len(assignments)} teslimat atandı. {len(unassigned)} teslimat atanamadı.")
        return assignments
