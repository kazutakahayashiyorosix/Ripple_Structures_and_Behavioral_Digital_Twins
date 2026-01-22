import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import hashlib
import sys

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
# 5枚まとめて可視化
# =========================

def visualize_all_in_one(G, top_k=5):
    if not G.nodes:
        print("No graph data")
        return

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    pos = nx.spring_layout(G, seed=0)
    origin = list(G.nodes)[0]

    # 1. Ripple Structure
    nx.draw(G, pos, ax=axes[0], with_labels=True, node_size=400, font_size=7)
    axes[0].set_title("Ripple Structure")

    # 2. Depth Heatmap
    depths = nx.single_source_shortest_path_length(G, origin)
    max_depth = max(depths.values())
    counts = [0] * (max_depth + 1)
    for d in depths.values():
        counts[d] += 1

    sns.heatmap(
        [counts],
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        ax=axes[1],
        cbar=False
    )
    axes[1].set_yticks([0.5])
    axes[1].set_yticklabels(["Depth"])
    axes[1].set_title("Ripple Depth Heatmap")

    # 3. Ripple Tree
    tree = nx.bfs_tree(G, origin)
    pos_tree = nx.spring_layout(tree, seed=0)
    nx.draw(tree, pos_tree, ax=axes[2], with_labels=True, node_size=400, font_size=7)
    axes[2].set_title("Ripple Tree (BFS)")

    # 4. Ripple Propagation（静的）
    nx.draw(G, pos, ax=axes[3], with_labels=True, node_size=400)
    axes[3].set_title("Ripple Propagation")

    # 5. Ambassador Flywheel
    out_deg = dict(G.out_degree())
    ambassadors = sorted(out_deg, key=out_deg.get, reverse=True)[:top_k]
    colors = ["gold" if n in ambassadors else "lightblue" for n in G.nodes()]
    sizes = [800 if n in ambassadors else 400 for n in G.nodes()]

    nx.draw(
        G,
        pos,
        ax=axes[4],
        with_labels=True,
        node_color=colors,
        node_size=sizes,
        font_size=7
    )
    axes[4].set_title("Ambassador Flywheel")

    # 6枠目は空ける
    axes[5].axis("off")

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

    visualize_all_in_one(G)
