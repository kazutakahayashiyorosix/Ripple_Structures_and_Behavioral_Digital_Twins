Ripple Structure Simulation

This repository provides a Python-based simulation for modeling Ripple structures from YOROSIX behavioral event data, as introduced in the paper:

📄 Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins
Kazutaka Hayashi
DOI: https://doi.org/10.5281/zenodo.18298249

---

Overview

Ripple structures represent directional causal chains of cooperative actions
(e.g., A helps B → B helps C → …)
modeled as a directed temporal graph.

This simulation uses NetworkX to construct Ripple graphs from CSV-based behavioral logs.

Key Concepts

• Nodes: Anonymized actors
• Edges: Cooperative actions (Response, Share, Visit, Thanks)• Latency: Time delay between actions (minutes)
• Ripple Depth: Propagation distance from the origin request



---

Requirements

• Python 3.8+


Install dependencies

pip install -r requirements.txt


Or install manually:

pip install networkx matplotlib numpy pandas


---

Quick Start

1. Run with Sample Data (included)

python ripple_simulation.py sample_data/


Expected output:

Loading from folder: sample_data/

=== Ripple Analysis Results ===
Total Nodes: 5
Total Edges: 10
Max Ripple Depth: 2
Breadth per Depth: {0: 1, 1: 3, 2: 1}
Latency Distribution: Mean=105.00min, Std=45.23min
  Min=30.00min, Max=180.00min


A visualization window will display the Ripple graph.

---

2. Run with Your Own Data

Place the following 6 CSV files in a folder:

File	Description	
members.csv	User information	
posts.csv	Requests (origin nodes)	
replies.csv	Responses to requests	
share_links.csv	Share propagation events	
request_visits.csv	Visit events with ripple depth	
thanks_logs.csv	Thank events (optional)	


Important:
Replies are linked to members via email, not giver_member_id.

Run:

python ripple_simulation.py /path/to/your/csv/folder/


---

Sample Data Description

The sample_data/ folder includes:

• 5 actors (Alice, Bob, Charlie, David, Eve)
• 3 Requests
• 4 Responses
• 4 Share events
• 5 Visit events
• 4 Thanks events


Example Ripple Chains

1. Request 101: Alice → Bob (depth 1) → Charlie (depth 2)
2. Request 102: Bob → David (depth 1)
3. Request 103: Charlie → Eve (depth 1)


---

Code Explanation

Core Functions

`load_yorosix_ripple(data_dir)`

• Loads 6 CSV files
• Anonymizes actors via SHA-256
• Builds directed Ripple graph
• Links replies via email matching


`calculate_depth(G, origin)`

• Computes maximum Ripple depth


`calculate_breadth(G, origin)`

• Counts cooperators at each depth


`get_latency_distribution(G)`

• Extracts Δt for all edges


`visualize_ripple(G)`

• Draws Ripple graph with action types, latency, and depth


---

Customization

Add new event types

for _, row in custom_events.iterrows():
    from_id = hash_id(row['actor_id'])
    to_id = hash_id(row['target_id'])
    G.add_edge(from_id, to_id, action='CustomAction', latency=...)


Change latency units

latency = (pd.to_datetime(row['event_time']) -
           pd.to_datetime(row['origin_time'])).total_seconds() / 3600


Modify anonymization

def hash_id(id_value):
    return hashlib.sha256(str(id_value).encode()).hexdigest()[:12]


---

Full Dataset Access

Full YOROSIX observational datasets are proprietary and available to research collaborators.

Contact:
Kazutaka Hayashi
kazutaka.hayashi@yorosix.com

Co-authorship opportunities are available for empirical validation work.

---

Citation

