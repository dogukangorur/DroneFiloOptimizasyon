import heapq
from utils import calculate_distance, segment_crosses_polygon, is_time_in_range, parse_time_str
from datetime import datetime

def a_star_search(adjacency_list, nodes_map, nfzs_list, start_node_id, goal_node_id):
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
            path.append(start_node_id)
            path.reverse()
            return path, g_costs[goal_node_id]

        current_coords = nodes_map[current_node_id]['coords']
        for neighbor_node_id, cost in adjacency_list.get(current_node_id, []):
            neighbor_coords = nodes_map[neighbor_node_id]['coords']

            now = datetime.now().replace(year=1900, month=1, day=1)
            blocked = False
            for nfz in nfzs_list:
                if nfz.start_time and nfz.end_time:
                    nfz_start = parse_time_str(nfz.start_time)
                    nfz_end = parse_time_str(nfz.end_time)
                    if not is_time_in_range(nfz_start, nfz_end, now):
                        continue
                if segment_crosses_polygon(current_coords, neighbor_coords, nfz.coordinates):
                    blocked = True
                    break
            if blocked:
                continue

            tentative_g_cost = g_costs[current_node_id] + cost
            if tentative_g_cost < g_costs[neighbor_node_id]:
                g_costs[neighbor_node_id] = tentative_g_cost
                came_from[neighbor_node_id] = current_node_id
                heuristic_cost = calculate_distance(neighbor_coords, nodes_map[goal_node_id]['coords'])
                heapq.heappush(open_set, (tentative_g_cost + heuristic_cost, tentative_g_cost, neighbor_node_id))

    return [], float('inf')