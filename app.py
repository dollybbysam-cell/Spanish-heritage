import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.write("Type a name, customize its look, and add a looping motion effect.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=52, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Sky", "Sunset", "Lavender", "Forest", "Ocean"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=1, max_value=10, value=5,
                      help="1 is slowest and 10 is fastest.")

backgrounds = {
    "Light": ("#ffffff", "#171717"),
    "Dark": ("#10131c", "#ffffff"),
    "Sky": ("linear-gradient(135deg, #8bd3ff, #eaf9ff)", "#102a43"),
    "Sunset": ("linear-gradient(135deg, #ff9966, #ff5e62, #6a3093)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #e7d8ff, #fbe4f2)", "#35204d"),
    "Forest": ("linear-gradient(135deg, #163a2a, #6b9b70)", "#ffffff"),
    "Ocean": ("linear-gradient(135deg, #005c97, #363795)", "#ffffff"),
}
bg, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")
safe_font = font_family.replace("'", "").replace('"', "")
duration = round(2.8 - (speed - 1) * 0.23, 2)

# Make a set of varied particles. CSS animates them in the browser, independently
# of Streamlit reruns, so the effects loop continuously without time.sleep().
particle_count = 46 if effect in ("Rain", "Snow", "Hail", "Confetti") else 18
symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄", "❅", "❆", "✳"],
    "Hail": ["●", "◆", "🧊"],
    "Wind Gust": ["〰", "﹏", "➝", "💨"],
    "Confetti": ["🎉", "✦", "●", "■", "▲", "★"],
    "Tornado": ["〰", "🌀", "·", "✦"],
}
particles = ""
if effect != "None":
    for i in range(particle_count):
        symbol = random.choice(symbols[effect])
        left = random.randint(1, 98)
        delay = random.uniform(-duration, 0)
        size = random.randint(12, 27) if effect != "Tornado" else random.randint(15, 30)
        drift = random.randint(-90, 90)
        fall_duration = duration * random.uniform(0.8, 1.8)
        particles += (
            f'<span class="particle p{i}" style="left:{left}%;'
            f'animation-delay:{delay:.2f}s;animation-duration:{fall_duration:.2f}s;'
            f'font-size:{size}px;--drift:{drift}px;">{html.escape(symbol)}</span>'
        )

if name_mode == "Repeated":
    name_content = '<div class="repeated">' + "".join(
        f'<div>{safe_name}</div>' for _ in range(5)
    ) + "</div>"
elif name_mode == "Ticker Tape":
    name_content = (
        '<div class="ticker"><div class="ticker-track">'
        f'<span>{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;</span>'
        f'<span>{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;</span>'
        "</div></div>"
    )
else:
    name_content = f'<div class="center-name">{safe_name}</div>'

effect_class = {
    "None": "no-effect",
    "Rain": "rain",
    "Snow": "snow",
    "Hail": "hail",
    "Wind Gust": "wind",
    "Confetti": "confetti",
    "Tornado": "tornado",
}[effect]

document = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.scene {{
  position: relative; width: 100%; height: 560px; overflow: hidden;
  border-radius: 18px; background: {bg}; color: {text_color};
  font-family: "{safe_font}", sans-serif;
}}
.particle-layer {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
.particle {{ position:absolute; top:-45px; opacity:.82; user-select:none; }}
.rain .particle {{ animation-name: rain-fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
.snow .particle {{ animation-name: snow-fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
.hail .particle {{ animation-name: hail-fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
.confetti .particle {{ animation-name: confetti-fall; animation-timing-function:linear; animation-iteration-count:infinite; }}
.wind .particle {{ top:var(--top, 50%); animation-name: wind-blow; animation-timing-function:ease-in-out; animation-iteration-count:infinite; }}
.tornado .particle {{ top:50%; left:50% !important; animation-name:tornado-spin; animation-timing-function:linear; animation-iteration-count:infinite; }}
@keyframes rain-fall {{ to {{ transform:translate(25px, 650px); }} }}
@keyframes snow-fall {{ 0% {{ transform:translate(0,-10px) rotate(0); }} 50% {{ transform:translate(45px,300px) rotate(180deg); }} 100% {{ transform:translate(-15px,650px) rotate(360deg); }} }}
@keyframes hail-fall {{ to {{ transform:translate(35px,650px) rotate(220deg); }} }}
@keyframes confetti-fall {{ 0% {{ transform:translateY(-30px) rotate(0); }} 100% {{ transform:translate(var(--drift),650px) rotate(720deg); }} }}
@keyframes wind-blow {{ 0% {{ transform:translateX(-160px) rotate(0); opacity:0; }} 20% {{ opacity:.9; }} 100% {{ transform:translateX(115vw) rotate(25deg); opacity:0; }} }}
@keyframes tornado-spin {{ 0% {{ transform:rotate(0deg) translateX(20px) scale(.5); opacity:.2; }} 50% {{ opacity:.9; }} 100% {{ transform:rotate(360deg) translateX(170px) scale(1.2); opacity:.2; }} }}
.name-layer {{ position:absolute; z-index:2; inset:0; display:flex; align-items:center; justify-content:center;
  padding:32px; font-size:{font_size}px; font-weight:700; text-align:center; overflow:hidden;
  overflow-wrap:anywhere; text-shadow:0 2px 10px rgba(0,0,0,.12); }}
.center-name {{ max-width:100%; }}
.repeated {{ width:100%; line-height:1.28; }}
.ticker {{ width:100%; overflow:hidden; white-space:nowrap; }}
.ticker-track {{ display:flex; width:max-content; animation:marquee {max(8, 24 - speed * 1.5)}s linear infinite; }}
.ticker-track span {{ flex-shrink:0; padding-right:1rem; }}
@keyframes marquee {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-50%); }} }}
.hint {{ position:absolute; z-index:3; bottom:14px; left:0; right:0; text-align:center; font:12px Arial,sans-serif; opacity:.72; }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker-track {{ animation-duration:30s !important; }}
}}
</style>
</head>
<body>
<div class="scene">
  <div class="particle-layer {effect_class}">{particles}</div>
  <div class="name-layer">{name_content}</div>
  <div class="hint">{html.escape(effect)} effect · looping animation</div>
</div>
</body>
</html>"""

components.html(document, height=580, scrolling=False)
st.caption("Tip: Change the font, size, background, display mode, or effect in the sidebar. Animations run in the preview without repeatedly refreshing the Streamlit page.")
