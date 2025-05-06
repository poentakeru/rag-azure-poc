# RAG Azure PoC

本プロジェクトは、Azure上で動作させることを想定した **RAG（Retrieval-Augmented Generation）構成のPoC** です。すべての機能を疎結合なAPIで構成し、再現性・移植性・可視性に優れた構造となっています。

---

## 💻 開発環境

本プロジェクトは以下の環境で動作確認されています：

- macOS (Apple M2)
- Docker Desktop 4.21.1 (114176)
- Python 3.11（ベースイメージ）
- VSCode + dev container（任意）
---
## 🔧 構成概要

本PoCは以下のマイクロサービスで構成されています：

| サービス名    | 説明                             | ポート |
|--------------|----------------------------------|--------|
| `retriever`  | クエリから類似チャンクを検索      | 8001   |
| `generator`  | クエリ＋文脈から回答を生成        | 8002   |
| `vector-db`  | ベクトル登録・検索（FAISS等想定） | 8003   |
| `controller` | 全体制御API。retriever→generator連携 | 8004   |
| `ui`         | Streamlitによる問い合わせUI       | 8501   |

---

## 🚀 クイックスタート

### 1. コンテナ起動

```bash
docker compose up --build
```

起動後、以下にアクセス：

UI: http://localhost:8501


### 2. 例：curlで直接APIを叩く

```bash
curl -X POST http://localhost:8004/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "乾電池の捨て方"}'
```
---
## 使用技術

- Python 3.11 + FastAPI
- Streamlit
- Docker / docker-compose
- FAISS（予定）
- Hugging Face Transformers（予定）
---
## 📝 今後の実装予定
- vector-db にFAISSを組み込み、チャンクベクトルの登録・検索を実装
- エンベディングモデルや生成モデルの選択切り替え機能（configで制御）
- Azure VMへの移植構成整備（App Gatewayやセキュリティを考慮）
- 精度評価用のベンチマークデータ整備
---
## 📁 ディレクトリ構成

```text
rag-azure-poc/
├── retriever/
├── generator/
├── vector-db/
├── controller/
├── ui/
├── docker-compose.yml
└── README.md
```
---