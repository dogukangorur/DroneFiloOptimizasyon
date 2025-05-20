# main.py

from utils import calculate_distance, is_time_in_range, is_point_in_polygon, segment_crosses_polygon, parse_time_str
from entities import Drone, DeliveryPoint, NoFlyZone
from graph_utils import build_graph
from a_star_solver import a_star_search
from csp_solver import CSPSolver
from ga_optimizer import GAOptimizer
from plot_utils import plot_routes

def main():
    MAX_MAP_X = 1000
    MAX_MAP_Y = 1000

    # Dronelar
    print("\n--- Drones Initialized ---")
    drones_data = [
        {"drone_id": 1, "max_weight": 10.0, "battery_capacity": 7160, "speed": 18.0, "start_pos": (59, 698)},
        {"drone_id": 2, "max_weight": 4.2, "battery_capacity": 15224, "speed": 16.7, "start_pos": (989, 424)},
        {"drone_id": 3, "max_weight": 3.6, "battery_capacity": 11172, "speed": 19.5, "start_pos": (417, 75)},
        {"drone_id": 4, "max_weight": 7.5, "battery_capacity": 18500, "speed": 20.5, "start_pos": (150, 800)},
        {"drone_id": 5, "max_weight": 6.0, "battery_capacity": 14000, "speed": 17.0, "start_pos": (750, 200)}
    ]
    drones_list = [Drone(**data) for data in drones_data]
    for drone in drones_list:
        print(drone)

    # Teslimatlar
    print("\n--- 10 Delivery Points Generated ---")
    deliveries_data = [
        {"point_id": 101, "location": (592, 666), "weight": 3.6, "priority": 3, "time_window": ("09:00", "12:00")},
        {"point_id": 102, "location": (120, 52), "weight": 4.2, "priority": 4, "time_window": ("10:00", "13:00")},
        {"point_id": 103, "location": (224, 33), "weight": 1.0, "priority": 5, "time_window": None},
        {"point_id": 104, "location": (412, 108), "weight": 1.3, "priority": 3, "time_window": ("09:30", "10:30")},
        {"point_id": 105, "location": (292, 543), "weight": 3.9, "priority": 3, "time_window": None},
        {"point_id": 106, "location": (424, 425), "weight": 1.2, "priority": 2, "time_window": None},
        {"point_id": 107, "location": (81, 998), "weight": 3.2, "priority": 4, "time_window": None},
        {"point_id": 108, "location": (905, 564), "weight": 2.4, "priority": 3, "time_window": None},
        {"point_id": 109, "location": (944, 22), "weight": 3.3, "priority": 3, "time_window": None},
        {"point_id": 110, "location": (685, 634), "weight": 1.8, "priority": 3, "time_window": None}
    ]
    deliveries_list = [DeliveryPoint(**data) for data in deliveries_data]
    for delivery in deliveries_list:
        print(delivery)

    # Yasak bölgeler
    print("\n--- 2 No-Fly Zones Generated ---")
    nfzs_data = [
        {"zone_id": 1001, "coordinates": [(542, 511), (365, 272), (534, 526)], "start_time": "09:30", "end_time": "11:00"},
        {"zone_id": 1002, "coordinates": [(526, 686), (362, 368), (486, 303), (727, 396), (670, 271)], "start_time": "10:30", "end_time": "12:00"}
    ]
    nfzs_list = [NoFlyZone(**data) for data in nfzs_data]
    for nfz in nfzs_list:
        print(nfz)

    # Graf oluştur
    print("\n--- Graph Structure Building ---")
    nodes_map, adj_list = build_graph(drones_list, deliveries_list)
    csp_solver = CSPSolver(deliveries_list, drones_list, adj_list, nodes_map, nfzs_list)

    # A* örneği
    print("\n--- A* Algorithm Example (Start) ---")
    found_path, total_cost = a_star_search(adj_list, nodes_map, nfzs_list, "D1_START", "101")
    if found_path:
        print(f"  Path Found: {found_path}")
        print(f"  Total Cost: {total_cost:.2f}")
    else:
        print("  No Path Found or Path is invalid!")

    # CSP Çözümü
    print("\n--- Constraint Satisfaction Problem (CSP) ---")
    delivery_assignments = csp_solver.solve()

    # Görselleştirme
    print("\n--- CSP Harita Çizimi ---")
    plot_routes(drones_list, deliveries_list, delivery_assignments, nodes_map, nfzs_list, adj_list)

    # Genetik Algoritma
    print("\n--- Genetik Algoritma (GA) ---")
    ga_solver = GAOptimizer(drones_list, deliveries_list, nfzs_list, nodes_map, adj_list)
    ga_assignments = ga_solver.run()

    print("\n--- GA Sonucu ---")
    for d_id, dr_id in ga_assignments.items():
        print(f"  Teslimat {d_id} -> Dron {dr_id}")

    # GA Haritası
    print("\n--- GA Harita Çizimi ---")
    plot_routes(drones_list, deliveries_list, ga_assignments, nodes_map, nfzs_list)

    print("\nDrone Filo Optimizasyon Projesi Tamamlandı.")

if __name__ == "__main__":
    main()