@article{hayashi2026ripple,
  title={Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins},
  author={Hayashi, Kazutaka},
  year={2026},
  doi={10.5281/zenodo.18298249},
  url={https://doi.org/10.5281/zenodo.18298249}
}


---

Theoretical Background

This simulation implements the Ripple framework, which models cooperation as:

1. Directional behavioral events
2. Information flow with measurable latency
3. Emergent propagation without centralized control


Key predictions:

• Cooperation emerges without incentives
• Propagation follows non-optimal paths
• Re-propagation roles emerge organically


See the paper for full theory and validation.

---

Troubleshooting

Issue	Solution	
FileNotFoundError: members.csv	Ensure all 6 CSV files exist	
KeyError: ‘email’	Check email column in members.csv & replies.csv	
Empty graph	Verify IDs and non-empty CSVs	
No visualization	Save instead: plt.savefig('ripple_graph.png')	


---

License

MIT License © 2026 Kazutaka Hayashi

---

Acknowledgments

This work is part of ongoing research on decentralized cooperation systems and Behavioral Digital Twins.
Special thanks to the YOROSIX community.

---



Ripple Structure Simulation（リップル構造シミュレーション）

このリポジトリは、論文
「Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins」
（DOI: https://doi.org/10.5281/zenodo.18298249） (doi.org in Bing)
で提案された Ripple（協力の伝播構造） を Python で再現するシミュレーションコードです。

---

概要

Ripple 構造とは、
A が B を助け、B が C を助け…
というような 協力行動の因果的な伝播 を、時間情報を含む有向グラフとして表現する枠組みです。

このシミュレーションでは、YOROSIX の行動ログ（CSV）から Ripple グラフを構築します。

キー概念

• ノード: 匿名化されたアクター
• エッジ: 協力行動（Response / Share / Visit / Thanks）• Latency: 行動間の時間差（分）
• Ripple Depth: 起点からの伝播距離



---

必要環境

• Python 3.8+


依存ライブラリのインストール

pip install -r requirements.txt


または手動で：

pip install networkx matplotlib numpy pandas


---

クイックスタート

1. サンプルデータで実行

python ripple_simulation.py sample_data/


出力例：

=== Ripple Analysis Results ===
Total Nodes: 5
Total Edges: 10
Max Ripple Depth: 2
Breadth per Depth: {0: 1, 1: 3, 2: 1}
Latency Distribution: Mean=105.00min ...


Ripple グラフが可視化されます。

---

2. 自分のデータで実行

以下の 6つの CSV をフォルダに配置：

ファイル名	内容	
members.csv	ユーザー情報	
posts.csv	リクエスト（起点）	
replies.csv	レスポンス	
share_links.csv	シェアによる伝播	
request_visits.csv	訪問ログ（深さ付き）	
thanks_logs.csv	サンクス（任意）	


重要:
replies.csv は giver_member_id を使わず、email で紐付けます。

実行：

python ripple_simulation.py /path/to/your/csv/folder/


---

サンプルデータの内容

• 5人のアクター
• 3つのリクエスト
• 4つのレスポンス
• 4つのシェア
• 5つの訪問
• 4つのサンクス


Ripple 例

1. Alice → Bob（深さ1）→ Charlie（深さ2）
2. Bob → David
3. Charlie → Eve


---

コード解説

主な関数

`load_yorosix_ripple(data_dir)`

• 6 CSV を読み込み
• SHA-256 で匿名化
• Ripple グラフを構築
• email でレスポンスを紐付け


`calculate_depth(G, origin)`

Ripple の最大深さを計算

`calculate_breadth(G, origin)`

深さごとの協力者数を算出

`get_latency_distribution(G)`

全エッジの時間差を抽出

`visualize_ripple(G)`

Ripple グラフを可視化

---

カスタマイズ

新しいイベントタイプの追加

G.add_edge(from_id, to_id, action='CustomAction', latency=...)


レイテンシ単位の変更

... / 3600  # 分→時間


匿名化の変更

hash_id(... )[:12]


---

データアクセス

YOROSIX の完全データセットは共同研究者に提供可能です。

連絡先：
kazutaka.hayashi@yorosix.com

---

引用

@article{hayashi2026ripple,
  ...
}


---

理論背景

Ripple は以下を前提に構築されています：

1. 行動ベースの因果構造
2. 情報としての協力
3. 非中央集権的な伝播


予測される現象：

• インセンティブなしで協力が生まれる
• 最適ではない経路で伝播する
• 再伝播ノードが自然に形成される


---

トラブルシューティング

問題	解決策	
FileNotFoundError	6 CSV が揃っているか確認	
KeyError: email	members と replies の email を確認	
グラフが空	ID の整合性を確認	
可視化されない	plt.savefig() を使用	


---

ライセンス

MIT License © 2026 Kazutaka Hayashi

---

謝辞

非介入型観察の基盤を提供した YOROSIX コミュニティに感謝します。
