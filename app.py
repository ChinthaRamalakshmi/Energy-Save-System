import os
from dotenv import load_dotenv

load_dotenv()
import smtplib
from email.mime.text import MIMEText
from flask import request, jsonify
from flask import Flask, render_template_string, url_for,request, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
#-----------------mail config----------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
#-----------------mail functon---------------

def send_email(to_email, data, limit, status):

    morning = data.get("morning", 0)
    afternoon = data.get("afternoon", 0)
    night = data.get("night", 0) 

    usage = morning + afternoon + night

    subject = "⚡ Energy Usage Report"

    labels = ["Morning", "Afternoon", "Night"]
    values = [morning, afternoon, night]

    # 📈 Peak hour detection
    peak_index = values.index(max(values))
    peak_time = labels[peak_index]

    # ⚡ STATUS
    if status == "cross":
        color = "#ff4d4d"
        title = "⚠ ENERGY LIMIT EXCEEDED"
        status_text = "OVER LIMIT ⚠"
    else:
        color = "#00c851"
        title = "✅ ENERGY USAGE REPORT"
        status_text = "SAFE ✅"

    # 💡 SUGGESTIONS
    if peak_time == "Morning":
        suggestion = """
🔴 Morning Peak Usage Detected

💡 Suggestions:
- Reduce TV usage in morning
- Avoid simultaneous Fan + TV usage
- Use natural light instead of lights
"""
    elif peak_time == "Afternoon":
        suggestion = """
🔴 Afternoon Peak Usage Detected (HIGH LOAD AREA)

💡 Suggestions:
- AC is major consumer → reduce usage
- Avoid fridge overuse
- Do not run multiple devices together
"""
    else:
        suggestion = """
🔴 Night Peak Usage Detected

💡 Suggestions:
- Reduce AC usage
- Turn off unnecessary lights
- Use sleep mode
"""

    # 🔥 IMPORTANT: NGROK LINK USE CHEY
    analysis_link = analysis_link = f"/analysis?morning={morning}&afternoon={afternoon}&night={night}"  # 👉 nee real link ikada paste chey

    # 📩 EMAIL BODY
    body = f"""
<html>
<body style="font-family:Arial;background:#f4f4f4;padding:20px;">

    <div style="max-width:600px;margin:auto;
                background:#000;
                color:white;
                padding:20px;
                border-radius:12px;
                box-shadow:0 0 15px rgba(0,0,0,0.6);">

        <h2 style="color:#00f2ff;text-align:center;">
            ⚡ {title}
        </h2>

        <hr style="border:0;height:1px;background:#333;">

        <div style="background:#111;padding:15px;border-radius:10px;">
            <p><b>📊 Total Usage:</b> {usage} units</p>
            <p><b>📉 Limit:</b> {limit} units</p>
            <p><b>📈 Peak Time:</b> {peak_time}</p>
            <p><b>⚡ Status:</b> {status_text}</p>
        </div>

        <br>

        <div style="text-align:center;margin:20px;">
            <a href="{analysis_link}" target="_blank"
               style="background:#00c6ff;color:black;
                      padding:12px 20px;
                      text-decoration:none;
                      border-radius:8px;
                      font-weight:bold;">
                📊 View Full Energy Dashboard
            </a>
        </div>

        <div style="background:#111;padding:15px;border-radius:10px;">
            <h3 style="color:#00f2ff;">💡 Smart Suggestions</h3>
            <pre style="white-space:pre-wrap;font-family:Arial;color:white;">
{suggestion}
            </pre>
        </div>

        <p style="
    font-size:18px;
    font-weight:bold;
    padding:10px;
    border-radius:8px;
    text-align:center;
    background:{'#ff1a1a' if status=='cross' else '#00c851'};
    color:white;
    box-shadow:0 0 15px {('#ff1a1a' if status=='cross' else '#00c851')};
">
    ⚡ STATUS: {status_text}
</p>

    </div>

</body>
</html>
"""
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    msg.attach(MIMEText(body, "html"))


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

