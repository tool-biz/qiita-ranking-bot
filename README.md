# qiita-ranking-bot

Qiita API × Gemini API × GitHub Actions で、
「初心者」タグのQiita記事を週間ランキング化する自動化ボットです。


## できること

- Qiita APIから「初心者」タグの記事を取得
- 直近1週間のいいね数でTOP10をランキング
- Gemini APIで各記事を一言要約
- Markdownを生成してQiita記事を自動更新
- GitHub Actionsで毎週自動実行

## 構成

```text
GitHub Actions
      ↓
   Qiita API
      ↓
記事取得・ランキング集計
      ↓
   Gemini API
      ↓
一言要約・Markdown生成
      ↓
   Qiita API
      ↓
   Qiita記事更新
```

## Tech Stack
- Python
- Qiita API
- Gemini API
- GitHub Actions

## 実際の成果物
#### Qiita記事

[「知らない技術でも、その日のうちに動かす」｜4時間でQiita API×Gemini×GitHub Actionsを自動化した話](https://qiita.com/tool-bizsystems/items/cc557b632df5ddfc8a58)

#### 自動更新されるランキング

[Qiita「初心者」タグ週間ランキング](https://qiita.com/tool-bizsystems/items/11e0cf9b2d863fd00036)

## 開発について

Git / GitHub / GitHub Actions / Qiita API は、
今回の開発着手時点ではほぼ未経験でした。

AIを活用しながら仕様を調べ、試行錯誤を繰り返して、
約4時間で本番で動くところまで実装しました。

詳しい開発記録はQiita記事をご覧ください。
