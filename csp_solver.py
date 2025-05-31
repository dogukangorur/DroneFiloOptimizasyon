# csp_solver.py

from utils import calculate_distance, is_point_in_polygon
from a_star_solver import a_star_search
from datetime import datetime


class CSPSolver:
    def __init__(self, deliveries, drones, adj_list, nodes_map, nfzs):
        self.deliveries = deliveries      # Liste[DeliveryPoint]
        self.drones = drones              # Liste[Drone]
        self.adj_list = adj_list          # nodes_map ve NFZ kontrolleriyle oluşturuldu
        self.nodes_map = nodes_map
        self.nfzs = nfzs

        # Her dronun başlangıç konumu ve bataryası
        # (entities.Drone sınıfının current_battery özniteliği zaten var.)
        for dr in self.drones:
            dr.current_location = dr.start_pos  # Yeni öznitelik: hangi noktada bekliyor
            # dr.current_battery zaten mevcut olmalı

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
        """
        Yeni yapı:
        - Atanmamış teslimatlar listesini baştan oluştururuz.
        - Döngü: Atanmamış teslimat kaldığı ve en az bir dron atama yaptığı sürece devam eder.
        """
        print("CSP çözümü başlatılıyor...")
        assignments = {}  # {delivery_id: drone_id}
        unassigned = [d for d in self.deliveries if not is_point_in_polygon(d.location, self.nfzs[0].coordinates) 
                      if self.nfzs] if self.nfzs else list(self.deliveries)
        # Yukarıda: teslimatı NFZ içinde olanları çıkarıyoruz. Eğer nfzs listesi boşsa, hepsi valid.

        # İsterseniz zaman penceresine burada müdahale edebilirsiniz:
        # (Aşağıdaki zaman kontrolünü tamamen kaldırdım, 
        #  ancak gerçek çalışma durumunda yorum satırını kaldırıp tekrar aktive edebilirsiniz.)
        # now = datetime.now().replace(second=0, microsecond=0)

        # Öncelikli olarak "daha yüksek priority" olan teslimatları önce deneyelim:
        unassigned.sort(key=lambda t: t.priority, reverse=True)

        # Bu döngü, "unassigned" listesinde öğe kaldığı ve
        # bu turda en az bir atama yapılabildiği sürece devam eder.
        while True:
            atama_yapildi = False

            # Zaman filtresi eklemek isterseniz burada “d.time_window” kontrolü yapabilirsiniz.

            for delivery in unassigned[:]:  # unassigned’ın bir kopyası üzerinde dönüyoruz
                best_drone = None
                best_cost = float("inf")

                for drone in self.drones:
                    # 1) Ağırlık kapasitesi kontrolü
                    if not self.check_drone_capacity(drone, delivery):
                        continue

                    # 2) Drone'un şimdiki konumu (string ID) gerekiyor.
                    #    Eğer dr.current_location = (x,y) ise bunu node_id’ye dönüştüreceğiz.
                    #    Bizim nodes_map, "D{drone_id}_START" veya teslimat ID ("101", "105") gibi string düğümler içeriyor.
                    #    Bu nedenle, eğer dr.current_location hâlâ start_pos ise start_node o dronun "D{id}_START" düğümü:
                    #    (Sonrasında dr.current_location = delivery.location şeklinde güncellenecek.)
                    if hasattr(drone, "last_node_id"):
                        start_node = drone.last_node_id
                    else:
                        start_node = f"D{drone.drone_id}_START"

                    delivery_node = str(delivery.point_id)

                    # 3) A* ile yol ve cost kontrolü
                    path_valid, cost = self.check_path_validity(start_node, delivery_node)
                    if not path_valid:
                        continue

                    # 4) Pil kullanımı kontrolü
                    battery_usage = self.estimate_battery_usage(cost, drone, delivery.weight)
                    if battery_usage > drone.current_battery:
                        continue

                    # 5) En düşük maliyetli dron araması
                    if cost < best_cost:
                        best_cost = cost
                        best_drone = drone

                # Eğer bu teslimata atanabilecek bir dron bulunduysa kaydedelim
                if best_drone:
                    # 6) Atama işlemi
                    drone = best_drone
                    usage = self.estimate_battery_usage(best_cost, drone, delivery.weight)
                    drone.current_battery -= usage
                    # Drone'un şimdiki düğümünü "delivery.point_id" node ID'si olarak güncelleyelim
                    drone.last_node_id = str(delivery.point_id)

                    assignments[delivery.point_id] = drone.drone_id
                    delivery.delivered = True

                    print(f"Teslimat {delivery.point_id} → Dron {drone.drone_id} | Maliyet: {best_cost:.2f} | Pil Kalan: {drone.current_battery:.2f}")

                    # Bu teslimat, unassigned listesinden çıkarılıyor
                    unassigned.remove(delivery)
                    atama_yapildi = True

            # Eğer bu turda hiç atama yapılmadıysa veya unassigned boşsa döngüden çık
            if not atama_yapildi or not unassigned:
                break

        print(f"Sonuç: Toplam {len(assignments)} teslimat atandı. {len(unassigned)} teslimat atanamadı.")
        return assignments