#-----------------add backend route----------
@app.route('/send_email_multiple', methods=['POST'])
def send_email_multiple():
    data = request.get_json()

    emails = data["emails"]
    limit = data.get("limit", 0)
    status = data.get("status", "safe")

    # 👉 GET ENERGY FROM SESSION (NOT from POST)
    energy = session.get("energy", {
        "morning": 0,
        "afternoon": 0,
        "night": 0
    })

    for email in emails:
        email = email.strip()
        if email:
            send_email(email, energy, limit, status)

    return jsonify({"ok": True})

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template_string("""
<html>
<head>
<style>

/* REMOVE ALL DEFAULT GAPS */
html, body{
margin:0;
padding:0;
}

/* BODY */
body{
background:linear-gradient(#0f2027,#2c5364);
color:white;
font-family:Arial;
overflow:hidden;
}

/* TOP BAR */
.topbar{
display:flex;
height:12vh;        /* 🔥 12% height */
width:100%;
background:white;
}

/* LOGO */
.logo{
width:10%;
height:100%;
object-fit:fill;   /* 🔥 FULL COVER */
display:block;
}

/* HEADER */
.header-img{
width:90%;
height:100%;
object-fit:fill;   /* 🔥 FULL COVER */
display:block;
}

/* SCROLL TEXT */
.marquee{
color:yellow;
font-size:20px;
text-align:center;
margin-top:5px;
}

/* PARTICLES */
.particle{
position:absolute;
bottom:-10px;
width:6px;
height:6px;
background:#00f2ff;
border-radius:50%;
animation:rise linear infinite;
}
@keyframes rise{
0%{transform:translateY(0);}
100%{transform:translateY(-110vh);}
}

/* CARD */
.card{
width:700px;
margin:5% auto;
padding:30px;
background:rgba(0,0,0,0.7);
border-radius:20px;
text-align:center;
box-shadow:0 0 20px #00f2ff;
}

button{
padding:12px 25px;
background:#00c6ff;
border:none;
border-radius:10px;
color:white;
cursor:pointer;
}

</style>
</head>

<body>

<!-- 🔥 TOP BAR -->
<div class="topbar">
    <img src="{{ url_for('static', filename='logo.png') }}" class="logo">
    <img src="{{ url_for('static', filename='header.png') }}" class="header-img">
</div>

<!-- SCROLL -->
<div class="marquee">
<marquee>Artificial Intelligence and Data Science</marquee>
</div>

<!-- PARTICLES -->
{% for i in range(30) %}
<div class="particle"
style="left:{{range(0,100)|random}}vw;
animation-duration:{{range(4,8)|random}}s;"></div>
{% endfor %}

<h1 style="text-align:center;color:#00f2ff;">⚡ Energy Save System</h1>
                                  
<div class="card">
  <p>Monitor your energy usage efficiently.</p>
  <p>Analyze and reduce power usage.</p>
  <a href="/input"><button>🚀 Start Analysis</button></a>                                
</div>
<div style="
    width:300px;
    margin:25px auto;
    padding:15px;
    background:#ff2e88;
    border-radius:15px;
    text-align:center;
    color:white;
    font-weight:bold;
    box-shadow:0 0 20px #ff2e88;
    position:relative;
    z-index:999;
">
    <h3>Presented by</h3>
    <p>Ch.Ramalakshmi</p>
    <p>K.Nityaprasanthi</p>
    <p>Ch.Gayatri</p>                              
    
</div>                                                                 

</body>
</html>
""")

