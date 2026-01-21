import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib
import sys

# SHA-256 で Actor ID を匿名化
def hash_id(id_value):
    if pd.isna(id_value):
        return None
    return hashlib.sha256(str(id_value).encode()).hexdigest()[:8]

# Ripple Graph 構築
def load_yorosix_ripple(data_dir='sample_data/'):
    G = nx.DiGraph()

    # CSV 読み込み
    try:
        members = pd.read_csv(f'{data_dir}members.csv')
        posts = pd.read_csv(f'{data_dir}posts.csv')
        replies = pd.read_csv(f'{data_dir}replies.csv')
        share_links = pd.read_csv(f'{data_dir}share_links.csv')
        request_visits = pd.read_csv(f'{data_dir}request_visits.csv')
        thanks_logs = pd.read_csv(f'{data_dir}thanks_logs.csv')
    except FileNotFoundError as e:
        print(f"Error: Missing CSV → {e}")
        return G

    # 型を揃える（merge が失敗しないための最重要ポイント）
    posts['id'] = posts['id'].astype(str)
    replies['request_id'] = replies['request_id'].astype(str)

    # ノード追加（Actor）
    for _, row in members.iterrows():
        actor_id = hash_id(row['id'])
        G.add_node(actor_id, label=f"Actor {actor_id}", original_id=row['id'])

    # === Response 連鎖（返信者 → 投稿者）===
    # replies.request_id → posts.id で merge
    replies_merged = replies.merge(
        posts[['id', 'member_id', 'created']],
        left_on='request_id',
        right_on='id',
        suffixes=('_reply', '_post')
    )

    if 'member_id_post' not in replies_merged.columns:
        print("ERROR: merge failed → request_id と posts.id が一致していません")
        print(replies_merged.head())
        return G

    for _, row in replies_merged.iterrows():
        # 返信者（email → members）
        email = row['email']
        member_match = members[members['email'] == email]

        if len(member_match) == 0:
            continue

        from_id = hash_id(member_match.iloc[0]['id'])  # 返信者
        to_id = hash_id(row['member_id_post'])          # 投稿者

        latency = (
            pd.to_datetime(row['created_at']) -
            pd.to_datetime(row['created_post'])
        ).total_seconds() / 60

        G.add_edge(from_id, to_id, action='Response', latency=latency)

    # === Share 連鎖（共有者 → 投稿者）===
    for _, row in share_links.iterrows():
        # request_id → posts.member_id に変換
        req = posts[posts['id'] == str(row['request_id'])]
        if len(req) == 0:
            continue

        to_member = req.iloc[0]['member_id']
        from_id = hash_id(row['owner_user_id'])
        to_id = hash_id(to_member)

        G.add_edge(from_id, to_id, action='Share', latency=0)

    # === Visit 連鎖（訪問者 → 投稿者）===
    for _, row in request_visits.iterrows():
        req = posts[posts['id'] == str(row['request_id'])]
        if len(req) == 0:
            continue

        to_member = req.iloc[0]['member_id']
        from_id = hash_id(row['visitor_user_id'])
        to_id = hash_id(to_member)

        G.add_edge(from_id, to_id, action='Visit', latency=0)

    # === Thanks 連鎖（感謝送信者 → 受信者）===
    for _, row in thanks_logs.iterrows():
        sender = members[members['id'] == row['sender_id']]
        receiver = members[members['id'] == row['giver_member_id']]

        if len(sender) == 0 or len(receiver) == 0:
            continue

        from_id = hash_id(sender.iloc[0]['id'])
        to_id = hash_id(receiver.iloc[0]['id'])

        G.add_edge(from_id, to_id, action='Thanks', latency=0)

    return G

# Ripple Depth（最長距離）
def calculate_depth(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]
    try:
        depths = nx.single_source_shortest_path_length(G, origin)
        return max(depths.values())
    except:
        return 0

# Breadth（深度ごとのノード数）
def calculate_breadth(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]
    try:
        levels = nx.single_source_shortest_path_length(G, origin)
        breadth = {}
        for node, depth in levels.items():
            breadth[depth] = breadth.get(depth, 0) + 1
        return breadth
    except:
        return {}

# Latency 分布
def get_latency_distribution(G):
    return [d['latency'] for _, _, d in G.edges(data=True) if 'latency' in d]

# 可視化
def visualize_ripple(G):
    if len(G.nodes) == 0:
        print("No nodes to visualize")
        return

    pos = nx.spring_layout(G)
    edge_labels = {
        (u, v): f"{d['action']} ({d.get('latency', 0):.1f}m)"
        for u, v, d in G.edges(data=True)
    }

    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            arrows=True, node_size=800, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title("Ripple Structure")
    plt.tight_layout()
    plt.show()

# 実行
if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else 'sample_data/'
    print(f"Loading from folder: {data_dir}")

    G = load_yorosix_ripple(data_dir)

    print("\n=== Ripple Analysis Results ===")
    print(f"Total Nodes: {len(G.nodes)}")
    print(f"Total Edges: {len(G.edges)}")
    print(f"Max Ripple Depth: {calculate_depth(G)}")

    breadth = calculate_breadth(G)
    print(f"Breadth per Depth: {breadth}")

    latencies = get_latency_distribution(G)
    if latencies:
        print(f"Latency Mean={np.mean(latencies):.2f}m, Std={np.std(latencies):.2f}m")
    else:
        print("Latency: No data")

    visualize_ripple(G)
