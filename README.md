# Ripple Structure Simulation

This repository provides a Python-based simulation for modeling **Ripple Structures** from YOROSIX behavioral event data, as introduced in the paper:

📄 **Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins**  
Kazutaka Hayashi  
DOI: https://doi.org/10.5281/zenodo.18298249

---

## 1. Overview

Ripple Structures represent **directional causal chains of cooperative actions**, such as:

```
A helps B → B helps C → C helps D → …
```

These chains are modeled as a **directed temporal graph**, where each edge represents a cooperative action with measurable latency.

This simulation constructs Ripple graphs from CSV-based behavioral logs using **NetworkX** and visualizes 5 key perspectives in a single dashboard.

### Key Concepts

- **Nodes**: Anonymized actors  
- **Edges**: Cooperative actions  
  - Response (replies to requests)
  - Share (propagation events)
  - Visit (engagement tracking)
  - Thanks (contribution acknowledgment)
- **Latency**: Time delay between actions (minutes)  
- **Ripple Depth**: Propagation distance from the origin request  

---

## 2. Requirements

- Python **3.8+**

### Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install networkx matplotlib numpy pandas seaborn
```

---

## 3. Quick Start

### 3.1 Run with Sample Data

```bash
python ripple_simulation.py sample_data/
```

Expected output:

```
Loading: sample_data/
Nodes: 5
Edges: 10
```

A visualization window will appear showing **5 analysis perspectives**:
1. Ripple Structure (full graph)
2. Depth Heatmap (propagation depth distribution)
3. Ripple Tree (BFS traversal from origin)
4. Ripple Propagation (temporal flow)
5. Ambassador Flywheel (top-5 influencers highlighted)

---

### 3.2 Run with Your Own Data

Place the following **6 CSV files** in a folder:

| File | Description |
|------|-------------|
| members.csv | User information (requires: id, email) |
| posts.csv | Requests/origin nodes (requires: id, member_id, created) |
| replies.csv | Responses to requests (requires: request_id, email, created_at) |
| share_links.csv | Share propagation events (requires: request_id, owner_user_id) |
| request_visits.csv | Visit events (requires: request_id, visitor_user_id) |
| thanks_logs.csv | Thank events (requires: sender_id, giver_member_id) |

**Important Changes:**  
- Replies are now linked to request creators **via email matching** (not via direct member_id)
- This reflects the actual YOROSIX data structure where replies come from external users

Run:

```bash
python ripple_simulation.py /path/to/your/csv/folder/
```

---

## 4. Sample Data Description

The `sample_data/` folder includes:

- 5 actors  
- 3 requests  
- 4 responses  
- 4 share events  
- 5 visit events  
- 4 thanks events  

### Example Ripple Chains

1. Alice → Bob (depth 1) → Charlie (depth 2)  
2. Bob → David  
3. Charlie → Eve  

---

## 5. Code Explanation

### Core Functions

#### `load_yorosix_ripple(data_dir)`
- Loads all 6 CSV files  
- Anonymizes actors via SHA-256 (8-character hash)
- Builds a directed Ripple graph with 4 edge types
- **Key Fix**: Links replies to post creators via email matching (avoiding `member_id_post` errors)

#### `visualize_all_in_one(G, top_k=5)`
Generates a 5-panel visualization dashboard:
1. **Ripple Structure**: Full network graph
2. **Depth Heatmap**: Distribution of actors across propagation depths
3. **Ripple Tree**: BFS traversal showing hierarchical propagation
4. **Ripple Propagation**: Static view of cooperation flow
5. **Ambassador Flywheel**: Highlights top-k most active propagators (gold nodes)

---

## 6. Visualization Dashboard

The simulation now outputs **5 analyses in one view**:

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Ripple Structure│  Depth Heatmap  │   Ripple Tree   │
├─────────────────┼─────────────────┼─────────────────┤
│Ripple Propagation│ Ambassador      │     (empty)     │
│                 │   Flywheel      │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

**Ambassador Flywheel** identifies key propagators:
- Gold nodes = Top 5 by out-degree (most shares/responses)
- Larger node size = Higher influence
- Useful for identifying natural "ambassadors" in the network

---

## 7. Key Implementation Details

### Anonymization
```python
def hash_id(x):
    return hashlib.sha256(str(x).encode()).hexdigest()[:8]
