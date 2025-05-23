
# plot_utils.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from a_star_solver import a_star_search
from utils import segment_crosses_polygon
from matplotlib.animation import FuncAnimation
import numpy as np
import time

def plot_routes(drones, deliveries, assignments, nodes_map, nfzs, adj_list, animate=False):
    fig, ax = plt.subplots(figsize=(10, 10))

    # --- NO-FLY ZONES --- 
    for nfz in nfzs:
        polygon = patches.Polygon(nfz.coordinates, closed=True, edgecolor='red', facecolor='salmon', alpha=0.4)
        ax.add_patch(polygon)
        centroid = tuple(map(lambda x: sum(x)/len(x), zip(*nfz.coordinates)))
        ax.text(*centroid, f"NFZ {nfz.zone_id}", fontsize=8, color='red')

    # --DRONES --
    for drone in drones:
        x, y = drone.start_pos
        ax.plot(x, y, 'bo', markersize=10)
        ax.text(x+5, y+5, f"D{drone.drone_id}", fontsize=8)

    # --DELIVERIES --
    for delivery in deliveries:
        x, y = delivery.location
        ax.plot(x, y, 'gs', markersize=6)
        ax.text(x+5, y+5, f"T{delivery.point_id}", fontsize=8)

    # --- GENERATE NFZ EDGE POINTS ---
    # Extract the edge points directly from the NFZ polygons with minimal safety margin
    edge_points = extract_nfz_edge_points(nfzs, safety_margin=2)
    
    # Optionally plot the edge points (for debugging)
    # for point in edge_points:
    #     ax.plot(point[0], point[1], 'mx', markersize=3)

    # --- ROUTES (with NFZ avoidance along edges) --- 
    valid_paths = []
    drone_ids = []
    
    for delivery_id, drone_id in assignments.items():
        drone_node = f"D{drone_id}_START"
        delivery_node = str(delivery_id)
        
        # Get start and end positions
        start_pos = nodes_map[drone_node]["coords"]
        end_pos = nodes_map[delivery_node]["coords"]
        
        # Check if direct path crosses any NFZ
        direct_path_safe = True
        for nfz in nfzs:
            if segment_crosses_polygon((start_pos, end_pos), nfz.coordinates):
                direct_path_safe = False
                break
                
        if direct_path_safe:
            # Direct path doesn't cross any NFZ, use it
            path = [start_pos, end_pos]
            xs, ys = zip(*path)
            ax.plot(xs, ys, linestyle='--', linewidth=1.5, alpha=0.8, color='blue')
            valid_paths.append(path)
            drone_ids.append(drone_id)
        else:
            # Need to find path that navigates along NFZ edges
            path = find_path_along_nfz_edges(start_pos, end_pos, nfzs, edge_points)
            
            if path:
                xs, ys = zip(*path)
                ax.plot(xs, ys, linestyle='--', linewidth=1.5, alpha=0.8, color='green')
                
                # Plot waypoints used in the path
                for i in range(1, len(path)-1):
                    wp = path[i]
                    ax.plot(wp[0], wp[1], 'go', markersize=4)
                    
                valid_paths.append(path)
                drone_ids.append(drone_id)
            else:
                print(f"⚠️  Dron {drone_id} → Teslimat {delivery_id} için geçerli bir rota bulunamadı!")

    ax.set_title("Drone Teslimat Rotaları")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.tight_layout()

    # --ANIMATE (optional) --
    if animate and valid_paths:
        print("🎬 Animasyon başlatılıyor...")
        
        # Create a separate dot for each drone
        dots = []
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        
        for i, drone_id in enumerate(drone_ids):
            color_idx = i % len(colors)
            dot, = ax.plot([], [], 'o', markersize=8, color=colors[color_idx], label=f'Drone {drone_id}')
            dots.append(dot)
        
        # Add legend
        ax.legend(loc='upper left')
        
        def init():
            for dot in dots:
                dot.set_data([], [])
            return dots
        
        # Find the longest path to determine animation frames
        max_frames = max(len(path) for path in valid_paths)
        
        def update(frame):
            for i, (path, dot) in enumerate(zip(valid_paths, dots)):
                # For each path, if frame is within path length, update the dot position
                if frame < len(path):
                    point = path[frame]
                    dot.set_data([point[0]], [point[1]])  # Use lists to ensure it's a sequence
                elif frame >= len(path):
                    # Keep the dot at the last position in its path
                    last_point = path[-1]
                    dot.set_data([last_point[0]], [last_point[1]])  # Use lists to ensure it's a sequence
            return dots
        
        # Create the animation
        try:
            ani = FuncAnimation(
                fig, 
                update, 
                frames=max_frames,
                init_func=init, 
                blit=True, 
                interval=500,  # Slower animation (500ms between frames)
                repeat=False
            )
            
            plt.show()
        except Exception as e:
            print(f"Animasyon hatası: {str(e)}")
            # If animation fails, at least show the static plot
            plt.show()
    else:
        plt.show()

