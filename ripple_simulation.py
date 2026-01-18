import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib  # 匿名化用
import sys  # コマンドライン引数用追加

# 複数のCSVからRippleグラフを構築
def load_yorosix_ripple(data_dir='data/'):
    G = nx.DiGraph()
    
    # CSVロード (ツールからエクスポートしたファイル想定)
    try:
        members = pd.read_csv(f'{data_dir}members.csv')  # ユーザー情報
        posts = pd.read_csv(f'{data_dir}posts.csv')      # 投稿 (Request)
        replies = pd.read_csv(f'{data_dir}replies.csv')  # Response
        share_links = pd.read_csv(f'{data_dir}share_links.csv')  # Share
        request_visits = pd.read_csv(f'{data_dir}request_visits.csv')  # 訪問/深度
        thanks_logs = pd.read_csv(f'{data_dir}thanks_logs.csv')  # Thanks (オプション協力)
    except FileNotFoundError as e:
        print(f"Error: CSV file missing - {e}")
        return G
    
    # アクターID匿名化 (SHA-256)
    def hash_id(id_value):
        return hashlib.sha256(str(id_value).encode()).hexdigest()[:8]  # 短く表示
    
    # ノード追加 (membersからユーザー)
    for _, row in members.iterrows():
        actor_id = hash_id(row['id'])
        G.add_node(actor_id, label=f"Actor {actor_id}", original_id=row['id'])
    
    # エッジ追加: posts/repliesからResponse連鎖
    replies = replies.merge(posts[['id', 'member_id', 'created']], left_on='request_id', right_on='id', suffixes=('_reply', '_post'))
    for _, row in replies.iterrows():
        from_id = hash_id(row['giver_member_id'] if 'giver_member_id' in row else row['request_id'])  # sender or owner
        to_id = hash_id(row['request_id'])  # 親post
        latency = (pd.to_datetime(row['created_at']) - pd.to_datetime(row['created_post'])).total_seconds() / 60 if 'created_post' in row else 0
        G.add_edge(from_id, to_id, action='Response', latency=latency)
    
    # エッジ追加: share_linksからShare連鎖
    for _, row in share_links.iterrows():
        from_id = hash_id(row['owner_user_id'])
        to_id = hash_id(row['request_id'])  # 共有先
        latency = 0  # shareは即時想定、必要なら追加
        G.add_edge(from_id, to_id, action='Share', latency=latency, ripple_depth=row.get('ripple_depth', 0))
    
    # エッジ追加: request_visitsから訪問/深度 (オプション連鎖)
    for _, row in request_visits.iterrows():
        from_id = hash_id(row['visitor_user_id'])
        to_id = hash_id(row['request_id'])
        latency = 0  # 訪問時間差追加可能
        G.add_edge(from_id, to_id, action='Visit', latency=latency, ripple_depth=row['ripple_depth'])
    
    # エッジ追加: thanks_logsからThanks (協力感謝連鎖)
    for _, row in thanks_logs.iterrows():
        from_id = hash_id(row['sender_id'])
        to_id = hash_id(row['giver_member_id'])
        latency = 0
        G.add_edge(from_id, to_id, action='Thanks', latency=latency)
    
    return G

# 深度計算 (origin指定、論文のmax path)
def calculate_depth(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]  # デフォルト原点
    try:
        depths = nx.single_source_shortest_path_length(G, origin)
        return max(depths.values())
    except:
        return 0

# Latency分布
def get_latency_distribution(G):
    latencies = [data['latency'] for _, _, data in G.edges(data=True)]
    return latencies

# 可視化 (ripple_depthもラベル追加)
def visualize_ripple(G):
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['action']} ({d['latency']:.2f}, depth:{d.get('ripple_depth', 0)})" for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Ripple Structure from YOROSIX CSV")
    plt.show()

# 実行例 (コマンドラインでフォルダパス指定: sys.argv[1])
if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else 'data/'  # ユーザ指定 or デフォルト
    print(f"Loading from folder: {data_dir}")
    G = load_yorosix_ripple(data_dir)
    print(f"Max Ripple Depth: {calculate_depth(G)}")
    latencies = get_latency_distribution(G)
    print(f"Latency Distribution: {latencies} (Mean: {np.mean(latencies) if latencies else 0:.2f})")
    visualize_ripple(G)

