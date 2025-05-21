from utils import calculate_distance, is_time_in_range, is_point_in_polygon, segment_crosses_polygon, parse_time_str
from entities import Drone, DeliveryPoint, NoFlyZone
from graph_utils import build_graph
from a_star_solver import a_star_search
from csp_solver import CSPSolver
from ga_optimizer import GAOptimizer
from plot_utils import plot_routes
from plot_utils import plot_routes

# data_generator.py'den gerekli fonksiyonları içe aktarın
from data_generator import generate_random_drones, generate_random_delivery_points, generate_fixed_no_fly_zones
import random # random.seed() için

def main():
    # random.seed() satırını siliyoruz veya yorum satırı yapıyoruz ki her çalıştırmada farklı rastgele veriler oluşsun
    # random.seed(42) # Bu satırı sildim veya yorum satırı yaptım

    MAX_MAP_X = 1000
    MAX_MAP_Y = 1000

    # --- Dronelar ---
    print("\n--- Drones Initialized ---")
    # data_generator.py'den 5 adet rastgele drone üretin
    num_drones_to_generate = 5
    drones_list = generate_random_drones(num_drones_to_generate, MAX_MAP_X, MAX_MAP_Y)

    for drone in drones_list:
        print(drone)

    # --- Teslimatlar ---
    print("\n--- Delivery Points Generated ---")
    # data_generator.py'den 20 adet rastgele teslimat noktası üretin
    num_deliveries_to_generate = 20
    deliveries_list = generate_random_delivery_points(num_deliveries_to_generate, MAX_MAP_X, MAX_MAP_Y)

    for delivery in deliveries_list:
        print(delivery)

    # --- Yasak bölgeler ---
    print("\n--- No-Fly Zones Initialized ---")
    # data_generator.py'den sabit no-fly zone'ları üretin
    nfzs_list = generate_fixed_no_fly_zones()

    for nfz in nfzs_list:
        print(nfz)


    # Graf oluştur
    print("\n--- Graph Structure Building ---")
    # Graf oluştururken yeni oluşturulan listeleri kullanın
    nodes_map, adj_list = build_graph(drones_list, deliveries_list)

    # CSP Çözücü
    print("\n--- Constraint Satisfaction Problem (CSP) ---")
    # CSPSolver'ı doğru listelerle başlatın ve nfzs_list'i iletin
    csp_solver = CSPSolver(deliveries_list, drones_list, adj_list, nodes_map, nfzs_list)

    # CSP Çözümü
    delivery_assignments_csp = csp_solver.solve()

    # Görselleştirme - CSP
    print("\n--- CSP Map Plotting ---")
    # plot_routes fonksiyonuna nfzs_list ve adj_list'i iletin
    plot_routes(drones_list, deliveries_list, delivery_assignments_csp, nodes_map, nfzs_list, adj_list)


    # Genetik Algoritma
    print("\n--- Genetic Algorithm (GA) ---")
    # GAOptimizer'ı yeni oluşturulan listelerle başlatın ve nfzs_list'i iletin
    ga_solver = GAOptimizer(drones_list, deliveries_list, nfzs_list, nodes_map, adj_list)
    ga_assignments = ga_solver.run()

    print("\n--- GA Result ---")
    # GA sonuçlarını yazdırma (daha önce yaptığımız gibi delivery_point nesnesinden bilgi alarak)
    for d_id, dr_id in ga_assignments.items():
         # point_id'yi DeliveryPoint nesnesinden alarak yazdırın
         delivery_point = next((dp for dp in deliveries_list if dp.point_id == d_id), None)
         if delivery_point:
            print(f"  Teslimat {delivery_point.point_id} -> Dron {dr_id}")
         else:
             print(f"  Teslimat ID {d_id} için bilgi bulunamadı -> Dron {dr_id}")

    # Görselleştirme - GA
    print("\n--- GA Map Plotting ---")
    # plot_routes fonksiyonuna nfzs_list ve adj_list'i iletin
    plot_routes(drones_list, deliveries_list, ga_assignments, nodes_map, nfzs_list, adj_list)

    # A* örneği (isteğe bağlı, test amaçlı)
    # A* için başlangıç ve bitiş noktalarını dinamik olarak belirlemek gerekebilir
    # Şu anki kod dinamik ID'ler kullanıyor (oluşturulan ilk drone ve ilk teslimat)
    print("\n--- A* Algorithm Example (Start) ---")
    if drones_list and deliveries_list:
        first_drone_start_node = f"D{drones_list[0].drone_id}_START"
        first_delivery_goal_node = str(deliveries_list[0].point_id)
        print(f"  Calculating path from {first_drone_start_node} to {first_delivery_goal_node}")
        # a_star_search fonksiyonuna nfzs_list'i zaten iletiyorduk
        found_path, total_cost = a_star_search(adj_list, nodes_map, nfzs_list, first_drone_start_node, first_delivery_goal_node)

        if found_path:
            print(f"  Path Found: {found_path}")
            print(f"  Total Cost: {total_cost:.2f}")
        else:
            print(f"  No Path Found or Path is invalid from {first_drone_start_node} to {first_delivery_goal_node}!")
    else:
        print("  Cannot run A* example: No drones or deliveries generated.")

    print("\nDrone Fleet Optimization Project Completed.")

if __name__ == "__main__":
    main()