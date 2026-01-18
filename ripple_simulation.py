import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # CSV読み込み用追加

# CSVからRippleグラフをロードする関数 (ランダム生成をCSV対応に修正)
def load_real_ripple(data_file='real_data.csv'):
    # Directed graph作成 (協力の方向性)
    G = nx.DiGraph()
    
    # データ読み込み
    df = pd.read_csv(data_file)
    
    # ユニークなアクターをノード追加 (アクターID)
    actors = set(df['actor_from'].unique()) | set(df['actor_to'].unique())
    for actor in actors:
        G.add_node(actor, label=f"Actor {actor}")
    
    # エッジ追加 (協力行動: Response or Share)
    for _, row in df.iterrows():
        # latencyをtimestamp差から計算 (分単位)
        latency = (pd.to_datetime(row['timestamp_to']) - pd.to_datetime(row['timestamp_from'])).total_seconds() / 60
        G.add_edge(row['actor_from'], row['actor_to'], action=row['event_type'], latency=latency)
    
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
    edge_labels = {(u, v): f"{d['action']} ({d['latency']:.2f})" for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Ripple Structure from CSV Data")
    plt.show()

# 実行例 (CSVからロード)
G = load_real_ripple('real_data.csv')  # 実際のCSVファイル名に置き換え
print(f"Max Ripple Depth: {calculate_depth(G)}")
latencies = get_latency_distribution(G)
print(f"Latency Distribution: {latencies} (Mean: {np.mean(latencies) if latencies else 0:.2f})")
visualize_ripple(G)
