from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key="ENTER YOUR API KEY")

app = Flask(__name__)
model = genai.GenerativeModel('gemini-3.5-flash')

@app.route('/')
def home():
    return """
<html><head>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
body{font-family:Arial;background:#121212;color:white}
.box{max-width:600px;margin:auto;text-align:center;padding-top:20px}
#chat{text-align:left;margin-top:20px}
input{width:80%;padding:10px;border-radius:5px;border:none}
button{padding:10px;background:#4fc3f7;border:none;border-radius:5px;cursor:pointer}
.ai{background:#1e1e1e;padding:10px;border-radius:10px;margin:10px 0}
</style>
</head><body>
<div class="box">
<h2>🤖 EduGenie - Unga AI</h2>
<div id="chat"></div><br>
<input id="q" placeholder="Edhavadhu kelu...">
<button onclick="send()">Send</button>
</div>
<script>
async function send(){
 let q=document.getElementById('q').value;
 if(!q)return;
 document.getElementById('chat').innerHTML+=`<div>You: ${q}</div>`;
 document.getElementById('q').value='';
 let res=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
 let data=await res.json();
 document.getElementById('chat').innerHTML+=`<div class="ai">${marked.parse(data.answer)}</div>`;
}
</script>
</body></html>
"""

@app.route('/ask', methods=['POST'])
def ask():
    q = request.json['question']
    r = model.generate_content(q)
    return jsonify({'answer': r.text})

if __name__ == '__main__':
    app.run(debug=True)