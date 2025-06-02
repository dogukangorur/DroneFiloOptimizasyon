import heapq


from utils import calculate_distance, is_point_in_polygon, segment_crosses_polygon, is_time_in_range, parse_time_str
from datetime import datetime

def reconstruct_path(came_from, current, goal):
    """A* algoritmasında bulunan yolu geri oluşturur"""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    
    return list(reversed(total_path))


def heuristic(coords1, coords2):
    """İki koordinat arasındaki Öklid mesafesini hesaplar (kuş uçuşu mesafe)"""
    return ((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2) ** 0.5


def a_star_search(adj_list, nodes_map, nfzs, start_node, goal_node):
    if start_node not in adj_list or goal_node not in adj_list:
        return None, float('inf')
    
    
    def heuristic(node1, node2):
        x1, y1 = nodes_map[node1]['coords']
        x2, y2 = nodes_map[node2]['coords']
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    
    open_set = [(0, start_node)]  # (f_score, node)
    
   
    g_score = {node: float('inf') for node in adj_list}
    g_score[start_node] = 0
    
    
    f_score = {node: float('inf') for node in adj_list}
    f_score[start_node] = heuristic(start_node, goal_node)
    
    
    came_from = {}
    
    
    closed_set = set()
    
    while open_set:
       
        current_f, current = heapq.heappop(open_set)
        
        if current == goal_node:
           
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, g_score[goal_node]
        
        closed_set.add(current)
        
        
        for neighbor, cost in adj_list[current]:
            if neighbor in closed_set:
                continue
                
            
            tentative_g = g_score[current] + cost
            
            if tentative_g < g_score[neighbor]:
                
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal_node)
                
                
                if all(node != neighbor for _, node in open_set):
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    
    return None, float('inf')