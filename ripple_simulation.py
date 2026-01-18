import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

# Ripple構造のシミュレーション関数
def simulate_ripple(num_nodes=10, edge_prob=0.3, max_latency=10):
    # Directed graph作成 (協力の方向性)
    G = nx.DiGraph()
    
    # ノード追加 (アクターID)
    for i in range(num_nodes):
        G.add_node(i, label=f"Actor {i}")
    
    # エッジ追加 (協力行動: Response or Share)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_prob:
                action_type = random.choice(["Response", "Share"])
                latency = np.random.randint(1, max_latency + 1)  # ランダム遅延 (1~10単位時間)
                G.add_edge(i, j, action=action_type, latency=latency)
    
    return G

# 深度計算 (origin=0から最長パス)
def calculate_depth(G, origin=0):
    try:
        depths = nx.single_source_shortest_path_length(G, origin)
        max_depth = max(depths.values())
        return max_depth
    except nx.NetworkXNoPath:
        return 0

# Latency分布計算
def get_latency_distribution(G):
    latencies = [data['latency'] for u, v, data in G.edges(data=True)]
    return latencies

# 可視化
def visualize_ripple(G):
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['action']} ({d['latency']})" for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Ripple Structure Simulation")
    plt.show()

# 実行例
G = simulate_ripple(num_nodes=8, edge_prob=0.2, max_latency=5)
print(f"Max Ripple Depth: {calculate_depth(G)}")
latencies = get_latency_distribution(G)
print(f"Latency Distribution: {latencies} (Mean: {np.mean(latencies) if latencies else 0:.2f})")
visualize_ripple(G)