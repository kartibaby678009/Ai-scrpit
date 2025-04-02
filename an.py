from flask import Flask, render_template, request import requests import time import random

app = Flask(name)

User-Agent List (Auto Rotate Every 30 min)

USER_AGENTS = [ "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124", "Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/92.0.4515.107", "Mozilla/5.0 (X11; Linux x86_64) Chrome/91.0.4472.124", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) Safari/537.36", "Mozilla/5.0 (Android 10; Mobile; LG-M255) Chrome/89.0.4389.90", ]

def get_random_user_agent(): return random.choice(USER_AGENTS)

def get_random_emoji(): emojis = ["🙂", "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"] return random.choice(emojis)

def post_comment(cookie, token, post_url, comment_text, user_agent): headers = { "User-Agent": user_agent, "Cookie": cookie } post_id = post_url.split("/")[-1] comment_url = f"https://graph.facebook.com/{post_id}/comments" data = { "message": comment_text + " " + get_random_emoji(), "access_token": token } response = requests.post(comment_url, headers=headers, data=data) return response.json()

@app.route("/", methods=["GET", "POST"]) def index(): if request.method == "POST": with open("cookies.txt", "r") as f: cookies = f.readlines() with open("token.txt", "r") as f: tokens = f.readlines() with open("posturl.txt", "r") as f: post_url = f.read().strip() with open("time.txt", "r") as f: interval = int(f.read().strip())

for i, cookie in enumerate(cookies):
        user_agent = get_random_user_agent()
        token = tokens[i % len(tokens)].strip()
        response = post_comment(cookie.strip(), token, post_url, "Auto Comment", user_agent)
        print(response)
        time.sleep(interval + random.randint(1, 5))

    return "Auto Comments Sent Successfully!"

return render_template("index.html")

if name == "main": app.run(host="0.0.0.0", port=10000, debug=True)