def extract_nfz_edge_points(nfzs, safety_margin=2, points_per_edge=10):
    """
    Extract points directly from the edges of NFZ polygons with minimal safety margin.
    
    Args:
        nfzs: List of no-fly zone objects
        safety_margin: Minimal distance from the NFZ boundary in meters
        points_per_edge: Number of points to extract per edge
        
    Returns:
        List of (x, y) coordinates along NFZ edges
    """
    edge_points = []
    
    for nfz in nfzs:
        coords = nfz.coordinates
        
        # Get the vertices (corners) of the NFZ
        for i in range(len(coords)):
            p1 = coords[i]
            p2 = coords[(i + 1) % len(coords)]
            
            # Calculate vector along the edge
            edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
            edge_length = np.sqrt(edge_vector[0]**2 + edge_vector[1]**2)
            
            # Skip if edge is too short
            if edge_length < 1:
                continue
                
            # Normalize the edge vector
            unit_edge = (edge_vector[0] / edge_length, edge_vector[1] / edge_length)
            
            # Calculate perpendicular vector (outward from NFZ)
            perp_vector = (-unit_edge[1], unit_edge[0])
            
            # Check if perpendicular vector points outward
            test_point = (p1[0] + perp_vector[0], p1[1] + perp_vector[1])
            if is_point_in_polygon(test_point, coords):
                # If inside, flip the vector
                perp_vector = (-perp_vector[0], -perp_vector[1])
            
            # Generate points along the edge
            for j in range(points_per_edge + 1):
                # Position along the edge (0 to 1)
                t = j / points_per_edge
                
                # Interpolate between p1 and p2 to get point on the edge
                point_on_edge = (p1[0] + t * edge_vector[0], p1[1] + t * edge_vector[1])
                
                # Add minimal safety margin
                safe_point = (
                    point_on_edge[0] + safety_margin * perp_vector[0],
                    point_on_edge[1] + safety_margin * perp_vector[1]
                )
                
                edge_points.append(safe_point)
            
            # Always include the NFZ vertices themselves (with safety margin)
            safe_vertex = (
                p1[0] + safety_margin * perp_vector[0],
                p1[1] + safety_margin * perp_vector[1]
            )
            edge_points.append(safe_vertex)
    
    return edge_points

def is_point_in_polygon(point, polygon):
    """
    Check if a point is inside a polygon using the ray casting algorithm.
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y:
                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xinters:
                inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def segment_dist(p1, p2):
    """Calculate the Euclidean distance between two points"""
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def find_path_along_nfz_edges(start, end, nfzs, edge_points, max_nodes=15):
    """
    Find a path from start to end that navigates along NFZ edges.
    Uses a modified A* algorithm to find the shortest path.
    
    Args:
        start: (x, y) start coordinate
        end: (x, y) end coordinate
        nfzs: List of no-fly zone objects
        edge_points: List of (x, y) coordinates along NFZ edges
        max_nodes: Maximum number of nodes in the path to prevent overly complex routes
        
    Returns:
        List of (x, y) coordinates forming a path, or None if no path found
    """
    # Include start and end in potential path nodes
    all_points = [start] + edge_points + [end]
    
    # Create a graph of valid connections
    connections = {}
    for i, p1 in enumerate(all_points):
        connections[i] = []
        
        # Try to connect directly to end point to optimize
        if i != len(all_points) - 1:  # Not the end point itself
            # Check if can connect directly to end
            end_point = all_points[-1]
            if not any(segment_crosses_polygon((p1, end_point), nfz.coordinates) for nfz in nfzs):
                dist = segment_dist(p1, end_point)
                connections[i].append((len(all_points) - 1, dist))
        
        # Connect to other points if not crossing NFZs
        for j, p2 in enumerate(all_points):
            if i != j and j != len(all_points) - 1:  # Skip self and end (handled above)
                # Only connect if the segment doesn't cross any NFZ
                if not any(segment_crosses_polygon((p1, p2), nfz.coordinates) for nfz in nfzs):
                    dist = segment_dist(p1, p2)
                    connections[i].append((j, dist))
    
    # A* algorithm
    # Create open and closed sets
    open_set = {0}  # Start with the start node
    closed_set = set()
    
    # g_score: cost from start to current node
    g_score = {i: float('inf') for i in range(len(all_points))}
    g_score[0] = 0
    
    # f_score: g_score + heuristic (estimated cost to end)
    f_score = {i: float('inf') for i in range(len(all_points))}
    f_score[0] = segment_dist(start, end)  # Heuristic for start node
    
    # came_from: to reconstruct the path
    came_from = {}
    
    # Number of nodes in the path so far
    path_length = {0: 1}
    
    while open_set:
        # Find node with lowest f_score
        current = min(open_set, key=lambda x: f_score[x])
        
        # If we reached the end, reconstruct and return the path
        if current == len(all_points) - 1:
            path = []
            while current in came_from:
                path.append(all_points[current])
                current = came_from[current]
            path.append(start)  # Add the start point
            return path[::-1]  # Reverse to get start to end
        
        open_set.remove(current)
        closed_set.add(current)
        
        for neighbor, dist in connections[current]:
            if neighbor in closed_set:
                continue
                
            # Skip if this would make the path too long
            if path_length.get(current, 0) + 1 > max_nodes:
                continue
                
            # Calculate tentative g_score
            tentative_g = g_score[current] + dist
            
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g >= g_score[neighbor]:
                continue
                
            # This path is better, record it
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g
            path_length[neighbor] = path_length.get(current, 0) + 1
            f_score[neighbor] = g_score[neighbor] + segment_dist(all_points[neighbor], end)
    
    # No path found
    return None

