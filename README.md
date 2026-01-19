
Ripple Structure Simulation

This repository provides a Python simulation for modeling Ripple structures from YOROSIX behavioral event data, as introduced in the paper:

📄 Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins
Kazutaka Hayashi
DOI: https://doi.org/10.5281/zenodo.18298249

---

1. Overview

Ripple structures represent directional causal chains of cooperative actions
(e.g., A helps B → B helps C → …)
modeled as a directed temporal graph.

This simulation uses NetworkX to construct Ripple graphs from CSV-based behavioral logs.

Key Concepts

• Nodes: Anonymized actors
• Edges: Cooperative actions (Response, Share, Visit, Thanks)• Latency: Time delay between actions (minutes)
• Ripple Depth: Propagation distance from the origin request



---

2. Requirements

• Python 3.8+


Install dependencies

pip install -r requirements.txt


Or install manually:

pip install networkx matplotlib numpy pandas


---

3. Quick Start

3.1 Run with Sample Data

python ripple_simulation.py sample_data/


Expected output:

=== Ripple Analysis Results ===
Total Nodes: 5
Total Edges: 10
Max Ripple Depth: 2
Breadth per Depth: {0: 1, 1: 3, 2: 1}
Latency Distribution: Mean=105.00min, Std=45.23min


A visualization window will appear.

---

3.2 Run with Your Own Data

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

4. Sample Data Description

The sample_data/ folder includes:

• 5 actors
• 3 requests
• 4 responses
• 4 share events
• 5 visit events
• 4 thanks events


Example Ripple Chains

1. Alice → Bob (depth 1) → Charlie (depth 2)
2. Bob → David
3. Charlie → Eve


---

5. Code Explanation

Core Functions

`load_yorosix_ripple(data_dir)`

• Loads 6 CSV files
• Anonymizes actors via SHA-256
• Builds directed Ripple graph
• Links replies via email matching


`calculate_depth(G, origin)`

Computes maximum Ripple depth.

`calculate_breadth(G, origin)`

Counts cooperators at each depth.

`get_latency_distribution(G)`

Extracts Δt for all edges.

`visualize_ripple(G)`

Draws Ripple graph with action types, latency, and depth.

---

6. Customization

Add new event types

G.add_edge(from_id, to_id, action='CustomAction', latency=...)


Change latency units

... / 3600  # minutes → hours


Modify anonymization

hash_id(... )[:12]


---

7. Full Dataset Access

Full YOROSIX datasets are available to research collaborators.

Contact:
kazutaka.hayashi@yorosix.com

---

8. Citation

@article{hayashi2026ripple,
  title={Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins},
  author={Hayashi, Kazutaka},
  year={2026},
  doi={10.5281/zenodo.18298249},
  url={https://doi.org/10.5281/zenodo.18298249}
}


---

9. Theoretical Background

Ripple models cooperation as:

1. Directional behavioral events
2. Information flow with measurable latency
3. Emergent propagation without centralized control


Predictions tested:

• Cooperation emerges without incentives
• Propagation follows non-optimal paths
• Re-propagation roles emerge organically


---

10. Troubleshooting

Issue	Solution	
FileNotFoundError	Ensure all 6 CSV files exist	
KeyError: email	Check email column in members.csv & replies.csv	
Empty graph	Verify IDs and non-empty CSVs	
No visualization	Use plt.savefig('ripple_graph.png')	


---

11. License

MIT License © 2026 Kazutaka Hayashi

---

12. Acknowledgments

Thanks to the YOROSIX community for enabling non-interventional observational research.

---

🔵 日本語版 README

---

Ripple Structure Simulation（リップル構造シミュレーション）

このリポジトリは、論文：

📄 「Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins」
DOI: https://doi.org/10.5281/zenodo.18298249

で提案された Ripple（協力の伝播構造） を Python で再現するシミュレーションコードです。

---

1. 概要

Ripple 構造とは：

A が B を助け、B が C を助け…
という協力行動の因果的な伝播を、時間情報を含む有向グラフとして表現する枠組みです。

このシミュレーションでは、YOROSIX の行動ログ（CSV）から Ripple グラフを構築します。

キー概念

• ノード: 匿名化されたアクター
• エッジ: 協力行動（Response / Share / Visit / Thanks）• Latency: 行動間の時間差（分）
• Ripple Depth: 起点からの伝播距離



---

2. 必要環境

• Python 3.8+


依存ライブラリのインストール

pip install -r requirements.txt


または：

pip install networkx matplotlib numpy pandas


---

3. クイックスタート

3.1 サンプルデータで実行

python ripple_simulation.py sample_data/


---

3.2 自分のデータで実行

以下の 6つの CSV をフォルダに配置：

ファイル名	内容	
members.csv	ユーザー情報	
posts.csv	リクエスト	
replies.csv	レスポンス	
share_links.csv	シェア	
request_visits.csv	訪問ログ	
thanks_logs.csv	サンクス	


重要:
replies.csv は giver_member_id を使わず、email で紐付けます。

実行：

python ripple_simulation.py /path/to/your/csv/folder/


---

4. サンプルデータの内容

• 5人のアクター
• 3つのリクエスト
• 4つのレスポンス
• 4つのシェア
• 5つの訪問
• 4つのサンクス


---

5. コード解説

主な関数

• load_yorosix_ripple()
• calculate_depth()
• calculate_breadth()
• get_latency_distribution()
• visualize_ripple()


---

6. カスタマイズ

新しいイベントタイプの追加

G.add_edge(from_id, to_id, action='CustomAction', latency=...)


---

7. データアクセス

共同研究者向けに提供可能です。
kazutaka.hayashi@yorosix.com

---

8. 引用

@article{hayashi2026ripple,
  ...
}


---

9. 理論背景

Ripple は以下を前提に構築：

• 行動ベースの因果構造
• 情報としての協力
• 非中央集権的な伝播


---

10. トラブルシューティング

問題	解決策	
FileNotFoundError	CSV が揃っているか確認	
KeyError: email	email 列を確認	
グラフが空	ID の整合性を確認	
可視化されない	plt.savefig() を使用	


---

11. ライセンス

MIT License © 2026 Kazutaka Hayashi

---

12. 謝辞

YOROSIX コミュニティに感謝します。

