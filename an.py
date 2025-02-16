from flask import Flask, request, render_template_string
import requests
import time
import random

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment (100% Anti-Ban)</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Facebook Auto Comment - 100% Safe & Anti-Ban</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" required><br>
        <input type="file" name="cookie_file" accept=".txt"><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="file" name="proxy_file" accept=".txt"><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Interval in Seconds (e.g., 30)" required><br>
        <input type="number" name="run_time" placeholder="Total Run Time in Minutes (e.g., 60)" required><br>
        <button type="submit">Start Safe Commenting</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    token_file = request.files['token_file']
    cookie_file = request.files.get('cookie_file')
    comment_file = request.files['comment_file']
    proxy_file = request.files.get('proxy_file')
    post_url = request.form['post_url']
    interval = int(request.form['interval'])
    run_time = int(request.form['run_time']) * 60  # Convert minutes to seconds

    tokens = token_file.read().decode('utf-8').splitlines()
    cookies_list = cookie_file.read().decode('utf-8').splitlines() if cookie_file else []
    comments = comment_file.read().decode('utf-8').splitlines()
    proxies = proxy_file.read().decode('utf-8').splitlines() if proxy_file else []

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"
    success_count = 0

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)"
    ]

    def get_random_proxy():
        """Proxy को Random तरीके से Select करता है।"""
        if proxies:
            proxy = random.choice(proxies)
            return {"http": proxy, "https": proxy}
        return None

    def modify_comment(comment):
        """Facebook AI को चकमा देने के लिए Comment में Random Modification करेगा।"""
        emojis = ["🔥", "✅", "💯", "👏", "😊", "👍", "🙌"]
        return comment + " " + random.choice(emojis)

    def post_with_token(token, comment):
        headers = {"User-Agent": random.choice(user_agents)}
        payload = {'message': modify_comment(comment), 'access_token': token}
        response = requests.post(url, data=payload, headers=headers, proxies=get_random_proxy())
        return response

    def post_with_cookie(cookie, comment):
        headers = {
            "User-Agent": random.choice(user_agents),
            "Cookie": cookie
        }
        data = {"comment_text": modify_comment(comment)}
        fb_comment_url = f"https://m.facebook.com/comment/replies/?ft_ent_identifier={post_id}"
        session = requests.Session()
        response = session.post(fb_comment_url, headers=headers, data=data, proxies=get_random_proxy())
        return response

    token_index = 0
    start_time = time.time()

    while time.time() - start_time < run_time:
        if token_index >= len(tokens):  
            token_index = 0  # Restart from first token

        comment = comments[token_index % len(comments)]
        token = tokens[token_index]

        response = post_with_token(token, comment)

        if response.status_code == 200:
            success_count += 1
            print(f"✅ Comment Posted Successfully with Token {token_index + 1}")
        elif response.status_code in [400, 403]:
            print(f"❌ Token {token_index + 1} Blocked, Trying Next Token...")
        else:
            print(f"⚠️ Unexpected Error with Token {token_index + 1}, Skipping...")

        token_index += 1

        safe_delay = interval + random.randint(10, 30)
        print(f"⏳ Safe Waiting Time: {safe_delay} seconds before next comment...")
        time.sleep(safe_delay)

        if success_count % 10 == 0:
            long_break = random.randint(120, 300)
            print(f"😴 Taking a Long Break for {long_break} seconds...")
            time.sleep(long_break)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
