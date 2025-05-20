
# graph_utils.py

from entities import DeliveryPoint, Drone

NODE_TYPE_DRONE_START = 'drone_start'
NODE_TYPE_DELIVERY = 'delivery_point'

def build_graph(drones, deliveries):
    """
    Dronlar ve teslimatlar arasındaki grafı oluşturur.
    """
    nodes_map = {}
    adj_list = {}

    # Drone düğümleri ekle
    for drone in drones:
        drone_node_id = f"D{drone.drone_id}_START"
        nodes_map[drone_node_id] = {'coords': drone.start_pos, 'type': NODE_TYPE_DRONE_START, 'original_id': drone.drone_id}

    # Teslimat düğümleri ekle
    for delivery in deliveries:
        delivery_node_id = str(delivery.point_id)
        nodes_map[delivery_node_id] = {'coords': delivery.location, 'type': NODE_TYPE_DELIVERY, 'original_id': delivery.point_id}

    # Komşuluk listesi oluşturun (boş; A* sırasında doldurulur)
    adj_list = {key: [] for key in nodes_map.keys()}

    return nodes_map, adj_list

