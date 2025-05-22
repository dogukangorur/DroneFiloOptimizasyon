# plot_utils.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from a_star_solver import a_star_search
from utils import segment_crosses_polygon
from matplotlib.animation import FuncAnimation
import numpy as np

def plot_routes(drones, deliveries, assignments, nodes_map, nfzs, adj_list, animate=False):
    fig, ax = plt.subplots(figsize=(10, 10))

    # --- NO-FLY ZONES ---
    for nfz in nfzs:
        polygon = patches.Polygon(nfz.coordinates, closed=True, edgecolor='red', facecolor='salmon', alpha=0.4)
        ax.add_patch(polygon)
        centroid = tuple(map(lambda x: sum(x)/len(x), zip(*nfz.coordinates)))
        ax.text(*centroid, f"NFZ {nfz.zone_id}", fontsize=8, color='red')

    # --- DRONES ---
    for drone in drones:
        x, y = drone.start_pos
        ax.plot(x, y, 'bo', markersize=10)
        ax.text(x+5, y+5, f"D{drone.drone_id}", fontsize=8)

    # --- DELIVERIES ---
    for delivery in deliveries:
        x, y = delivery.location
        ax.plot(x, y, 'gs', markersize=6)
        ax.text(x+5, y+5, f"T{delivery.point_id}", fontsize=8)

    # --- ROUTES (with NFZ validation) ---
    valid_paths = []
    for delivery_id, drone_id in assignments.items():
        drone_node = f"D{drone_id}_START"
        delivery_node = str(delivery_id)

        path, _ = a_star_search(adj_list, nodes_map, nfzs, drone_node, delivery_node)
        if not path:
            continue

        coords = [nodes_map[node]["coords"] for node in path]
        is_valid = True
        for i in range(len(coords) - 1):
            for nfz in nfzs:
                if segment_crosses_polygon(coords[i], coords[i+1], nfz.coordinates):
                    is_valid = False
                    break
            if not is_valid:
                break

        if is_valid:
            xs, ys = zip(*coords)
            ax.plot(xs, ys, linestyle='--', linewidth=1.5, alpha=0.8, color='blue')
            valid_paths.append(coords)
        else:
            print(f"⚠️  Dron {drone_id} → Teslimat {delivery_id} rotası NFZ kesiyor, çizilmiyor.")

    ax.set_title("Drone Teslimat Rotaları")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.tight_layout()

    # --- ANIMATE (optional) ---
    if animate and valid_paths:
        print("🎬 Animasyon başlatılıyor...")

        dot, = ax.plot([], [], 'ro', markersize=8)

        flat_points = [point for path in valid_paths for point in path]
        xs, ys = zip(*flat_points)

        def init():
            dot.set_data([], [])
            return dot,

        def update(frame):
            dot.set_data(xs[frame], ys[frame])
            return dot,

        ani = FuncAnimation(fig, update, frames=len(xs), init_func=init, blit=True, interval=300, repeat=False)

    plt.show()
