# Ripple Structure Simulation

This repository provides a Python simulation for modeling "Ripple" structures from YOROSIX CSV data, as described in the paper "Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins" by Kazutaka Hayashi.

## Overview
Ripple structures represent directional causal chains of cooperative actions (e.g., A helps B → B helps C) as a directed temporal graph. This code uses NetworkX to model such graphs from multiple CSV files exported from YOROSIX Research Export Tool.

Nodes: Anonymized actors (users).
Edges: Cooperative actions (Response, Share, Visit, Thanks) with latency (time delay) and ripple_depth.

## Requirements
- Python 3.x
- Libraries: `networkx`, `matplotlib`, `numpy`, `pandas` (install via `pip install networkx matplotlib numpy pandas`)

## Usage
1. Export CSV files from YOROSIX tool (members.csv, posts.csv, replies.csv, share_links.csv, request_visits.csv, thanks_logs.csv) and place them in a folder.
2. Run the script with the folder path as argument:
python ripple_simulation.py /path/to/your/csv/folder

- If no path provided, defaults to 'data/' folder.
- This loads CSVs, builds the graph, computes max depth and latency distribution, and visualizes.

Example output:
- Loading from folder: /path/to/your/csv/folder
- Max Ripple Depth: 3 (example)
- Latency Distribution: [5.0, 0.0, ...] (Mean: 2.5)

## Code Explanation
- `load_yorosix_ripple(data_dir)`: Loads multiple CSVs, anonymizes IDs, adds nodes/edges from events.
- `calculate_depth()`: Computes maximum propagation depth.
- `get_latency_distribution()`: Extracts latency values.
- `visualize_ripple()`: Draws the graph with labels.

## Extension
Customize for your data:
- Adjust column names in code if CSVs vary.
- Add more event types or latency calculations.

For details, see the paper on arXiv or contact: kazutaka.hayashi@yorosix.com.

## License
MIT License



# リップル構造シミュレーション

このリポジトリは、林和孝の論文「Modeling Cooperation as Information Flow: Ripple Structures and Behavioral Digital Twins」で提案された「Ripple」構造を、YOROSIX CSVデータからモデル化するPythonシミュレーションを提供します。

## 概要
Ripple構造は、協力行動の方向性因果連鎖をdirected temporal graphとしてモデル化します。このコードはYOROSIX Research Export Toolからエクスポートした複数CSVを使ってグラフを構築します。

ノード: 匿名化されたアクター（ユーザー）。
エッジ: 協力行動（Response, Share, Visit, Thanks）で、latency（時間遅延）とripple_depth付き。

## 必要環境
- Python 3.x
- ライブラリ: `networkx`, `matplotlib`, `numpy`, `pandas` (`pip install networkx matplotlib numpy pandas` でインストール)

## 使い方
1. YOROSIXツールからCSVファイル（members.csv, posts.csv, replies.csv, share_links.csv, request_visits.csv, thanks_logs.csv）をエクスポートし、フォルダに置く。
2. スクリプトを実行し、フォルダパスを引数で指定:
python ripple_simulation.py /path/to/your/csv/folder

- パス指定なしなら'data/'フォルダをデフォルト使用。
- CSVをロードし、グラフ構築、最大深度/latency分布計算、可視化します。

例の出力:
- Loading from folder: /path/to/your/csv/folder
- Max Ripple Depth: 3 (例)
- Latency Distribution: [5.0, 0.0, ...] (平均: 2.5)

## コードの説明
- `load_yorosix_ripple(data_dir)`: 複数CSVをロード、ID匿名化、イベントからノード/エッジ追加。
- `calculate_depth()`: 指定原点からの最大伝播深度計算。
- `get_latency_distribution()`: エッジのlatency抽出。
- `visualize_ripple()`: Matplotlibでグラフ描画（ラベル付き）。

## 拡張方法
データに合わせてカスタム:
- CSVのカラム名が変わったらコードのrow['xxx']を調整。
- さらにイベントタイプやlatency計算を追加可能。

詳細は論文(arXiv)参照、または連絡: kazutaka.hayashi@yorosix.com。

## ライセンス
MIT License
