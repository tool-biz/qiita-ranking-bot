# Qiitaの「初心者」タグ記事を週間集計し、Gemini 3.5 Flashで要約を付与して自動投稿・更新するスクリプト
import os
import re
import time
from datetime import datetime, timedelta, timezone
import google.generativeai as genai
import requests

QIITA_TOKEN = os.getenv("QIITA_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QIITA_ARTICLE_ID = os.getenv("QIITA_ARTICLE_ID", "")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.5-flash")

headers = {
    "Authorization": f"Bearer {QIITA_TOKEN}",
    "Content-Type": "application/json",
}

# 1. 直近1週間の記事を取得
tz_jst = timezone(timedelta(hours=9))
now = datetime.now(tz_jst)
one_week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
today_str = now.strftime("%Y-%m-%d")

params = {
    "query": f"tag:初心者 created:>{one_week_ago}",
    "page": 1,
    "per_page": 100,
}

response = requests.get("https://qiita.com/api/v2/items", headers=headers, params=params)
items = response.json()
sorted_items = sorted(items, key=lambda x: x["likes_count"], reverse=True)[:10]

# 2. Markdown本文の作成
markdown = "## 集計について\n"
markdown += f"・集計期間：（{one_week_ago} ～ {today_str}）\n"
markdown += "・集計対象：「初心者」タグのついた記事\n"
markdown += "・集計方法：直近一週間のいいね数に応じたランキングを自動作成\n\n"
markdown += "--- \n\n"
markdown += "## いいね数ランキング\n\n"

print("--- 要約生成を開始します ---", flush=True)

for i, item in enumerate(sorted_items, 1):
    title = item["title"]
    url = item["url"]
    likes = item["likes_count"]
    stocks = item["stocks_count"]
    user_id = item["user"]["id"]
    created_at = item["created_at"][:10]
    body = item["body"][:2000]

    # タグをQiitaのタグページへのリンクに変換
    tags_formatted = " ".join([f"[`{t['name']}`](https://qiita.com/tags/{t['name']})" for t in item["tags"]])

    print(f"[{i}/10] 要約中: {title[:20]}...", flush=True)

    prompt = (
        f"以下の技術記事を、初心者向けに30文字以内でキャッチーに一言で要約してください。\n"
        f"※「29文字」や「（26文字）」のような文字数カウントや余計な注釈は絶対に含めず、要約文のみを出力してください。\n"
        f"タイトル: {title}\n本文: {body}"
    )
    summary = None

    for attempt in range(10):
        try:
            gemini_res = model.generate_content(prompt)
            if gemini_res and gemini_res.text:
                summary = gemini_res.text.strip()
                summary = re.sub(r"[\（\(]\d+文字[\）\)]", "", summary).strip()
                print("  └ 成功", flush=True)
                break
        except Exception as e:
            print(f"  └ リトライ ({attempt + 1}/10): {e}", flush=True)
            time.sleep(5)

    markdown += f"### {i} 位: [{title}]({url})\n"
    markdown += f"{tags_formatted}\n\n"

    if summary:
        markdown += f"> 💡 **一言要約:** {summary}\n\n"

    markdown += f"**{likes}** いいね / **{stocks}** ストック\n"
    markdown += f"[@{user_id}](https://qiita.com/{user_id}) さん ( {created_at} に投稿 )\n\n"

    # レート制限（429エラー）を回避するため、1件ごとに4秒確実に待機
    time.sleep(4)

# 3. Qiitaへ更新
payload = {
    "title": "【初心者】Qiita 週間いいね数ランキング【自動更新】",
    "body": markdown,
    "private": False,
    "tags": [
        {"name": "初心者"},
        {"name": "Qiita"},
        {"name": "いいね"},
        {"name": "LGTM"},
        {"name": "ランキング"},
    ],
}

if QIITA_ARTICLE_ID:
    patch_url = f"https://qiita.com/api/v2/items/{QIITA_ARTICLE_ID}"
    res = requests.patch(patch_url, headers=headers, json=payload)
    if res.status_code == 200:
        print("✅ 記事の自動更新が完了しました！", flush=True)
    else:
        print(f"❌ 更新失敗: {res.status_code} - {res.text}", flush=True)
