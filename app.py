import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="🎾 CourtCast — Tennis Match Predictor", page_icon="🎾", layout="wide")

# ===== Load model =====
import os
import tempfile
import streamlit as st
import joblib
import requests
import pandas as pd

# ------------------------
# MODEL DOWNLOAD + LOAD
# ------------------------
def download_gdrive(file_id, output_path):
    url = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(url, params={"id": file_id}, stream=True)
    response.raise_for_status()
    token = None
    for k,v in response.cookies.items():
        if k.startswith("download_warning"):
            token = v
            break
    if token:
        response = session.get(url, params={"id": file_id, "confirm": token}, stream=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

@st.cache_resource
def load_model():
    file_id = "1HwtJ6nJwMTs2MmAFPsNPpCZ6oXe6cF0T"
    model_name = "final_model.pkl"

    temp_dir = tempfile.gettempdir()
    model_path = os.path.join(temp_dir, model_name)

    if not os.path.exists(model_path):
        with st.spinner("⬇️ Downloading model..."):
            download_gdrive(file_id, model_path)

    model = joblib.load(model_path)
    return model

model = load_model()
# ===== Funky Tennis Theme (court + ball + neon) =====
COURT = "#1DB954"        # court green
COURT_DARK = "#0E7A3A"
SKY = "#6EE7FF"          # funky background tint
NEON = "#F7FF00"         # tennis ball
INK = "#0B1220"
WHITE = "#FFFFFF"
LINE = "rgba(255,255,255,0.65)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800;900&display=swap');
html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif; }}

/* Funky background */
.stApp {{
  background:
    radial-gradient(circle at 12% 18%, rgba(110,231,255,0.35) 0%, rgba(0,0,0,0) 36%),
    radial-gradient(circle at 90% 18%, rgba(247,255,0,0.22) 0%, rgba(0,0,0,0) 34%),
    linear-gradient(135deg, #0B1220 0%, #12263A 55%, #0B1220 100%);
  background-attachment: fixed;
}}

.block-container {{ max-width: 1200px; padding-top: 1.2rem; }}
[data-testid="stHeader"] {{ background: transparent; }}

/* Text */
html, body, p, li, span, div, label, small {{ color: rgba(255,255,255,0.88) !important; }}
h1, h2, h3, h4 {{ color: {NEON} !important; font-weight: 900 !important; letter-spacing: 0.5px; }}

/* Hero court card */
.hero {{
  position: relative;
  border-radius: 26px;
  padding: 26px 26px;
  background:
    linear-gradient(135deg, rgba(29,185,84,0.22) 0%, rgba(255,255,255,0.06) 45%, rgba(110,231,255,0.10) 100%);
  border: 1px solid rgba(247,255,0,0.28);
  box-shadow: 0 20px 55px rgba(0,0,0,0.45);
  overflow: hidden;
  margin-bottom: 18px;
}}

/* Tennis court lines */
.court-lines {{
  position: absolute; inset: 14px;
  border-radius: 18px;
  border: 2px solid {LINE};
  pointer-events: none;
}}
.court-mid {{
  position:absolute; left:50%; top:14px; bottom:14px;
  width:2px; background:{LINE}; transform: translateX(-1px);
}}
.court-box1 {{
  position:absolute; left:14px; right:14px; top:38%;
  height:24%;
  border-top:2px solid {LINE};
  border-bottom:2px solid {LINE};
}}
.court-box2 {{
  position:absolute; left:22%; right:22%; top:14px; bottom:14px;
  border-left:2px solid {LINE};
  border-right:2px solid {LINE};
}}

/* Ball */
@keyframes bounce {{
  0%, 100% {{ transform: translate(0,0) rotate(0deg); }}
  50% {{ transform: translate(-8px, -10px) rotate(-6deg); }}
}}
.ball {{
  position: absolute;
  right: 22px; top: 22px;
  width: 90px; height: 90px;
  border-radius: 999px;
  background: radial-gradient(circle at 35% 35%, #FFFFA8 0%, {NEON} 45%, #C9CF00 100%);
  box-shadow: 0 0 35px rgba(247,255,0,0.35);
  opacity: 0.95;
  animation: bounce 2.2s ease-in-out infinite;
}}
.ball:before, .ball:after {{
  content: "";
  position: absolute;
  inset: 10px;
  border-radius: 999px;
  border: 2px solid rgba(255,255,255,0.72);
  clip-path: polygon(0 46%, 100% 46%, 100% 54%, 0 54%);
}}
.ball:after {{
  inset: 14px;
  border-color: rgba(0,0,0,0.22);
  clip-path: polygon(0 46%, 100% 46%, 100% 54%, 0 54%);
}}

/* Badges */
.badges {{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 10px; }}
.badge {{
  padding: 7px 12px; border-radius: 999px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.18);
  color: rgba(255,255,255,0.88) !important;
  font-weight: 800;
  font-size: 0.88rem;
}}

/* Panels */
.panel {{
  border-radius: 22px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.14);
  box-shadow: 0 18px 45px rgba(0,0,0,0.35);
  padding: 18px 18px;
  margin-bottom: 16px;
}}
.panel-title {{
  font-weight: 900;
  color: {NEON} !important;
  font-size: 1.05rem;
  letter-spacing: 0.6px;
  margin-bottom: 6px;
}}
.panel-sub {{
  color: rgba(255,255,255,0.78) !important;
  margin-bottom: 12px;
}}