```
- Ensures privacy while maintaining consistent IDs
- 8-character hash balances readability and anonymity

### Safe Edge Addition
```python
def safe_add_edge(G, u, v, **attrs):
    if u is None or v is None:
        return
    G.add_edge(u, v, **attrs)
```
- Prevents errors from missing/invalid IDs
- Gracefully handles incomplete data

### Reply Linking
```python
replies_merged = replies.merge(
    posts[["id", "member_id", "created"]],
    left_on="request_id",
    right_on="id",
    how="left"
)
```
- Merges replies with post creators
- Uses email to identify responders (from members table)
- Calculates latency from post creation to reply timestamp

---

## 8. Customization

### Add new event types

```python
G.add_edge(from_id, to_id, action='CustomAction', latency=...)
```

### Change latency units

```python
... / 3600   # minutes → hours
```

### Modify anonymization length

```python
hash_id(...)[:12]  # 8 → 12 characters
```

### Adjust Ambassador detection

```python
visualize_all_in_one(G, top_k=10)  # Show top 10 instead of 5
```

---

## 9. Full Dataset Access

Full YOROSIX datasets are available to research collaborators.

**Contact:**  
kazutaka.hayashi@yorosix.com

---

## 10. Citation

```bibtex
@article{hayashi2026ripple,
  title={Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins},
  author={Hayashi, Kazutaka},
  year={2026},
  doi={10.5281/zenodo.18298249},
  url={https://doi.org/10.5281/zenodo.18298249}
}
```

---

## 11. Theoretical Background

Ripple models cooperation as:

1. **Directional behavioral events** (not psychological states)
2. **Information flow** with measurable latency
3. **Emergent propagation** without centralized control

### Predictions tested:

• Cooperation emerges without incentives  
• Propagation follows non-optimal paths  
• Re-propagation roles emerge organically  
• Ambassador nodes amplify cooperation signals

---

## 12. Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` | Ensure all 6 CSV files exist in the specified folder |
| `KeyError: 'email'` | Check that members.csv and replies.csv both have 'email' column |
| `Empty graph` | Verify that member IDs in replies.csv match emails in members.csv |
| `No visualization` | Check matplotlib backend; try `plt.savefig('ripple_graph.png')` |
| `TypeError: unhashable type` | Ensure all ID columns are strings; use `.astype(str)` if needed |

---

## 13. What's New in This Version

### v2.0 Changes:
- ✅ **Fixed**: Removed `member_id_post` dependency (caused pandas KeyError)
- ✅ **Added**: 5-panel dashboard visualization
- ✅ **Added**: Ambassador Flywheel analysis
- ✅ **Added**: Depth heatmap and BFS tree views
- ✅ **Improved**: Reply linking now uses email matching (more robust)
- ✅ **Improved**: Safe edge addition prevents None-value errors

---

## 14. License

MIT License © 2026 Kazutaka Hayashi

---

## 15. Acknowledgments

Thanks to the YOROSIX community for enabling non-interventional observational research.

---

---

# Ripple Structure Simulation（リップル構造シミュレーション）

このリポジトリは、以下の論文で提案された **Ripple（協力の伝播構造）** を Python で再現するシミュレーションコードです。

📄 「Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins」  
DOI: https://doi.org/10.5281/zenodo.18298249

---

## 1. 概要

Ripple 構造とは：

```
A が B を助け、B が C を助け、C が D を助け…
```

という **協力行動の因果的な伝播** を、時間情報を含む **有向グラフ** として表現する枠組みです。

このシミュレーションでは、YOROSIX の行動ログ（CSV）から Ripple グラフを構築し、**5つの分析視点を1画面で可視化**します。

### キー概念

• **ノード**: 匿名化されたアクター  
• **エッジ**: 協力行動
  - Response（返信）
  - Share（共有）
  - Visit（訪問）
  - Thanks（感謝）
• **Latency**: 行動間の時間差（分）  
• **Ripple Depth**: 起点からの伝播距離

---

## 2. 必要環境

• Python 3.8+

### 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

または：

```bash
pip install networkx matplotlib numpy pandas seaborn
```

---

## 3. クイックスタート

### 3.1 サンプルデータで実行

```bash
python ripple_simulation.py sample_data/
```

期待される出力：

```
Loading: sample_data/
Nodes: 5
Edges: 10
```

**5つの分析画面**が表示されます：
1. Ripple Structure（全体グラフ）
2. Depth Heatmap（深さの分布）
3. Ripple Tree（幅優先探索ツリー）
4. Ripple Propagation（伝播フロー）
5. Ambassador Flywheel（トップ5の影響力者を強調）

---

### 3.2 自分のデータで実行

以下の **6つの CSV** をフォルダに配置：

| ファイル名 | 内容 |
|-----------|------|
| members.csv | ユーザー情報（必須: id, email） |
| posts.csv | リクエスト（必須: id, member_id, created） |
| replies.csv | レスポンス（必須: request_id, email, created_at） |
| share_links.csv | シェア（必須: request_id, owner_user_id） |
| request_visits.csv | 訪問ログ（必須: request_id, visitor_user_id） |
| thanks_logs.csv | サンクス（必須: sender_id, giver_member_id） |

**重要な変更点:**  
返信（replies）は **email でマッチング**します（`member_id_post` は不要になりました）

実行：

```bash
python ripple_simulation.py /path/to/your/csv/folder/
```

---

## 4. サンプルデータの内容

• 5人のアクター  
• 3つのリクエスト  
• 4つのレスポンス  
• 4つのシェア  
• 5つの訪問  
• 4つのサンクス

---

## 5. コード解説

### 主な関数：

#### `load_yorosix_ripple(data_dir)`
- 6つのCSVを読み込み
- SHA-256で匿名化（8文字）
- 4種類のエッジでグラフ構築
- **修正済**: emailでマッチングすることで `member_id_post` エラーを回避

#### `visualize_all_in_one(G, top_k=5)`
5つのパネルで可視化：
1. Ripple Structure（全体）
2. Depth Heatmap（深さ分布）
3. Ripple Tree（BFS木）
4. Ripple Propagation（伝播）
5. Ambassador Flywheel（上位5名をゴールドで強調）

---

## 6. 可視化ダッシュボード

**5つの分析を1画面で表示：**

```
┌─────────────────┬─────────────────┬─────────────────┐
│ Ripple Structure│  Depth Heatmap  │   Ripple Tree   │
├─────────────────┼─────────────────┼─────────────────┤
│Ripple Propagation│ Ambassador      │     (空欄)      │
│                 │   Flywheel      │                 │
└─────────────────┴─────────────────┴─────────────────┘
```

**Ambassador Flywheel** は主要な伝播者を特定：
- ゴールドノード = 発信数トップ5
- ノードサイズ = 影響力の大きさ
- 自然発生的な「アンバサダー」を可視化

---

## 7. バージョン2.0の変更点

### 新機能：
- ✅ **修正**: `member_id_post` 依存を削除（pandasエラーを解消）
- ✅ **追加**: 5パネルダッシュボード可視化
- ✅ **追加**: アンバサダーフライホイール分析
- ✅ **追加**: 深さヒートマップとBFSツリー表示
- ✅ **改善**: 返信のリンクをemailマッチングに変更（より堅牢）
- ✅ **改善**: None値エラーを防ぐセーフエッジ追加

---

## 8. カスタマイズ

### 新しいイベントタイプの追加

```python
G.add_edge(from_id, to_id, action='CustomAction', latency=...)
```

### アンバサダー検出数の変更

```python
visualize_all_in_one(G, top_k=10)  # トップ10を表示
```

---

## 9. データアクセス

共同研究者向けに提供可能です。  
**連絡先:** kazutaka.hayashi@yorosix.com

---

## 10. 引用

```bibtex
@article{hayashi2026ripple,
  title={Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins},
  author={Hayashi, Kazutaka},
  year={2026},
  doi={10.5281/zenodo.18298249},
  url={https://doi.org/10.5281/zenodo.18298249}
}
```

---

## 11. 理論背景

Ripple は以下を前提に構築：

• **行動ベースの因果構造**（心理状態ではない）  
• **情報としての協力**（測定可能な遅延を含む）  
• **非中央集権的な伝播**（自然発生）  
• **アンバサダーノード**が協力シグナルを増幅

---

## 12. トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `FileNotFoundError` | 6つのCSVファイルが揃っているか確認 |
| `KeyError: 'email'` | members.csvとreplies.csvの両方にemailカラムがあるか確認 |
| グラフが空 | replies.csvのmember IDがmembers.csvのemailと一致するか確認 |
| 可視化されない | matplotlibバックエンドを確認；`plt.savefig()`を試す |

---

## 13. ライセンス

MIT License © 2026 Kazutaka Hayashi

---

## 14. 謝辞

YOROSIX コミュニティに感謝します。
