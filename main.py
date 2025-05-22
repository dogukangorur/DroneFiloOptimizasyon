from utils import calculate_distance, is_time_in_range, is_point_in_polygon, segment_crosses_polygon, parse_time_str
from entities import Drone, DeliveryPoint, NoFlyZone
from graph_utils import build_graph
from a_star_solver import a_star_search
from csp_solver import CSPSolver
from ga_optimizer import GAOptimizer
from plot_utils import plot_routes

from data_generator import generate_random_drones, generate_random_delivery_points, generate_fixed_no_fly_zones
import random

def main():
    MAX_MAP_X = 1000
    MAX_MAP_Y = 1000

    print("\n--- Drones Initialized ---")
    drones_list = generate_random_drones(5, MAX_MAP_X, MAX_MAP_Y)
    for drone in drones_list:
        print(drone)

    print("\n--- Delivery Points Generated ---")
    deliveries_list = generate_random_delivery_points(20, MAX_MAP_X, MAX_MAP_Y)
    for delivery in deliveries_list:
        print(delivery)

    print("\n--- No-Fly Zones Initialized ---")
    nfzs_list = generate_fixed_no_fly_zones()
    for nfz in nfzs_list:
        print(nfz)

    print("\n--- Graph Structure Building ---")
    nodes_map, adj_list = build_graph(drones_list, deliveries_list, nfzs_list)

    print("\n--- Constraint Satisfaction Problem (CSP) ---")
    csp_solver = CSPSolver(deliveries_list, drones_list, adj_list, nodes_map, nfzs_list)
    delivery_assignments_csp = csp_solver.solve()

    print("\n--- CSP Map Plotting ---")
    # 🔄 animate=False (statik çizim)
    plot_routes(drones_list, deliveries_list, delivery_assignments_csp, nodes_map, nfzs_list, adj_list, animate=False)

    print("\n--- Genetic Algorithm (GA) ---")
    ga_solver = GAOptimizer(drones_list, deliveries_list, nfzs_list, nodes_map, adj_list)
    ga_assignments = ga_solver.run()

    print("\n--- GA Result ---")
    for d_id, dr_id in ga_assignments.items():
        delivery_point = next((dp for dp in deliveries_list if dp.point_id == d_id), None)
        if delivery_point:
            print(f"  Teslimat {delivery_point.point_id} -> Dron {dr_id}")
        else:
            print(f"  Teslimat ID {d_id} için bilgi bulunamadı -> Dron {dr_id}")

    print("\n--- GA Map Plotting ---")
    # 🔄 animate=True (hareketli çizim)
    plot_routes(drones_list, deliveries_list, ga_assignments, nodes_map, nfzs_list, adj_list, animate=True)

    print("\n--- A* Algorithm Example (Start) ---")
    if drones_list and deliveries_list:
        first_drone_start_node = f"D{drones_list[0].drone_id}_START"
        first_delivery_goal_node = str(deliveries_list[0].point_id)
        print(f"  Calculating path from {first_drone_start_node} to {first_delivery_goal_node}")
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
