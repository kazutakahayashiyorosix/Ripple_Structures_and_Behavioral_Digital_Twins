# 🧩 Ripple Simulation Engine（リップル構造シミュレーション）

This repository provides Python-based simulations for reproducing and examining **Ripple Structures**,  
a framework that models cooperation as information flow, derived from behavioral event data collected via  
[YOROSIX](https://www.yorosix.com/).

The simulations and models in this repository are based on the following paper:

> ### **Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins**
> **Kazutaka Hayashi**  
> 📄 **DOI:** https://doi.org/10.5281/zenodo.18298249
> 📄 **DOI:** https://doi.org/10.5281/zenodo.18298603

---

## 📦 Scope of this Repository

This repository publicly provides:
* **The theoretical framework** (linked paper)
* **Reproducible simulations** (Python source code)

In contrast, the following components remain under the stewardship of  
**Kazutaka Hayashi at YOROSIX**:
* The full research program and experimental design
* Comprehensive behavioral data collected from real-world deployments

> [!TIP]
> Researchers interested in independent validation, replication, or extension of this work  
> in different empirical or theoretical contexts are welcome to initiate a conversation,  
> provided that the research purpose is clearly defined.

---

## 🧩 Challenge: The Coordination Puzzle

If the theory feels abstract, let intuition lead before analysis.  
We have prepared an experiential entry point where the "Information Flow" becomes tangible.

### **Are you ready to solve the puzzle?**
### 👉 [**Visit yorosix.com**](https://www.yorosix.com/)

---
*Warning: Understanding the ripple is easier than mastering it.*

---

## 1. Overview  （概要）

Ripple Structures represent **directional causal chains of cooperative actions**, such as:

A → B → C → D → …

These chains are modeled as a **directed temporal graph**, where each edge represents a cooperative action with measurable latency.

This simulation constructs Ripple graphs from CSV-based behavioral logs using **NetworkX**, and additionally computes:

- Ripple Depth  
- Ripple Breadth  
- Ripple Latency  
- Re-propagation Nodes (Prediction 5)  
- Hierarchical Ripple Tree  
- 7-panel visualization dashboard  

Ripple 構造とは：

A が B を助け、B が C を助け、C が D を助ける…

という **協力行動の因果的な伝播構造** を、時間情報を含む **有向グラフ** として表現する枠組みです。

本シミュレーションは CSV ログから Ripple グラフを構築し、さらに：

- Ripple 深さ（Depth）  
- Ripple 幅（Breadth）  
- 協力遅延（Latency）  
- 再伝播ノード（Prediction 5）  
- 階層 Ripple Tree  
- 7枚の可視化パネル  

を生成します。

---

## 2. Requirements  （必要環境） 

- Python **3.8+**

### Install dependencies  （依存ライブラリのインストール）

```
pip install -r requirements.txt
```

or manually:

```
pip install networkx matplotlib numpy pandas seaborn
```

---

## 3. Quick Start  （クイックスタート）

### 3.1 Run with Sample Data  （サンプルデータで実行）

```
python ripple_simulation.py sample_data/
```

A visualization window with **7 analysis panels** will appear.

---

### 3.2 Run with Your Own Data  （自分のデータで実行）

Place the following **6 CSV files** in a folder:

| File | Description |
|------|-------------|
| members.csv | User information |
| posts.csv | Requests (origin nodes) |
| replies.csv | Responses |
| share_links.csv | Share events |
| request_visits.csv | Visit events |
| thanks_logs.csv | Thanks events |

**Important:**  
Replies are linked to members **via email**, not via `giver_member_id`.

実行：

```
python ripple_simulation.py /path/to/your/csv/folder/
```

---

## 4. Sample Data Description  （サンプルデータの内容）

The `sample_data/` folder includes:

- 5 actors  
- 3 requests  
- 4 responses  
- 4 shares  
- 5 visits  
- 4 thanks  

Example Ripple Chains:

1. A → B → C  
2. B → D  
3. C → E  

---

## 5. Code Explanation  （コード解説）

### Core Functions  （主な関数）

#### `load_yorosix_ripple(data_dir)`
- Loads all 6 CSV files  
- Anonymizes actors via SHA-256  
- Builds a directed Ripple graph  

#### `compute_depth(G, origin)`
Computes Ripple depth.

#### `compute_breadth(depths)`
Counts cooperators per depth.

#### `compute_latency(G)`
Extracts latency values.

#### `detect_repropagation_nodes(G)`
Detects actors with repeated Share events (Prediction 5).

#### `hierarchical_layout(G, origin)`
Generates a layered Ripple Tree layout.

#### `visualize_all(G)`
Displays **7 visual panels**:
1. Ripple Structure  
2. Depth Heatmap  
3. Hierarchical Ripple Tree  
4. Ripple Propagation  
5. Breadth  
6. Latency Distribution  
7. Re-propagation Nodes  

---

## 6. Customization  （カスタマイズ） 

### Add new event types

```python
G.add_edge(from_id, to_id, action='CustomAction', latency=...)
```

### Change latency units

```python
latency_seconds / 3600   # → hours
```

### Modify anonymization length

```python
hash_id(... )[:12]
```

---

## 7. Full Dataset Access  （データアクセス）

Full YOROSIX datasets are available to research collaborators.

Contact:  
kazutaka.hayashi@yorosix.com

---

## 8. Citation  （引用） 

```
@article{hayashi2026ripple,
  title={Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins},
  author={Hayashi, Kazutaka},
  year={2026},
  doi={10.5281/zenodo.18298249},
  url={https://doi.org/10.5281/zenodo.18298249}
}
```

---

## 9. Theoretical Background  （理論背景）

Ripple models cooperation as:

1. Directional behavioral events  
2. Information flow with measurable latency  
3. Emergent propagation without centralized control  
4. Re-propagation roles (Prediction 5)

Ripple は以下を前提に構築：

1. 行動ベースの因果構造  
2. 情報としての協力  
3. 非中央集権的な伝播  
4. 再伝播ノードの出現（予測5）

---

## 10. Troubleshooting  （トラブルシューティング）

| Issue | Solution |
|-------|----------|
| FileNotFoundError | Ensure all 6 CSV files exist |
| KeyError: email | Check email column in members.csv & replies.csv |
| Empty graph | Verify IDs and non-empty CSVs |
| No visualization | Use `plt.savefig()` |

---

## License（ライセンス）

MIT License  
© 2026 Kazutaka Hayashi

See the [LICENSE](./LICENSE.mb) file for details.

---

## 12. Acknowledgments  （謝辞）

Thanks to the YOROSIX community for enabling non-interventional observational research.  
YOROSIX コミュニティに感謝します。