/* Inputs */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input {{
  background: rgba(255,255,255,0.10) !important;
  border: 1px solid rgba(255,255,255,0.20) !important;
  border-radius: 14px !important;
  color: rgba(255,255,255,0.92) !important;
  font-weight: 700 !important;
}}
.stSelectbox span {{ color: rgba(255,255,255,0.92) !important; font-weight: 800 !important; }}

/* Button */
.stButton > button {{
  width: 100%;
  border: none;
  border-radius: 16px;
  padding: 1.0rem 1.2rem;
  font-weight: 950;
  letter-spacing: 1px;
  color: {INK} !important;
  background: linear-gradient(135deg, {NEON} 0%, #A3FF12 55%, {SKY} 100%);
  box-shadow: 0 18px 45px rgba(247,255,0,0.22);
}}
.stButton > button:hover {{ transform: translateY(-2px); }}

/* "Probability bar" style */
.prob-wrap {{
  border-radius: 18px;
  padding: 16px;
  background: rgba(29,185,84,0.10);
  border: 1px solid rgba(247,255,0,0.25);
}}
</style>
""", unsafe_allow_html=True)

# ===== HERO =====
st.markdown(f"""
<div class="hero">
  <div class="court-lines"></div>
  <div class="court-mid"></div>
  <div class="court-box1"></div>
  <div class="court-box2"></div>
  <div class="ball"></div>

  <div style="font-size:2.1rem; font-weight:950; color:{NEON};">🎾 CourtCast</div>
  <div style="margin-top:6px; color:rgba(255,255,255,0.82); font-size:1.02rem;">
    Random Forest match win predictor — built for quick “who’s favored?” insights.
  </div>
  <div class="badges">
    <div class="badge">🌱 Surface-aware</div>
    <div class="badge">🏆 Round context</div>
    <div class="badge">📊 Rank + Points gaps</div>
    <div class="badge">✨  Court UI by Mayank Goyal</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ===== INPUTS =====
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">🎛️ Match Setup</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">Fill details like a real match card.</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    surface = st.selectbox("🟩 Surface", ["Hard", "Clay", "Grass", "Carpet"], index=0)
    best_of = st.selectbox("🎯 Best of", [3, 5], index=0)
with c2:
    round_ = st.selectbox("🏟️ Round", ["Q1", "Q2", "Q3", "R128", "R64", "R32", "R16", "QF", "SF", "F"], index=5)
with c3:
    st.caption("Tip: Smaller rank = stronger player.")

st.markdown("</div>", unsafe_allow_html=True)

# Player cards
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">🧑‍🎾 Players</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">Player A is the “higher-ranked” candidate in your formulation.</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    st.markdown("#### 🅰️ Player A")
    winner_rank = st.number_input("🏅 Rank (A)", min_value=1, value=20, step=1)
    winner_pts = st.number_input("📌 Rank points (A)", min_value=0, value=1500, step=50)
with p2:
    st.markdown("#### 🅱️ Player B")
    loser_rank = st.number_input("🏅 Rank (B)", min_value=1, value=35, step=1)
    loser_pts = st.number_input("📌 Rank points (B)", min_value=0, value=1200, step=50)

st.markdown("</div>", unsafe_allow_html=True)

# ===== PREDICT =====
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">🚀 Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">Click predict to see win probability + a tennis-style momentum bar.</div>', unsafe_allow_html=True)

predict = st.button("🎾 Predict Winner Probability")

if predict:
    X_new = pd.DataFrame([{
        "surface": surface,
        "round": round_,
        "best_of": best_of,
        "winner_rank": winner_rank,
        "loser_rank": loser_rank,
        "rank_gap": abs(winner_rank - loser_rank),
        "winner_rank_points": winner_pts,
        "loser_rank_points": loser_pts,
        "points_gap": abs(winner_pts - loser_pts),
    }])

    proba = float(model.predict_proba(X_new)[0][1])

    fav = "Player A" if proba >= 0.5 else "Player B"
    confidence = abs(proba - 0.5) * 2  # 0..1

    st.markdown('<div class="prob-wrap">', unsafe_allow_html=True)

    left, mid, right = st.columns([1, 1, 1])
    left.metric("🎯 Favored", fav)
    mid.metric("📈 Win prob (A)", f"{proba:.3f}")
    right.metric("🔥 Confidence", f"{confidence*100:.1f}%")

    # Tennis "momentum" bar using Streamlit progress [web:254]
    st.progress(proba, text="A’s win momentum (0 → B favored, 1 → A favored)")  # [web:254]

    # Fun callout
    if proba >= 0.7:
        st.success("✅ Strong edge for Player A — looks like a straight-sets vibe.")
    elif proba >= 0.55:
        st.info("🟨 Slight edge for Player A — could be a tight match.")
    elif proba <= 0.3:
        st.error("🟥 Player A is the underdog — upset needed.")
    else:
        st.warning("🟧 Very close — expect a match with drama 😄")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===== EXTRA “WOW” FEATURE: QUICK EXPLANATION =====
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">✨ What influenced it?</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">A quick human-friendly summary from your inputs (not SHAP, but helpful).</div>', unsafe_allow_html=True)

rank_gap = abs(winner_rank - loser_rank)
pts_gap = abs(winner_pts - loser_pts)

st.write(f"• Rank gap: **{rank_gap}** (bigger gap usually favors the better-ranked player).")
st.write(f"• Points gap: **{pts_gap}** (bigger gap suggests stronger recent performance).")
st.write(f"• Surface/round/best-of can shift upset probability depending on the training data.")

st.markdown("</div>", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<hr style="margin-top:2rem; border-color: rgba(255,255,255,0.16);">
<div style="text-align:center; padding: 1rem 0; color: rgba(255,255,255,0.72);">
  © 2025 <span style="font-weight:950; color:#F7FF00;">CourtCast</span> · Built by <b>Mayank Goyal</b><br>
  <a href="https://www.linkedin.com/in/mayank-goyal-4b8756363" target="_blank" style="color:#6EE7FF; text-decoration:none; font-weight:900; margin-right:18px;">LinkedIn</a>
  <a href="https://github.com/mayank-goyal09" target="_blank" style="color:#6EE7FF; text-decoration:none; font-weight:900;">GitHub</a>
</div>
""", unsafe_allow_html=True)


