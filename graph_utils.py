from utils import calculate_distance, is_point_in_polygon, segment_crosses_polygon


NODE_TYPE_DRONE_START = 'drone_start'
NODE_TYPE_DELIVERY = 'delivery_point'
NODE_TYPE_NFZ_CORNER = 'nfz_corner'
NODE_TYPE_WAYPOINT = 'waypoint'
def build_graph(delivery_points, drones, nfzs=None):
    if nfzs is None:
        nfzs = []
        
    nodes_map = {}
    
    # Add drone start positions
    for drone in drones:
        node_id = f"D{drone.drone_id}_START"
        nodes_map[node_id] = {
            'coords': drone.start_pos,
            'type': NODE_TYPE_DRONE_START,
            'original_id': drone.drone_id
        }
    
    # Add delivery points
    for point in delivery_points:
        node_id = str(point.point_id)
        nodes_map[node_id] = {
            'type': NODE_TYPE_DELIVERY,
            'coords': point.location,
            'weight': point.weight,
            'priority': point.priority,
            'time_window': point.time_window,
            'original_id': point.point_id
        }
    
    # Add NFZ corners as navigation points
    for nfz in nfzs:
        for i, corner in enumerate(nfz.coordinates):
            node_id = f"NFZ{nfz.zone_id}_C{i}"
            nodes_map[node_id] = {
                'coords': corner,
                'type': NODE_TYPE_NFZ_CORNER,
                'nfz_id': nfz.zone_id
            }
    
    # Add additional waypoints around NFZs with safety margin
    safety_margin = 20  # meters
    for nfz in nfzs:
        coords = nfz.coordinates
        for i in range(len(coords)):
            start = coords[i]
            end = coords[(i + 1) % len(coords)]
            
            # Create waypoint at middle of edge, offset outward
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            # Calculate normal vector (perpendicular to edge)
            edge_vec_x = end[0] - start[0]
            edge_vec_y = end[1] - start[1]
            
            # Perpendicular vector (outward from NFZ)
            normal_x = -edge_vec_y
            normal_y = edge_vec_x
            
            # Normalize the normal vector
            length = (normal_x**2 + normal_y**2)**0.5
            if length > 0:
                normal_x /= length
                normal_y /= length
            
            # Create waypoint with safety margin
            safe_x = mid_x + safety_margin * normal_x
            safe_y = mid_y + safety_margin * normal_y
            
            # Check if point is outside NFZ
            if not is_point_in_polygon((safe_x, safe_y), coords):
                node_id = f"WP_NFZ{nfz.zone_id}_E{i}"
                nodes_map[node_id] = {
                    'coords': (safe_x, safe_y),
                    'type': NODE_TYPE_WAYPOINT,
                    'nfz_id': nfz.zone_id
                }
    
    # Create adjacency list with all possible safe connections
    adj_list = {node_id: [] for node_id in nodes_map}
    
    # Connect nodes if path doesn't intersect any NFZ
    for node_id_1, node_1 in nodes_map.items():
        for node_id_2, node_2 in nodes_map.items():
            if node_id_1 != node_id_2:
                coords_1 = node_1['coords']
                coords_2 = node_2['coords']
                
                # Check if connection intersects with any NFZ
                is_safe = True
                for nfz in nfzs:
                    if segment_crosses_polygon((coords_1, coords_2), nfz.coordinates):
                        is_safe = False
                        break
                
                if is_safe:
                    distance = calculate_distance(coords_1, coords_2)
                    adj_list[node_id_1].append((node_id_2, distance))
    
    return nodes_map, adj_list