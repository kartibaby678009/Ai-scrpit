from flask import Flask, request, render_template_string
import requests
import time
import random

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, button { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Facebook Auto Comment</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <h3>📝 **Upload TOKEN File (Multi-User)**</h3>
        <input type="file" name="token_file" accept=".txt" required><br>

        <h3>📝 **Upload COMMENTS File**</h3>
        <input type="file" name="comment_file" accept=".txt" required><br>

        <h3>🔗 **Enter Facebook Post URL**</h3>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

        <h3>⏳ **Set Time Interval (Seconds)**</h3>
        <input type="number" name="interval" placeholder="Time Interval in Seconds (e.g., 30)" required><br>

        <button type="submit">🚀 Start Commenting</button>
    </form>
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
    
    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return "❌ Invalid Post URL!"

    url = f"https://graph.facebook.com/{post_id}/comments"

    blocked_tokens = []
    
    # 🔥 Random User-Agent List for Anti-Ban
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    ]

    def post_comment(token, comment):
        headers = {
            "User-Agent": random.choice(user_agents)  # 🔥 Random User-Agent Select होगा
        }
        payload = {'message': comment, 'access_token': token}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            blocked_tokens.append(token)
            return False

    while True:
        for token in tokens:
            if token in blocked_tokens:
                continue  
            for comment in comments:
                emoji_comment = comment + " " + random.choice(["😂", "🤣", "😍", "🔥", "💯", "❤️"])
                if post_comment(token, emoji_comment):
                    print(f"✅ Comment Success: {emoji_comment}")
                else:
                    print(f"❌ Token Blocked: {token}")
                time.sleep(interval)

        if not blocked_tokens:
            break  

        print("🔄 Checking Unblocked Tokens...")
        time.sleep(900)  # 15 मिनट का वेट करो (Unblock होने के लिए)

        for token in blocked_tokens[:]:
            test_url = f"https://graph.facebook.com/me?access_token={token}"
            headers = {
                "User-Agent": random.choice(user_agents)
            }
            if requests.get(test_url, headers=headers).status_code == 200:
                print(f"🔓 Token Unblocked: {token}")
                blocked_tokens.remove(token)

    return "✅ All Comments Posted!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
