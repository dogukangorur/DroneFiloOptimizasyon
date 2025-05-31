import os
import time
from datetime import datetime

from utils import calculate_distance
from entities import Drone, DeliveryPoint, NoFlyZone
from graph_utils import build_graph
from a_star_solver import a_star_search
from csp_solver import CSPSolver
from ga_optimizer import GAOptimizer
from plot_utils import plot_routes
from data_generator import generate_random_drones, generate_random_delivery_points, generate_fixed_no_fly_zones

def main():
    MAX_MAP_X = 1000
    MAX_MAP_Y = 1000

    print("\n--- Drones Initialized ---")
    drones_list = generate_random_drones(5, MAX_MAP_X, MAX_MAP_Y)
    for drone in drones_list:
        print(f"Drone {drone.drone_id} | Konum: {drone.start_pos} | Kapasite: {drone.max_weight:.2f} kg | Batarya: {drone.current_battery:.2f} | Hız: {drone.speed:.2f}")

    print("\n--- Delivery Points Generated ---")
    deliveries_list = generate_random_delivery_points(20, MAX_MAP_X, MAX_MAP_Y)
    for delivery in deliveries_list:
        tw = f"{delivery.time_window[0]}-{delivery.time_window[1]}" if delivery.time_window else "None"
        print(f"Teslimat {delivery.point_id} | Konum: {delivery.location} | Ağırlık: {delivery.weight:.2f} kg | Öncelik: {delivery.priority} | Time Window: {tw}")

    print("\n--- No-Fly Zones Initialized ---")
    nfzs_list = generate_fixed_no_fly_zones()
    for nfz in nfzs_list:
        coords_str = ", ".join(f"({x},{y})" for x, y in nfz.coordinates)
        print(f"NFZ {nfz.zone_id} → Köşeler: [{coords_str}]")

    # 🎯 VERİLERİ TXT DOSYASINA KAYDET
    folder_name = "data_records"
    os.makedirs(folder_name, exist_ok=True)
    now = datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H-%M") + ".txt"
    file_path = os.path.join(folder_name, file_name)
    human_readable = now.strftime("%Y-%m-%d %H:%M")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Drone Filo Verisi - {human_readable}\n\n")

        f.write("--- Drones Initialized ---\n")
        for dr in drones_list:
            f.write(f"Drone {dr.drone_id} | Konum: {dr.start_pos} | Kapasite: {dr.max_weight:.2f} kg | Batarya: {dr.current_battery:.2f} | Hız: {dr.speed:.2f} \n")

        f.write("\n--- Delivery Points Generated ---\n")
        for d in deliveries_list:
            tw = f"{d.time_window[0]}-{d.time_window[1]}" if d.time_window else "None"
            f.write(f"Teslimat {d.point_id} | Konum: {d.location} | Ağırlık: {d.weight:.2f} kg | Öncelik: {d.priority} | Time Window: {tw}\n")

        f.write("\n--- No-Fly Zones Initialized ---\n")
        for nfz in nfzs_list:
            coords = ", ".join([f"({x},{y})" for x, y in nfz.coordinates])
            f.write(f"NFZ {nfz.zone_id} → Köşeler: [{coords}]\n")

    # GRAF OLUŞTUR
    print("\n--- Graph Structure Building ---")
    nodes_map, adj_list = build_graph(deliveries_list, drones_list, nfzs_list)

    # CSP
    print("\n--- Constraint Satisfaction Problem (CSP) ---")
    t0_csp = time.time()
    csp_solver = CSPSolver(deliveries_list, drones_list, adj_list, nodes_map, nfzs_list)
    delivery_assignments_csp = csp_solver.solve()
    t1_csp = time.time()
    csp_duration = t1_csp - t0_csp

    print("\n--- CSP Map Plotting ---")
    plot_routes(drones_list, deliveries_list, delivery_assignments_csp, nodes_map, nfzs_list, adj_list, animate=False)

    # GA
    print("\n--- Genetic Algorithm (GA) ---")
    t0_ga = time.time()
    ga_solver = GAOptimizer(drones_list, deliveries_list, nfzs_list, nodes_map, adj_list)
    ga_assignments = ga_solver.run()
    t1_ga = time.time()
    ga_duration = t1_ga - t0_ga

    print("\n--- GA Result ---")
    for d_id, dr_id in ga_assignments.items():
        print(f"  Teslimat {d_id} → Dron {dr_id}")

    print("\n--- GA Map Plotting ---")
    plot_routes(drones_list, deliveries_list, ga_assignments, nodes_map, nfzs_list, adj_list, animate=True)

    # A*
    print("\n--- A* for All GA Assignments ---")
    t0_astar_all = time.time()
    all_paths = {}
    for d_id, dr_id in ga_assignments.items():
        start_node = f"D{dr_id}_START"
        goal_node = str(d_id)
        found_path, total_cost = a_star_search(adj_list, nodes_map, nfzs_list, start_node, goal_node)
        if found_path:
            all_paths[d_id] = (found_path, total_cost)
            print(f"  Teslimat {d_id} için Dron {dr_id}: Path = {found_path}, Cost = {total_cost:.2f}")
        else:
            print(f"  Teslimat {d_id} için Dron {dr_id}: Path bulunamadı veya NFZ nedeniyle geçersiz!")
    t1_astar_all = time.time()
    a_star_all_duration = t1_astar_all - t0_astar_all

    print("\nDrone Fleet Optimization Project Completed.")

    # Metrikler
    total_deliveries = len(deliveries_list)
    completed_deliveries = len([p for p in all_paths.values() if p is not None])
    completion_pct = (completed_deliveries / total_deliveries) * 100 if total_deliveries > 0 else 0.0

    total_energy = 0.0
    for d_id, dr_id in ga_assignments.items():
        delivery_point = next((dp for dp in deliveries_list if dp.point_id == d_id), None)
        drone_obj = next((dr for dr in drones_list if dr.drone_id == dr_id), None)
        if delivery_point and drone_obj:
            dist = calculate_distance(drone_obj.start_pos, delivery_point.location)
            total_energy += dist

    avg_energy = (total_energy / completed_deliveries) if completed_deliveries > 0 else 0.0

    print("\n--- Özet Metrikler ---")
    print(f"Tamamlanan Teslimat Sayısı: {completed_deliveries}/{total_deliveries} (%{completion_pct:.2f})")
    print(f"Ortalama Enerji Tüketimi (ortalama mesafe): {avg_energy:.2f} birim")
    print(f"CSP Çalışma Süresi: {csp_duration:.3f} saniye")
    print(f"GA Çalışma Süresi: {ga_duration:.3f} saniye")
    print(f"A* (Tüm Atamalar) Çalışma Süresi: {a_star_all_duration:.3f} saniye")

if __name__ == "__main__":
    main()
