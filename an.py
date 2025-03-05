from flask import Flask, request, render_template_string
import requests
import time
import random
import os

app = Flask(__name__)

# ✅ HTML Form
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
    <h1>😈 Facebook Auto Comment 😈</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <input type="file" name="token_file" accept=".txt" required><br>
        <input type="file" name="comment_file" accept=".txt" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="number" name="interval" placeholder="Time Interval in Seconds (e.g., 30)" required><br>
        <button type="submit">🔥 Start Auto Commenting 😈</button>
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

    try:
        post_id = post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

    url = f"https://graph.facebook.com/{post_id}/comments"

    def post_comment(token, comment):
        payload = {'message': comment, 'access_token': token}
        response = requests.post(url, data=payload)
        return response

    success_count = 0
    failed_tokens = []

    for i, comment in enumerate(comments):
        token = tokens[i % len(tokens)]  # **हर बार नया Token यूज़ होगा**
        
        # ✅ **Emoji Support - Random Emoji Add करेंगे**
        emoji_list = ["😈", "🔥", "💀", "🚀", "🤖", "😂", "😎", "💪"]
        random_emoji = random.choice(emoji_list)
        comment_with_emoji = f"{comment} {random_emoji}"

        response = post_comment(token, comment_with_emoji)

        if response.status_code == 200:
            success_count += 1
            print(f"✅ Comment Success! Token {i+1} - {comment_with_emoji}")
        else:
            print(f"❌ Token {i+1} Blocked! Trying Next...")
            failed_tokens.append(token)

        # **Anti-Ban System: Random Delay**
        time.sleep(interval + random.randint(10, 60))  

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Posted! 🚀")

if __name__ == '__main__':
    port = 10000  # ✅ Render & Replit Compatible Port
    app.run(host='0.0.0.0', port=port)
