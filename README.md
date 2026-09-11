# qiita-ranking-bot

Qiita API × Gemini API × GitHub Actions で、
「初心者」タグのQiita記事を週間ランキング化する自動化ボットです。

Qiita記事リンク：https://qiita.com/tool-bizsystems/items/cc557b632df5ddfc8a58

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
