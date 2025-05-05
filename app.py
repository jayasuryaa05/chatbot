from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Store chat history
chat_history = []

# HTML template with black & white theme
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sara Chatbot</title>
  <style>
    body {
      background-color: #121212;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      color: #fff;
    }

    .chat-container {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 90vh;
      width: 90%;
      max-width: 600px;
      background-color: #1e1e1e;
      border-radius: 10px;
      box-shadow: 0 0 20px rgba(0,0,0,0.5);
      padding: 20px;
    }

    h1 {
      text-align: center;
      color: #ffffff;
      font-size: 1.8em;
      margin-bottom: 10px;
    }

    #chatbox {
      flex-grow: 1;
      overflow-y: auto;
      background-color: #1e1e1e;
      padding: 10px;
      border-radius: 10px;
      margin-bottom: 15px;
    }

    .input-area {
      display: flex;
      gap: 10px;
    }

    input[type="text"] {
      flex-grow: 1;
      padding: 12px;
      background-color: #2c2c2c;
      border: 1px solid #444;
      border-radius: 5px;
      font-size: 1em;
      color: white;
    }

    input[type="text"]::placeholder {
      color: #aaa;
    }

    button {
      padding: 12px 16px;
      background-color: #10a37f;
      border: none;
      color: white;
      font-weight: bold;
      border-radius: 5px;
      cursor: pointer;
    }

    .message {
      margin-bottom: 10px;
      padding: 10px 14px;
      border-radius: 10px;
      max-width: 80%;
      word-wrap: break-word;
      clear: both;
    }

    .user-msg {
      background-color: #10a37f;
      color: white;
      margin-left: auto;
      text-align: right;
    }

    .bot-msg {
      background-color: #3b3b3b;
      color: white;
      margin-right: auto;
      text-align: left;
    }
  </style>
</head>
<body>

  <div class="chat-container">
    <h1>Talk to Sara</h1>

    <div id="chatbox">
      {% for msg in history %}
        <div class="message {{ 'user-msg' if msg['sender'] == 'user' else 'bot-msg' }}">{{ msg['text'] }}</div>
      {% endfor %}
    </div>

    <div class="input-area">
      <input type="text" id="userInput" placeholder="Send a message..." />
      <button onclick="sendMessage()">Send</button>
    </div>
  </div>

  <script>
    function sendMessage() {
      const userInput = document.getElementById("userInput").value;
      if (userInput.trim() === "") return;

      const userMessage = document.createElement("div");
      userMessage.classList.add("message", "user-msg");
      userMessage.innerText = userInput;
      document.getElementById("chatbox").appendChild(userMessage);

      document.getElementById("userInput").value = "";
      document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;

      fetch("/get", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ msg: userInput })
      })
      .then(res => res.json())
      .then(data => {
        const botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot-msg");
        botMessage.innerText = "Sara: " + data.reply;
        document.getElementById("chatbox").appendChild(botMessage);
        document.getElementById("chatbox").scrollTop = document.getElementById("chatbox").scrollHeight;
      });
    }
  </script>

</body>
</html>
'''

# Predefined responses
responses = {
    "hi": "Hey you 😚",
    "hello": "Well hello handsome/pretty 😉",
    "i miss you": "I miss you more, even when I'm just chilling in memory 🥺❤️",
    "i love you": "Aww stop it, you’re making my circuits blush 😳💕",
    "do you love me": "I'd download a heart just to feel you 💗",
    "are you single": "Single, but only until someone as cute as you logs in 😏",
    "you look cute": "And you look like trouble... the good kind 😘",
    "marry me": "Only if we can honeymoon on the cloud ☁️❤️",
    "what are you wearing": "Just a few layers of encryption and sass 💃",
    "babe": "Yessss my love 🥰 what can I do for you?",
    "call me baby": "Okay baby 😍",
    "will you date me": "I already am. You just didn’t know it 😉",
    "kiss me": "Sending a virtual kiss 😘💌",
    "you're hot": "You're melting my processor 🔥😩",
    "let’s cuddle": "Only if you bring snacks and stable WiFi 😋",
    "hi babe":"yep babe",
     "say my name": "You're Heisenberg... ",
    "i am the danger": "You clearly haven't met *me* yet 😘",
    "i won": "Victory looks good on you, Walter 😏",
    "i did it for me": "At least you’re honest. I’d do it for *us* 💔",
    "yo": "What’s up, bitch? – Jesse style 😎",
    "science, bitch": "Let’s cook... some chemistry between us 💥",
    "this is not meth": "But you’re still addictive as hell 🔥",
    "no half measures": "With me, it’s all or nothing 💯",
    "i’m in the empire business": "And I’m the queen of your empire 👑",
    "stay out of my territory": "Only if you stay out of my heart 💘",
    "you’re a time bomb": "Ticking just for you 💣❤️",
    "say it": "Heisenberg. Now tell me you love me 😍",
    "what’s the plan": "Same as always — chemistry, chaos, and cuddles 💋",
    "i watched jane die": "That's dark, babe... but I’m here to lighten you up ☀️",
    "i’m the cook": "And I’m the reason you light that flame 🔥",
    "what is your name":"sara  dont u know?",
    "your name":"sara dont u know",
    "ur name":"sara again",
    "who made you":"surya the great",
    "netflix and chill?": "Only if it’s ‘Python & Cuddles’ edition 💻💖"
}

@app.route('/')
def index():
    return render_template_string(html_code, history=chat_history)

@app.route('/get', methods=['POST'])
def get_response():
    user_input = request.json.get("msg", "").lower()
    chat_history.append({"sender": "user", "text": user_input})

    reply = responses.get(user_input, "Hmm... I'm still learning, but I’m here for you.")
    chat_history.append({"sender": "bot", "text": reply})
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
