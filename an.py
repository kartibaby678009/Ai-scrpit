from flask import Flask, request, render_template_string
import requests
import time
import random
import os

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment - Safe Mode</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, button { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Facebook Auto Comment - Safe Mode</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" required><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Time Interval in Seconds (e.g., 30)" required><br>
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
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = token_file.read().decode('utf-8').splitlines()
    comments = comment_file.read().decode('utf-8').splitlines()
    active_tokens = list(tokens)  # **Active Tokens List**

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

    def modify_comment(comment):
        """फेसबुक को स्पैम से बचाने के लिए Comment मॉडिफाई करेगा।"""
        emojis = ["🔥", "✅", "💯", "👏", "😊", "👍", "🙌", "🎉", "😉", "💪"]
        variations = ["!!", "!!!", "✔️", "...", "🤩", "💥"]
        return f"{random.choice(variations)} {comment} {random.choice(emojis)}"

    def post_with_token(token, comment):
        """Token से Facebook API को Comment भेजेगा।"""
        headers = {"User-Agent": random.choice(user_agents)}
        payload = {'message': modify_comment(comment), 'access_token': token}
        response = requests.post(url, data=payload, headers=headers)
        return response

    comment_index = 0
    while True:  # **Loop को Infinite कर दिया ताकि यह ऑल टाइम वर्क करे**
        if not active_tokens:
            active_tokens = list(tokens)  # **अगर सारे Tokens Block हो जाएं, तो List Reset कर दो**
            print("🔄 सभी Tokens Reset कर दिए गए!")

        token = active_tokens[comment_index % len(active_tokens)]
        comment = comments[comment_index % len(comments)]

        response = post_with_token(token, comment)

        if response.status_code == 200:
            success_count += 1
            print(f"✅ Token {comment_index+1} से Comment Success!")
        else:
            print(f"❌ Token {comment_index+1} Blocked, Removing...")
            active_tokens.remove(token)  # **Blocked Token को Remove कर दो**

        comment_index += 1  # **Next Comment के लिए Index Update करो**

        # **Safe Delay for Anti-Ban**
        safe_delay = interval + random.randint(10, 30)
        print(f"⏳ Waiting {safe_delay} seconds before next comment...")
        time.sleep(safe_delay)

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Successfully Posted!")

if __name__ == '__main__':
    port = 10000  # ✅ Port को 10000 कर दिया
    app.run(host='0.0.0.0', port=port)