# ---------------- INPUT PAGE ----------------
@app.route('/input')
def input_page():
    return render_template_string("""
<html>
<head>
<style>
body{
margin:0;
background:linear-gradient(#1a002e,#3a0ca3);
color:white;
text-align:center;
font-family:Arial;
overflow:hidden;
}

/* ⚡ LIGHTNING EFFECT (ONLY ADDED - NO OTHER CHANGE) */
.lightning{
position:absolute;
bottom:-20px;
font-size:18px;
color:#00f2ff;
animation:rise linear infinite;
opacity:0.8;
}

@keyframes rise{
0%{transform:translateY(0);opacity:0.8;}
100%{transform:translateY(-110vh);opacity:0;}
}

/* CARD */
.card{
width:750px;
margin:5% auto;
padding:20px;
background:rgba(0,0,0,0.7);
border-radius:15px;
}

table{
width:100%;
border-collapse:collapse;
margin-top:15px;
}
th,td{
padding:10px;
border:1px solid white;
}
input{
width:70px;
padding:5px;
text-align:center;
}

/* BUTTON */
button{
padding:10px 20px;
margin:10px;
background:#ff4dff;
border:none;
color:white;
border-radius:8px;
cursor:pointer;
}
#area{
    position:relative;
    z-index:20;
    margin-top:20px;
}
</style>

<script>
let appliances={
morning:["Fan","Lights","TV","Mobile"],
afternoon:["Fan","AC","Fridge","Laptop"],
night:["Lights","Fan","AC","TV"]
};

let data={morning:0,afternoon:0,night:0};
let current="";

function load(time){
    current = time;

    let html = `<table>
        <tr><th>Appliance</th><th>Watts</th><th>Hours</th></tr>`;

    appliances[time].forEach((a,i)=>{
        html += `
        <tr>
            <td>${a}</td>
            <td>
  <input id="${time}_${i}_w"
  onkeydown="moveToHour(event,'${time}_${i}_h')">
</td>

<td>
  <input id="${time}_${i}_h"
  onkeydown="moveToNextRow(event,${i})">
</td>
        </tr>`;
    });

    html += `</table>
    <button onclick="calc()">Calculate</button>`;

    let area = document.getElementById("area");

    // 🔥 FORCE RENDER RESET
    area.innerHTML = "";
    setTimeout(()=>{
        area.innerHTML = html;
    }, 50);
}

function next(e,id){
if(e.key==="Enter"){
e.preventDefault();
document.getElementById(id).focus();
}
}

function nextRow(e,i){
if(e.key==="Enter"){
e.preventDefault();
let next=document.getElementById(current+"_"+(i+1)+"_w");
if(next) next.focus();
}
}

function calc(){
let total=0;

appliances[current].forEach((a,i)=>{
let w=document.getElementById(current+"_"+i+"_w").value;
let h=document.getElementById(current+"_"+i+"_h").value;

if(w!="" && h!="" && w!="-"){
total+=(w*h)/1000;
}
});

data[current]=total;
localStorage.setItem("energy",JSON.stringify(data));
fetch("/save_energy", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
});
alert(current+" units = "+total.toFixed(2));
}
                                  function moveToHour(e,id){
    if(e.key === "Enter"){
        e.preventDefault();
        document.getElementById(id).focus();
    }
}

function moveToNextRow(e,i){
    if(e.key === "Enter"){
        e.preventDefault();

        let next = document.getElementById(current+"_"+(i+1)+"_w");
        if(next){
            next.focus();
        }
    }
}
</script>

</head>

<body>

<!-- ⚡ LIGHTNING EFFECT (ONLY ADDED HERE) -->
{% for i in range(30) %}
<div class="lightning"
style="left:{{range(0,100)|random}}vw;
animation-duration:{{range(3,7)|random}}s;">
⚡
</div>
{% endfor %}

<div class="card">
<h2>Enter Energy Data</h2>

<div style="position:relative;z-index:50;">

<button onclick="load('morning')">Morning ☀️</button>
<button onclick="load('afternoon')">Afternoon 🌤️</button>
<button onclick="load('night')">Night 🌙</button>
<div id="area"></div>

</div>

<div style="display:flex;justify-content:space-between;">
    
    <a href="/"><button class="nav-btn back">⬅ Back</button></a>

    <a href="/analysis"><button class="nav-btn next">Next ➡</button></a>

</div>

</body>
</html>
""")
# ---------------- ANALYSIS PAGE ----------------
@app.route('/analysis')
def analysis():
    return render_template_string("""
<html>
<head>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body{
margin:0;
overflow:hidden;
font-family:Arial;
background:linear-gradient(#0f2027,#203a43);
color:white;
text-align:center;
}

/* BUBBLES */
.bubble{
position:absolute;
bottom:-50px;
width:12px;
height:12px;
background:rgba(0,255,255,0.3);
border-radius:50%;
animation:rise linear infinite;
}

@keyframes rise{
0%{transform:translateY(0);opacity:0.7;}
100%{transform:translateY(-110vh);opacity:0;}
}

/* BOXES */
.flex{
display:flex;
justify-content:center;
gap:20px;
margin-top:20px;
position:relative;
z-index:2;
}

.box{
background:rgba(0,0,0,0.7);
padding:15px;
border-radius:10px;
width:200px;
}

.box.peak{
box-shadow:0 0 20px gold;
border:2px solid gold;
}

/* CHART */
.chart{
display:flex;
justify-content:center;
gap:20px;
margin-top:30px;
flex-wrap:wrap;
position:relative;
z-index:2;
}

canvas{
width:380px !important;
height:360px !important;
background:white;
border-radius:10px;
}

/* BUTTON */
button{
margin-top:20px;
padding:10px 20px;
background:white;
border:none;
color:black;
border-radius:8px;
cursor:pointer;
font-weight:bold;
position:relative;
z-index:2;
}
</style>
</head>

<body>

<!-- 🫧 BUBBLES (same style as page 1) -->
<script>
for(let i=0;i<35;i++){
let b=document.createElement("div");
b.className="bubble";
b.style.left=Math.random()*100+"vw";
b.style.width=(8+Math.random()*20)+"px";
b.style.height=b.style.width;
b.style.animationDuration=(4+Math.random()*6)+"s";
document.body.appendChild(b);
}
</script>

<h2 style="position:relative;z-index:2;">⚡ Energy Analysis Dashboard</h2>

<div class="flex">
<div class="box" id="total"></div>
<div class="box" id="peakBox"></div>
<div class="box" id="cost"></div>
</div>

<div class="chart">
<canvas id="line"></canvas>
<canvas id="pie"></canvas>
</div>

<div style="display:flex;justify-content:space-between;justify-content:center;gap:20px;">
    
    <a href="/input"><button class="nav-btn back">⬅ Back</button></a>

    <a href="/alert"><button class="nav-btn next">Next ➡</button></a>

</div>

<script>

let urlParams = new URLSearchParams(window.location.search);

let m = Number(urlParams.get("morning"));
let a = Number(urlParams.get("afternoon"));
let n = Number(urlParams.get("night"));

if(!m && !a && !n){
    let d = JSON.parse(localStorage.getItem("energy")) || {morning:0,afternoon:0,night:0};
    m = Number(d.morning);
    a = Number(d.afternoon);
    n = Number(d.night);
}

let values = [m,a,n];
let labels = ["Morning","Afternoon","Night"];

/* TOTAL */
let total = values.reduce((x,y)=>x+y,0);

/* PEAK */
let max = Math.max(...values);
let index = values.indexOf(max);
let names = ["Morning","Afternoon","Night"];

/* COST */
let costPerUnit = 5;
let totalCost = total * costPerUnit;

/* BOXES */
document.getElementById("total").innerHTML =
"⚡ Total Units<br>" + total.toFixed(2);

let peakBox = document.getElementById("peakBox");
peakBox.innerHTML =
"Peak: " + names[index] +
"<br>Units: " + values[index].toFixed(2);

if(max>0){
peakBox.classList.add("peak");
}

document.getElementById("cost").innerHTML =
"💰 Full Day Cost<br>₹ " + totalCost.toFixed(2);

/* 📈 LINE GRAPH (same style as your code) */
new Chart(document.getElementById("line"),{
type:'line',
data:{
labels:labels,
datasets:[

{
label:"Morning 🌅",
data:[0, m, 0],
borderColor:"red",
backgroundColor:"rgba(255,0,0,0.2)",
tension:0.6,
pointRadius:6,
fill:true
},

{
label:"Afternoon ☀️",
data:[0, a, 0],
borderColor:"blue",
backgroundColor:"rgba(0,0,255,0.2)",
tension:0.6,
pointRadius:6,
fill:true
},

{
label:"Night 🌙",
data:[0, n, 0],
borderColor:"green",
backgroundColor:"rgba(0,255,0,0.2)",
tension:0.6,
pointRadius:6,
fill:true
}

]
},
options:{
plugins:{
legend:{labels:{color:"black"}},
tooltip:{
callbacks:{
label:function(ctx){
return ctx.dataset.label+" : "+ctx.raw+" units ⚡";
}
}
}
}
}
});

/* 🥧 PIE CHART (100% distribution) */
new Chart(document.getElementById("pie"),{
type:'pie',
data:{
labels:labels,
datasets:[{
data:values,
backgroundColor:["red","blue","green"]
}]
},
options:{
plugins:{
tooltip:{
callbacks:{
label:function(ctx){
let sum = values.reduce((a,b)=>a+b,0)||1;
let percent = (ctx.raw/sum*100).toFixed(1);
return ctx.label+" : "+ctx.raw+" units ("+percent+"%)";
}
}
}
}
}
});

</script>

</body>
</html>
""")
# ---------------- ALERT SYSTEM PAGE ----------------
@app.route('/alert')
def alert():
    return render_template_string("""
<html>
<head>
<style>

body{
margin:0;
background:linear-gradient(135deg,#1a001a,#ff0055);
font-family:Arial;
overflow:hidden;
text-align:center;
color:white;
}

.symbol{
position:absolute;
bottom:-50px;
font-size:18px;
color:white;
opacity:0.9;
animation:rise linear infinite;
}

@keyframes rise{
0%{transform:translateY(0);opacity:0.9;}
100%{transform:translateY(-110vh);opacity:0;}
}

.card{
width:500px;
margin:10% auto;
padding:25px;
background:rgba(0,0,0,0.8);
border-radius:15px;
box-shadow:0 0 25px #ff006e;
}

textarea{
width:90%;
height:100px;
padding:10px;
margin:10px;
border:none;
border-radius:8px;
text-align:center;
}

input{
width:80%;
padding:10px;
margin:10px;
border:none;
border-radius:8px;
text-align:center;
}

button{
padding:10px 20px;
border:none;
border-radius:8px;
cursor:pointer;
margin:5px;
}

.activate{
background:#ff006e;
color:white;
}

.next{
background:white;
color:black;
font-weight:bold;
}

</style>

<script>
function sendAlert(){

fetch("/get_energy")
.then(res => res.json())
.then(usage => {

    let m = usage.morning;
    let a = usage.afternoon;
    let n = usage.night;

    let total = m + a + n;

    let suggestion = "";

    if(m > a && m > n){
        suggestion = "Morning usage high → reduce lights & TV";
    }
    else if(a > m && a > n){
        suggestion = "Afternoon usage high → reduce AC usage";
    }
    else{
        suggestion = "Night usage high → reduce AC & lights";
    }

    localStorage.setItem("suggestion_text", suggestion);

    // 👉 NOW safe to use
    let emails = document.getElementById("emails").value.split(",");
    let limit = Number(document.getElementById("limit").value);

    let status = (total > limit) ? "cross" : "safe";

    fetch("/send_email_multiple", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            emails:emails,
            usage:total,
            limit:limit,
            status:status
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Emails Sent ⚡");
    });

});

}
</script>

</head>

<body>

{% for i in range(35) %}
<div class="symbol"
style="left:{{range(0,100)|random}}vw;
animation-duration:{{range(3,7)|random}}s;">
⚠
</div>
{% endfor %}

<div class="card">
<h2>⚡ Energy Alert System</h2>

<textarea id="emails" placeholder="Enter emails separated by comma
example:
abc@gmail.com, xyz@gmail.com"></textarea>

<input id="limit" type="number" placeholder="Unit Limit">

<br>

<button class="activate" onclick="sendAlert()">
Activate (Send to All)
</button>

<div style="display:flex;justify-content:space-between;justify-content:center;gap:20px;">

    <a href="/analysis"><button class="nav-btn back">⬅ Back</button></a>

    <a href="/tips"><button class="nav-btn next">Next ➡</button></a>

</div>

</div>

</body>
</html>
""")
# ---------------- TIPS PAGE ----------------
@app.route('/tips')
def tips():
    return render_template_string("""
<html>
<head>
<style>
body{
margin:0;
background:linear-gradient(#200122,#ff6a00);
color:white;
text-align:center;
font-family:Arial;
overflow:hidden;
}

.light{
position:absolute;
bottom:-20px;
font-size:20px;
animation:rise linear infinite;
}
@keyframes rise{
0%{transform:translateY(0);}
100%{transform:translateY(-110vh);}
}

.card{
width:600px;
margin:8% auto;
padding:25px;
background:rgba(0,0,0,0.7);
border-radius:15px;
}
</style>
</head>

<body>

{% for i in range(25) %}
<div class="light"
style="left:{{range(0,100)|random}}vw;
animation-duration:{{range(3,7)|random}}s;">⚡</div>
{% endfor %}

<div class="card">
<h2>Energy Saving Tips</h2>
<div id="suggestionBox"></div>

<script>
let suggestion = localStorage.getItem("suggestion_text");

if(suggestion){
    document.getElementById("suggestionBox").innerHTML =
    `<div style="
        background:rgba(0,0,0,0.6);
        padding:15px;
        margin:15px auto;
        border-radius:10px;
        width:80%;
        color:#00f2ff;
        font-weight:bold;
    ">
        ⚡ Smart Suggestion:<br><br>
        ${suggestion}
    </div>`;
}
</script>

<p>💡 Turn off unused devices</p>
<p>💡 Use LED bulbs</p>
<p>💡 Reduce AC usage</p>

<h3>Save Energy, Save Money, Save Earth 🌍</h3>

<div style="display:flex;justify-content:space-between;justify-content:center;gap:20px;">

    <a href="/alert"><button class="nav-btn back">⬅ Back</button></a>

    <a href="/"><button class="nav-btn next">🏠 Home</button></a>

</div>
</div>

</body>
</html>
""")
@app.route('/get_energy')
def get_energy():
    return jsonify(session.get('energy', {
        "morning": 0,
        "afternoon": 0,
        "night": 0
    }))

# ---------------- RUN ----------------
@app.route('/save_energy', methods=['POST'])
def save_energy():
    session['energy'] = request.get_json()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)