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
        if pd.isna(id_value):
            return None
        return hashlib.sha256(str(id_value).encode()).hexdigest()[:8]  # 短く表示
    
    # ノード追加 (membersからユーザー)
    for _, row in members.iterrows():
        actor_id = hash_id(row['id'])
        G.add_node(actor_id, label=f"Actor {actor_id}", original_id=row['id'])
    
    # エッジ追加: posts/repliesからResponse連鎖 (emailで紐付け)
    replies = replies.merge(posts[['id', 'member_id', 'created']], left_on='request_id', right_on='id', suffixes=('_reply', '_post'))
    for _, row in replies.iterrows():
        # emailでmembersと紐付け
        email = row['email']
        member_match = members[members['email'] == email]
        
        if len(member_match) > 0:
            from_id = hash_id(member_match.iloc[0]['id'])  # emailから該当member_id取得
            to_id = hash_id(row['member_id_post'])  # post作成者
            latency = (pd.to_datetime(row['created_at']) - pd.to_datetime(row['created_post'])).total_seconds() / 60 if 'created_post' in row else 0
            G.add_edge(from_id, to_id, action='Response', latency=latency)
    
    # エッジ追加: share_linksからShare連鎖
    for _, row in share_links.iterrows():
        from_id = hash_id(row['owner_user_id'])
        to_id = hash_id(row['request_id'])  # 共有先request
        latency = 0  # shareは即時想定、必要なら追加
        G.add_edge(from_id, to_id, action='Share', latency=latency, ripple_depth=row.get('ripple_depth', 0))
    
    # エッジ追加: request_visitsから訪問/深度 (オプション連鎖)
    for _, row in request_visits.iterrows():
        visitor_id = hash_id(row['visitor_user_id'])
        if visitor_id is None:  # visitor_user_idがnullの場合スキップ
            continue
        to_id = hash_id(row['request_id'])
        latency = 0  # 訪問時間差追加可能
        G.add_edge(visitor_id, to_id, action='Visit', latency=latency, ripple_depth=row['ripple_depth'])
    
    # エッジ追加: thanks_logsからThanks (協力感謝連鎖) - emailで紐付け
    for _, row in thanks_logs.iterrows():
        # sender_idでmembers検索
        sender_match = members[members['id'] == row['sender_id']]
        giver_match = members[members['id'] == row['giver_member_id']]
        
        if len(sender_match) > 0 and len(giver_match) > 0:
            from_id = hash_id(sender_match.iloc[0]['id'])
            to_id = hash_id(giver_match.iloc[0]['id'])
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

# Breadth計算 (論文Section 6.3対応)
def calculate_breadth(G, origin=None):
    if not origin and G.nodes:
        origin = list(G.nodes)[0]
    try:
        levels = nx.single_source_shortest_path_length(G, origin)
        breadth_per_depth = {}
        for node, depth in levels.items():
            breadth_per_depth[depth] = breadth_per_depth.get(depth, 0) + 1
        return breadth_per_depth
    except:
        return {}

# Latency分布
def get_latency_distribution(G):
    latencies = [data['latency'] for _, _, data in G.edges(data=True) if 'latency' in data]
    return latencies

# 可視化 (ripple_depthもラベル追加)
def visualize_ripple(G):
    if len(G.nodes) == 0:
        print("No nodes to visualize")
        return
    
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['action']} ({d.get('latency', 0):.2f}min, depth:{d.get('ripple_depth', 0)})" 
                   for u, v, d in G.edges(data=True)}
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True, node_size=800, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title("Ripple Structure from YOROSIX CSV")
    plt.tight_layout()
    plt.show()

# 実行例 (コマンドラインでフォルダパス指定: sys.argv[1])
if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else 'sample_data/'  # デフォルトをsample_data/に変更
    print(f"Loading from folder: {data_dir}")
    G = load_yorosix_ripple(data_dir)
    
    print(f"\n=== Ripple Analysis Results ===")
    print(f"Total Nodes: {len(G.nodes)}")
    print(f"Total Edges: {len(G.edges)}")
    print(f"Max Ripple Depth: {calculate_depth(G)}")
    
    breadth = calculate_breadth(G)
    print(f"Breadth per Depth: {breadth}")
    
    latencies = get_latency_distribution(G)
    if latencies:
        print(f"Latency Distribution: Mean={np.mean(latencies):.2f}min, Std={np.std(latencies):.2f}min")
        print(f"  Min={min(latencies):.2f}min, Max={max(latencies):.2f}min")
    else:
        print(f"Latency Distribution: No data")
    
    visualize_ripple(G)
