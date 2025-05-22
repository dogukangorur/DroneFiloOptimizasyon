# graph_utils.py

from entities import DeliveryPoint, Drone, NoFlyZone

NODE_TYPE_DRONE_START = 'drone_start'
NODE_TYPE_DELIVERY = 'delivery_point'
NODE_TYPE_NFZ_CORNER = 'nfz_corner'  # 🔁 yeni tip

def build_graph(drones, deliveries, nfzs=[]):
    """
    Dronlar, teslimatlar ve NFZ köşeleri ile graf yapısını oluşturur.
    """
    nodes_map = {}
    adj_list = {}

    # 🛫 Drone düğümleri ekle
    for drone in drones:
        node_id = f"D{drone.drone_id}_START"
        nodes_map[node_id] = {
            'coords': drone.start_pos,
            'type': NODE_TYPE_DRONE_START,
            'original_id': drone.drone_id
        }

    # 🎯 Teslimat düğümleri ekle
    for delivery in deliveries:
        node_id = str(delivery.point_id)
        nodes_map[node_id] = {
            'coords': delivery.location,
            'type': NODE_TYPE_DELIVERY,
            'original_id': delivery.point_id
        }

    # 🚫 No-Fly Zone köşe düğümleri ekle
    for nfz in nfzs:
        for i, corner in enumerate(nfz.coordinates):
            node_id = f"NFZ{nfz.zone_id}_P{i}"
            nodes_map[node_id] = {
                'coords': corner,
                'type': NODE_TYPE_NFZ_CORNER,
                'original_id': nfz.zone_id
            }

    # 🔄 Komşuluk listesi oluştur
    adj_list = {node_id: [] for node_id in nodes_map.keys()}

    return nodes_map, adj_list
