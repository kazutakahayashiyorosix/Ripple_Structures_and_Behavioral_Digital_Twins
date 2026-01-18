# Ripple Structure Simulation

This repository provides a simple Python simulation for modeling "Ripple" structures as described in the paper "Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins" by Kazutaka Hayashi.

## Overview
Ripple structures represent directional causal chains of cooperative actions (e.g., A helps B → B helps C) as a directed temporal graph. This code uses NetworkX to model such graphs, where:
- Nodes: Actors (individuals or agents).
- Edges: Cooperative actions (Response or Share) with attributes like latency (time delay).

The simulation generates random graphs to demonstrate propagation depth and latency distribution, serving as a proof-of-concept for empirical validation.

## Requirements
- Python 3.x
- Libraries: `networkx`, `matplotlib`, `numpy`, `random` (install via `pip install networkx matplotlib numpy`)

## Usage
1. Clone the repository:
git clone https://github.com/kazutaka-hayashi/ripple-simulation.git

2. Run the script:
python ripple_simulation.py

- This will generate a random Ripple graph, compute max depth and latency distribution, and display a visualization.

Example output:
- Max Ripple Depth: 3 (example value)
- Latency Distribution: [2, 4, 1, ...] (Mean: 2.5)

## Code Explanation
- `simulate_ripple()`: Generates a directed graph with random edges representing cooperative actions.
- `calculate_depth()`: Computes the maximum propagation depth from a specified origin node.
- `get_latency_distribution()`: Extracts latency values from edges.
- `visualize_ripple()`: Draws the graph using Matplotlib.

## Extension
To incorporate real data:
- Modify `simulate_ripple()` to add edges based on actual events (e.g., from social network logs).
- Example: `G.add_edge(0, 1, action="Response", latency=3)` for a real cooperative event from Actor 0 to 1.

For more details, see the paper on arXiv or contact: kazutaka.hayashi@yorosix.com.

## License
MIT License






# リップル構造シミュレーション

このリポジトリは、林和孝の論文「Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins」で提案された「Ripple」構造のシンプルなPythonシミュレーションを提供します。

## 概要
Ripple構造は、協力行動の方向性因果連鎖（例: AがBを助ける → BがCを助ける）をdirected temporal graphとしてモデル化します。このコードはNetworkXを使ってそのグラフをモデルし、ノードをアクター、エッジを協力行動（Response or Share）とし、latency（時間遅延）を属性として追加します。

シミュレーションはランダムグラフを生成し、伝播深度とlatency分布を計算・可視化します。論文の理論的予測の概念実証として使えます。

## 必要環境
- Python 3.x
- ライブラリ: `networkx`, `matplotlib`, `numpy`, `random` (`pip install networkx matplotlib numpy` でインストール)

## 使い方
1. リポジトリをクローン:
git clone https://github.com/kazutaka-hayashi/ripple-simulation.git

2. スクリプトを実行:
python ripple_simulation.py

- ランダムなRippleグラフを生成し、最大深度とlatency分布を出力、可視化します。

例の出力:
- Max Ripple Depth: 3 (例)
- Latency Distribution: [2, 4, 1, ...] (平均: 2.5)

## コードの説明
- `simulate_ripple()`: 協力行動を表すランダムエッジ付きのdirected graphを生成。
- `calculate_depth()`: 指定の原点ノードからの最大伝播深度を計算。
- `get_latency_distribution()`: エッジのlatency値を抽出。
- `visualize_ripple()`: Matplotlibでグラフを描画。

## 拡張方法
実データを入れる場合:
- `simulate_ripple()` を修正し、実際のイベントに基づいてエッジを追加（例: ソーシャルネットワークのログから）。
- 例: `G.add_edge(0, 1, action="Response", latency=3)` でアクター0から1への協力イベントを追加。

詳細は論文(arXiv)参照、または連絡: kazutaka.hayashi@yorosix.com

## ライセンス
MIT License

