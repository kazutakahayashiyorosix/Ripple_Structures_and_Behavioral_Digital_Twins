import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import hashlib
import sys
from collections import defaultdict
import numpy as np

# =========================
# ユーティリティ
# =========================

def hash_id(x):
    if pd.isna(x):
        return None
    return hashlib.sha256(str(x).encode()).hexdigest()[:8]

def safe_add_edge(G, u, v, **attrs):
    if u is None or v is None:
        return
    G.add_edge(u, v, **attrs)

# =========================
# グラフ構築
# =========================

def load_yorosix_ripple(data_dir="sample_data/"):
    G = nx.DiGraph()

    members = pd.read_csv(f"{data_dir}members.csv")
    posts = pd.read_csv(f"{data_dir}posts.csv")
    replies = pd.read_csv(f"{data_dir}replies.csv")
    share_links = pd.read_csv(f"{data_dir}share_links.csv")
    request_visits = pd.read_csv(f"{data_dir}request_visits.csv")
    thanks_logs = pd.read_csv(f"{data_dir}thanks_logs.csv")

    posts["id"] = posts["id"].astype(str)
    replies["request_id"] = replies["request_id"].astype(str)

    # ノード
    for _, r in members.iterrows():
        hid = hash_id(r["id"])
        if hid:
            G.add_node(hid)

    # Response（返信 → 投稿者）
    replies_merged = replies.merge(
        posts[["id", "member_id", "created"]],
        left_on="request_id",
        right_on="id",
        how="left"
    )

    for _, r in replies_merged.iterrows():
        sender = members[members["email"] == r["email"]]
        if sender.empty:
            continue

        from_id = hash_id(sender.iloc[0]["id"])
        to_id = hash_id(r["member_id"])

        latency = (
            pd.to_datetime(r["created_at"]) -
            pd.to_datetime(r["created"])
        ).total_seconds() / 60

        safe_add_edge(G, from_id, to_id, action="Response", latency=latency)

    # Share
    for _, r in share_links.iterrows():
        p = posts[posts["id"] == str(r["request_id"])]
        if p.empty:
            continue
        safe_add_edge(
            G,
            hash_id(r["owner_user_id"]),
            hash_id(p.iloc[0]["member_id"]),
            action="Share",
            latency=0
        )

    # Visit
    for _, r in request_visits.iterrows():
        p = posts[posts["id"] == str(r["request_id"])]
        if p.empty:
            continue
        safe_add_edge(
            G,
            hash_id(r["visitor_user_id"]),
            hash_id(p.iloc[0]["member_id"]),
            action="Visit",
            latency=0
        )

    # Thanks
    for _, r in thanks_logs.iterrows():
        s = members[members["id"] == r["sender_id"]]
        t = members[members["id"] == r["giver_member_id"]]
        if s.empty or t.empty:
            continue
        safe_add_edge(
            G,
            hash_id(s.iloc[0]["id"]),
            hash_id(t.iloc[0]["id"]),
            action="Thanks",
            latency=0
        )

    return G

# =========================
# 分析機能（論文準拠）
# =========================

def compute_depth(G, origin):
    return nx.single_source_shortest_path_length(G, origin)

def compute_breadth(depths):
    max_d = max(depths.values())
    counts = [0] * (max_d + 1)
    for d in depths.values():
        counts[d] += 1
    return counts

def compute_latency(G):
    latencies = []
    for _, _, data in G.edges(data=True):
        if "latency" in data and data["latency"] > 0:
            latencies.append(data["latency"])
    return latencies

def detect_repropagation_nodes(G, threshold=3):
    share_counts = defaultdict(int)
    for u, v, data in G.edges(data=True):
        if data.get("action") == "Share":
            share_counts[u] += 1
    return [n for n, c in share_counts.items() if c >= threshold]

def hierarchical_layout(G, origin):
    depths = compute_depth(G, origin)

    layers = defaultdict(list)
    for node, d in depths.items():
        layers[d].append(node)

    pos = {}

    # 到達可能ノード
    for d, nodes in layers.items():
        for i, n in enumerate(nodes):
            pos[n] = (i, -d)

    # 到達不能ノード（origin から辿れない）
    unreachable = set(G.nodes()) - set(depths.keys())
    if unreachable:
        y = -(max(layers.keys()) + 1) if layers else 0
        for i, n in enumerate(sorted(unreachable)):
            pos[n] = (i, y)

    return pos


# =========================
# 可視化（7枚）
# =========================

def visualize_all(G):
    origin = list(G.nodes)[0]
    depths = compute_depth(G, origin)
    breadth = compute_breadth(depths)
    latencies = compute_latency(G)
    reprop_nodes = detect_repropagation_nodes(G)

    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    axes = axes.flatten()

    # 1. Ripple Structure
    pos = nx.spring_layout(G, seed=0)
    nx.draw(G, pos, ax=axes[0], with_labels=True, node_size=400, font_size=7)
    axes[0].set_title("Ripple Structure")

    # 2. Depth Heatmap
    sns.heatmap([breadth], annot=True, fmt="d", cmap="YlOrRd", ax=axes[1], cbar=False)
    axes[1].set_title("Ripple Depth Heatmap")

    # 3. Ripple Tree（階層）
    pos_h = hierarchical_layout(G, origin)
    nx.draw(G, pos_h, ax=axes[2], with_labels=True, node_size=400, font_size=7)
    axes[2].set_title("Ripple Tree (Hierarchical)")

    # 4. Ripple Propagation
    nx.draw(G, pos, ax=axes[3], with_labels=True, node_size=400)
    axes[3].set_title("Ripple Propagation")

    # 5. Breadth
    axes[4].bar(range(len(breadth)), breadth)
    axes[4].set_title("Ripple Breadth")

    # 6. Latency Distribution
    axes[5].hist(latencies, bins=20, color="skyblue")
    axes[5].set_title("Latency Distribution (min)")

    # 7. Re-propagation Nodes
    colors = ["gold" if n in reprop_nodes else "lightblue" for n in G.nodes()]
    nx.draw(G, pos, ax=axes[6], node_color=colors, with_labels=True, node_size=400)
    axes[6].set_title("Re-propagation Nodes")

    # 残りは空白
    axes[7].axis("off")
    axes[8].axis("off")

    plt.tight_layout()
    plt.show()

# =========================
# メイン
# =========================

if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "sample_data/"
    print("Loading:", data_dir)

    G = load_yorosix_ripple(data_dir)

    print("Nodes:", len(G.nodes))
    print("Edges:", len(G.edges))

    visualize_all(G)
