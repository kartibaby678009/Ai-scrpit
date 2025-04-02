from flask import Flask, render_template, request import requests import time import random

app = Flask(name)

USER_AGENTS = [ "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36", "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36", "Mozilla/5.0 (Android 10; Mobile; LG-M255) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.1 Safari/537.36", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0", "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36" ]

def get_random_user_agent(): return random.choice(USER_AGENTS)

def get_random_emoji(): emojis = ["🙂", "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"] return random.choice(emojis)

def post_comment(cookie, post_url, comment_text, user_agent): headers = { "User-Agent": user_agent, "Cookie": cookie } post_id = post_url.split("/")[-1] comment_url = f"https://graph.facebook.com/{post_id}/comments" data = { "message": comment_text + " " + get_random_emoji(), "access_token": "" } response = requests.post(comment_url, headers=headers, data=data) return response.json()

@app.route("/", methods=["GET", "POST"]) def index(): if request.method == "POST": with open("cookies.txt", "r") as f: cookies = f.readlines() with open("token.txt", "r") as f: tokens = f.readlines() with open("posturl.txt", "r") as f: post_url = f.read().strip() with open("time.txt", "r") as f: interval = int(f.read().strip())

for cookie in cookies:
        user_agent = get_random_user_agent()
        for token in tokens:
            response = post_comment(cookie.strip(), post_url, "Auto Comment", user_agent)
            print(response)
            time.sleep(interval + random.randint(1, 5))
    
    return "Auto Comments Sent Successfully!"

return render_template("index.html")

if name == "main": app.run(host="0.0.0.0", port=10000, debug=True)

