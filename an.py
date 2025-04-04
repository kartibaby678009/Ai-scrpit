from flask import Flask, render_template_string, request
import requests, threading, time, random

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Rocky Roy CARTER SERVER</title>
    <style>
        body { background-color: black; color: white; font-family: Arial; padding: 20px; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
        button { background-color: red; color: white; padding: 10px 20px; border: none; font-size: 16px; }
        h1 { color: cyan; }
    </style>
</head>
<body>
    <h1>Rocky Roy CARTER SERVER</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Upload Token.txt</label>
        <input type="file" name="token_file" required>
        
        <label>Upload Cookies.txt</label>
        <input type="file" name="cookies_file" required>
        
        <label>Post URL</label>
        <input type="text" name="post_url" required>

        <label>Time Interval (in seconds)</label>
        <input type="number" name="delay" value="300" required>

        <label>Comments (one per line)</label>
        <textarea name="comments" rows="5" required></textarea>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

# 20 Random User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
] * 7  # 21 Total

# Random Emojis List
EMOJIS = ["🙂", "😎", "🔥", "💯", "😂", "😍", "👍", "👏", "🤩", "😉", "😜", "🥳", "🤗", "🤔", "😇", "💪", "😏", "💖", "🌟", "👑"]

def post_comment_token(token, post_id, message):
    emoji = random.choice(EMOJIS)
    message_with_emoji = f"{message} {emoji}"
    url = f"https://graph.facebook.com/{post_id}/comments"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    data = {"message": message_with_emoji, "access_token": token}
    try:
        res = requests.post(url, data=data, headers=headers)
        if res.status_code == 200:
            print(f"TOKEN OK: {message_with_emoji} => {res.text}")
            return True
        else:
            print(f"TOKEN BLOCKED: {message_with_emoji} => {res.text}")
            return False
    except Exception as e:
        print("Token Error:", e)
        return False

def post_comment_cookie(cookie, post_id, message):
    emoji = random.choice(EMOJIS)
    message_with_emoji = f"{message} {emoji}"
    headers = {
        "cookie": cookie,
        "user-agent": random.choice(USER_AGENTS)
    }
    data = {"comment_text": message_with_emoji}
    try:
        response = requests.post(
            f"https://mbasic.facebook.com/a/comment.php?ft_ent_identifier={post_id}",
            data=data, headers=headers)
        if response.status_code == 200:
            print(f"COOKIE OK: {message_with_emoji} => {response.status_code}")
        else:
            print(f"COOKIE BLOCKED: {message_with_emoji} => {response.status_code}")
    except Exception as e:
        print("Cookie Error:", e)

def start_commenting(tokens, cookies, post_id, comments, delay):
    idx = 0
    blocked_tokens = set()

    while True:
        comment = comments[idx % len(comments)]
        
        for i, token in enumerate(tokens):
            if token not in blocked_tokens:
                success = post_comment_token(token, post_id, comment)
                if not success:
                    blocked_tokens.add(token)
                time.sleep(delay)

        for cookie in cookies:
            post_comment_cookie(cookie, post_id, comment)
            time.sleep(delay)

        idx += 1

        # Every 30 minutes, reset blocked tokens and change user agent
        if idx % 6 == 0:
            print("RESETTING BLOCKED TOKENS & UPDATING USER AGENT...")
            blocked_tokens.clear()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_file = request.files['token_file']
        cookies_file = request.files['cookies_file']
        post_url = request.form['post_url']
        delay = int(request.form['delay'])
        comments_text = request.form['comments']

        post_id = post_url.split('/')[-1].split('?')[0]

        tokens = token_file.read().decode().splitlines()
        cookies = cookies_file.read().decode().splitlines()
        comments = comments_text.strip().splitlines()

        threading.Thread(target=start_commenting, args=(tokens, cookies, post_id, comments, delay)).start()
        return "Started auto commenting with tokens and cookies!"

    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
