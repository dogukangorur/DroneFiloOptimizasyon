
# a_star_solver.py

import heapq
from utils import calculate_distance, segment_crosses_polygon

def a_star_search(adjacency_list, nodes_map, nfzs_list, start_node_id, goal_node_id):
    """
    A* algoritması ile en kısa yol bulma.
    """
    open_set = []
    heapq.heappush(open_set, (0, 0, start_node_id))
    g_costs = {node_id: float('inf') for node_id in adjacency_list}
    g_costs[start_node_id] = 0
    came_from = {}

    while open_set:
        _, current_g_cost, current_node_id = heapq.heappop(open_set)

        if current_node_id == goal_node_id:
            path = []
            while current_node_id in came_from:
                path.append(current_node_id)
                current_node_id = came_from[current_node_id]
            path.reverse()
            return path, g_costs[goal_node_id]

        current_coords = nodes_map[current_node_id]['coords']
        for neighbor_node_id, cost in adjacency_list.get(current_node_id, []):
            neighbor_coords = nodes_map[neighbor_node_id]['coords']

            # NFZ kontrolü
            if any(segment_crosses_polygon(current_coords, neighbor_coords, nfz.coordinates) for nfz in nfzs_list):
                continue

            tentative_g_cost = g_costs[current_node_id] + cost
            if tentative_g_cost < g_costs[neighbor_node_id]:
                g_costs[neighbor_node_id] = tentative_g_cost
                came_from[neighbor_node_id] = current_node_id
                heuristic_cost = calculate_distance(neighbor_coords, nodes_map[goal_node_id]['coords'])
                heapq.heappush(open_set, (tentative_g_cost + heuristic_cost, tentative_g_cost, neighbor_node_id))

    return [], float('inf')

