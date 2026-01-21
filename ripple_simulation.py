import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib
import sys
import seaborn as sns

# =========================
# 基本：グラフ構築
# =========================

def hash_id(id_value):
    if pd.isna(id_value):
        return None
    return hashlib.sha256(str(id_value).encode()).hexdigest()[:8]

def load_yorosix_ripple(data_dir='sample_data/'):
    G = nx.DiGraph()

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

    # 型揃え（重要）
    posts['id'] = posts['id'].astype(str)
    replies['request_id'] = replies['request_id'].astype(str)

    # ノード：Actor
    for _, row in members.iterrows():
        actor_id = hash_id(row['id'])
        G.add_node(actor_id, label=f"Actor {actor_id}", original_id=row['id'])

    # === Response 連鎖（返信者 → 投稿者）===
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
        email = row['email']
        member_match = members[members['email'] == email]
        if len(member_match) == 0:
            continue

        from_id = hash_id(member_match.iloc[0]['id'])      # 返信者
        to_id = hash_id(row['member_id_post'])             # 投稿者

        latency = (
            pd.to_datetime(row['created_at']) -
            pd.to_datetime(row['created_post'])
        ).total_seconds() / 60

        G.add_edge(from_id, to_id, action='Response', latency=latency)

    # === Share 連鎖（共有者 → 投稿者）===
    for _, row in share_links.iterrows():
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

# =========================
# 基本メトリクス
# =========================

def calculate_depth(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]
    try:
        depths = nx.single_source_shortest_path_length(G, origin)
        return max(depths.values())
    except:
        return 0

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

def get_latency_distribution(G):
    return [d['latency'] for _, _, d in G.edges(data=True) if 'latency' in d]

# =========================
# 1. Ripple Depth ヒートマップ
# =========================

def visualize_depth_heatmap(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]

    try:
        depths = nx.single_source_shortest_path_length(G, origin)
    except:
        print("Depth calculation failed")
        return

    depth_values = list(depths.values())
    if not depth_values:
        print("No depth data")
        return

    max_depth = max(depth_values)
    depth_count = {}
    for d in depth_values:
        depth_count[d] = depth_count.get(d, 0) + 1

    heatmap_data = [[depth_count.get(i, 0) for i in range(max_depth + 1)]]

    plt.figure(figsize=(max(6, max_depth + 1), 2))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap="YlOrRd",
        cbar=True,
        xticklabels=[f"D{i}" for i in range(max_depth + 1)],
        yticklabels=["Ripple Depth"],
        fmt="d"
    )
    plt.title("Ripple Depth Heatmap")
    plt.tight_layout()
    plt.show()

# =========================
# 2. Ripple Tree 自動生成
# =========================

def visualize_ripple_tree(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]

    try:
        tree = nx.bfs_tree(G, origin)
    except:
        print("Cannot build Ripple Tree")
        return

    pos = nx.nx_agraph.graphviz_layout(tree, prog="dot") if hasattr(nx, "nx_agraph") else nx.spring_layout(tree)

    depths = nx.single_source_shortest_path_length(tree, origin)
    max_depth = max(depths.values()) if depths else 0
    colors = []
    for n in tree.nodes():
        d = depths.get(n, 0)
        colors.append(plt.cm.plasma(d / max_depth if max_depth > 0 else 0))

    plt.figure(figsize=(8, 6))
    nx.draw(tree, pos, with_labels=True, node_color=colors,
            node_size=800, arrows=True, font_size=8)
    plt.title("Ripple Tree (BFS from Origin)")
    plt.tight_layout()
    plt.show()

# =========================
# 3. Ripple Propagation シミュレーション
# =========================

def simulate_ripple_propagation(G, origin=None, steps=10):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]

    # latency を時間として扱い、簡易的に離散ステップに落とす
    edges = []
    for u, v, d in G.edges(data=True):
        t = d.get('latency', 0)
        edges.append((u, v, max(0, t)))

    if not edges:
        print("No edges for propagation simulation")
        return

    # 時間順にソート
    edges.sort(key=lambda x: x[2])

    # ステップ分割
    times = [e[2] for e in edges]
    t_min, t_max = min(times), max(times)
    if t_max == t_min:
        t_bins = [t_min, t_max + 1]
    else:
        t_bins = np.linspace(t_min, t_max, steps + 1)

    activated = set([origin])
    snapshots = []

    for i in range(steps):
        t_start, t_end = t_bins[i], t_bins[i + 1]
        new_activated = set()
        for u, v, t in edges:
            if t_start <= t < t_end and u in activated:
                new_activated.add(v)
        activated |= new_activated
        snapshots.append((t_end, set(activated)))

    # 可視化（最後のスナップショットだけネットワーク表示）
    last_time, last_nodes = snapshots[-1]
    pos = nx.spring_layout(G)
    colors = []
    for n in G.nodes():
        colors.append('red' if n in last_nodes else 'lightgray')

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=800, arrows=True, font_size=8)
    plt.title(f"Ripple Propagation (activated by t={last_time:.1f} min)")
    plt.tight_layout()
    plt.show()

# =========================
# 4. Ambassador Flywheel 可視化
# =========================

def visualize_ambassador_flywheel(G, top_k=5):
    # シンプルに「アウトディグリーが大きいノード＝Ripple を生み出す Actor」として扱う
    out_deg = dict(G.out_degree())
    if not out_deg:
        print("No degree data for Ambassador Flywheel")
        return

    sorted_nodes = sorted(out_deg.items(), key=lambda x: x[1], reverse=True)
    ambassadors = [n for n, d in sorted_nodes[:top_k]]

    pos = nx.spring_layout(G)
    colors = []
    sizes = []
    for n in G.nodes():
        if n in ambassadors:
            colors.append('gold')
            sizes.append(1200)
        else:
            colors.append('lightblue')
            sizes.append(600)

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=sizes, arrows=True, font_size=8)

    # 凡例用ダミー
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='gold', label='Ambassador (high out-degree)'),
        Patch(facecolor='lightblue', label='Other Actors')
    ]
    plt.legend(handles=legend_elements, loc='best')
    plt.title("Ambassador Flywheel (structural view)")
    plt.tight_layout()
    plt.show()

# =========================
# 元のネットワーク可視化（任意）
# =========================

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

# =========================
# メイン実行
# =========================

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

    # 可視化群
    print("\n=== Base Ripple Graph ===")
    visualize_ripple(G)

    print("\n=== Ripple Depth Heatmap ===")
    visualize_depth_heatmap(G)

    print("\n=== Ripple Tree ===")
    visualize_ripple_tree(G)

    print("\n=== Ripple Propagation Simulation ===")
    simulate_ripple_propagation(G)

    print("\n=== Ambassador Flywheel Visualization ===")
    visualize_ambassador_flywheel(G)
