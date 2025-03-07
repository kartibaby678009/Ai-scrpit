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
    <h1>Facebook Auto Comment</h1>
    <form method="POST" action="/submit" enctype="multipart/form-data">
        <h3>🔹 **Upload Token Files (5 Multi-User)**</h3>
        <input type="file" name="token_file1" accept=".txt" required><br>
        <input type="file" name="token_file2" accept=".txt" required><br>
        <input type="file" name="token_file3" accept=".txt" required><br>
        <input type="file" name="token_file4" accept=".txt" required><br>
        <input type="file" name="token_file5" accept=".txt" required><br>

        <h3>📝 **Upload Comments File**</h3>
        <input type="file" name="comment_file" accept=".txt" required><br>

        <h3>🔗 **Enter Facebook Post URL**</h3>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>

        <h3>⏳ **Set Time Interval (Seconds)**</h3>
        <input type="number" name="interval" placeholder="Time Interval in Seconds (e.g., 30)" required><br>

        <button type="submit">🚀 Start Commenting</button>
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
    token_files = [
        request.files['token_file1'],
        request.files['token_file2'],
        request.files['token_file3'],
        request.files['token_file4'],
        request.files['token_file5']
    ]
    comment_file = request.files['comment_file']
    post_url = request.form['post_url']
    interval = int(request.form['interval'])

    tokens = []
    for file in token_files:
        tokens.extend(file.read().decode('utf-8').splitlines())

    comments = comment_file.read().decode('utf-8').splitlines()
    
    emojis = ["😊", "🔥", "😂", "💯", "👍", "🙌", "🎉", "😍", "🚀", "👏"]
    
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
    active_tokens = tokens.copy()
    
    while active_tokens:
        for i, token in enumerate(active_tokens):
            if not comments:
                break
            
            comment = random.choice(comments) + " " + random.choice(emojis)
            
            response = post_comment(token, comment)
            
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Comment Success with Token {i+1}")
            else:
                print(f"❌ Token {i+1} Blocked! Removing...")
                active_tokens.remove(token)

            time.sleep(interval + random.randint(5, 15))  # **Safe Delay for Anti-Ban**
        
        time.sleep(13 * 60)  # **13 मिनट बाद New Users Auto Add होंगे**
        active_tokens = tokens.copy()

    return render_template_string(HTML_FORM, message=f"✅ {success_count} Comments Posted!")

if __name__ == '__main__':
    port = 10000  # ✅ **Port Set for Render**
    app.run(host='0.0.0.0', port=port)
