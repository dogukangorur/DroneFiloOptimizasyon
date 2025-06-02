# --- KPI PLOTTER ------------------------------------------------------------
def plot_kpis(drones, distance_km, route_extension):
    """
    drones          : List[Drone]   – batarya_history alanı dolmuş olacak
    distance_km     : Dict[delivery_id] = km
    route_extension : Dict[delivery_id] = oran
    """
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axs = plt.subplots(1, 3, figsize=(18, 4))
    fig.suptitle("Drone KPI Görselleştirmeleri", fontsize=14)

    # Batarya eğrisi
    for dr in drones:
        axs[0].plot(dr.time_ticks, dr.battery_history, label=f"D{dr.drone_id}")
    axs[0].set_ylabel("%")
    axs[0].set_xlabel("Simülasyon adımı")
    axs[0].set_title("Batarya Deşarj Eğrisi")
    axs[0].legend()

    # Teslimat başı km
    ids   = list(distance_km.keys())
    kms   = [distance_km[i] for i in ids]
    axs[1].bar(ids, kms)
    axs[1].set_xticks(ids)
    axs[1].set_xlabel("Teslimat ID")
    axs[1].set_title("Teslimat Başı Kat Edilen km")

    # Rota uzama oranı
    ratios = [route_extension[i] for i in ids]
    axs[2].bar(ids, ratios, color="orange")
    axs[2].axhline(1.0, ls="--", lw=1, label="Kuş uçuşu = 1.0")
    axs[2].set_xticks(ids)
    axs[2].set_xlabel("Teslimat ID")
    axs[2].set_title("Rota Uzama Oranı")
    axs[2].legend()

    plt.tight_layout()
    plt.show()