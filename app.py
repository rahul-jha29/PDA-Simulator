 import streamlit as st
import graphviz
import time

# ─────────────────────────────────────────────────────────────────────────────
# Developed by: Rahul Jha  |  Roll No: 2024UCS1554
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="PDA Simulator — Rahul Jha", layout="wide", page_icon="⚙️")

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS  —  Cyberpunk Terminal Aesthetic
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700;800&family=Orbitron:wght@400;700;900&display=swap');

/* ── Root + Scrollbar ── */
:root {
    --bg:          #050508;
    --bg2:         #0d0d18;
    --bg3:         #12121f;
    --surface:     #1a1a2e;
    --surface2:    #20203a;
    --border:      #2a2a50;
    --border-glow: #00f5ff40;
    --cyan:        #00f5ff;
    --cyan-dim:    #00f5ff60;
    --green:       #39ff14;
    --green-dim:   #39ff1460;
    --red:         #ff2d55;
    --red-dim:     #ff2d5560;
    --amber:       #ffaa00;
    --amber-dim:   #ffaa0060;
    --purple:      #a855f7;
    --text:        #e0e0ff;
    --text-dim:    #6070a0;
    --font-mono:   'JetBrains Mono', monospace;
    --font-display:'Orbitron', monospace;
}
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] > .main > div { padding: 0 1.5rem 2rem; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--cyan-dim); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ── Streamlit UI Overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85em !important;
    caret-color: var(--cyan);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 12px var(--cyan-dim) !important;
    outline: none !important;
}
.stTextInput label, .stTextArea label { display: none !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--cyan) !important;
    color: var(--cyan) !important;
    font-family: var(--font-mono) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-radius: 6px !important;
    text-transform: uppercase !important;
    font-size: 0.8em !important;
    transition: all 0.2s !important;
    position: relative;
    overflow: hidden;
}
.stButton > button:hover:not(:disabled) {
    background: var(--cyan) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 20px var(--cyan-dim) !important;
}
.stButton > button:disabled {
    border-color: var(--border) !important;
    color: var(--text-dim) !important;
    opacity: 0.5 !important;
}
.stButton > button[kind="primary"] {
    border-color: var(--amber) !important;
    color: var(--amber) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--amber) !important;
    color: var(--bg) !important;
    box-shadow: 0 0 20px var(--amber-dim) !important;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* ── Graphviz ── */
[data-testid="stGraphVizChart"] { background: transparent !important; }
[data-testid="stGraphVizChart"] svg { background: transparent !important; max-width: 100%; }

/* ── Tab overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid var(--border) !important;
    border-bottom: none !important;
    gap: 2px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78em !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-radius: 5px !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--cyan-dim) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 1rem !important;
}

/* ── Metric boxes ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 0.7em !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: var(--cyan) !important; font-family: var(--font-display) !important; font-size: 1.5em !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}
@keyframes flicker {
    0%,100%{ opacity:1 } 92%{ opacity:1 } 93%{ opacity:.6 } 94%{ opacity:1 } 96%{ opacity:.8 } 97%{ opacity:1 }
}
@keyframes glitch-1 {
    0%,100%{ clip-path: inset(0 0 95% 0); transform: translate(-2px,0); }
    20%     { clip-path: inset(30% 0 50% 0); transform: translate(2px,0); }
    40%     { clip-path: inset(70% 0 10% 0); transform: translate(-2px,0); }
    60%     { clip-path: inset(10% 0 80% 0); transform: translate(2px,0); }
    80%     { clip-path: inset(60% 0 20% 0); transform: translate(-1px,0); }
}
@keyframes glitch-2 {
    0%,100%{ clip-path: inset(90% 0 0% 0); transform: translate(2px,0); }
    20%     { clip-path: inset(10% 0 70% 0); transform: translate(-2px,0); }
    60%     { clip-path: inset(50% 0 30% 0); transform: translate(1px,0); }
}
@keyframes pulse-border {
    0%,100% { box-shadow: 0 0 15px #00f5ff30, inset 0 0 15px #00f5ff05; }
    50%      { box-shadow: 0 0 35px #00f5ff60, inset 0 0 25px #00f5ff10; }
}
.hdr-wrap {
    position: relative;
    background: linear-gradient(135deg, #050508 0%, #0a0a18 50%, #050510 100%);
    border: 1px solid #00f5ff30;
    border-radius: 12px;
    padding: 28px 40px;
    margin-bottom: 24px;
    overflow: hidden;
    animation: pulse-border 4s ease-in-out infinite;
}
.hdr-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, #00f5ff04 2px, #00f5ff04 4px);
    pointer-events: none;
}
.hdr-grid {
    position: absolute;
    inset: 0;
    background-image: linear-gradient(#00f5ff08 1px,transparent 1px),linear-gradient(90deg,#00f5ff08 1px,transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}
.hdr-scan {
    position: absolute;
    left: 0; right: 0;
    height: 60px;
    background: linear-gradient(transparent, #00f5ff08, transparent);
    animation: scanline 5s linear infinite;
    pointer-events: none;
}
.hdr-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2em;
    font-weight: 900;
    color: #00f5ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    position: relative;
    animation: flicker 8s infinite;
    text-shadow: 0 0 20px #00f5ff80, 0 0 40px #00f5ff30;
    margin: 0;
}
.hdr-title::before {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    color: #ff2d55;
    animation: glitch-1 6s infinite;
    opacity: 0.7;
}
.hdr-title::after {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    color: #39ff14;
    animation: glitch-2 6s infinite 0.3s;
    opacity: 0.5;
}
.hdr-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    color: #6070a0;
    letter-spacing: 2px;
    margin-top: 8px;
    text-transform: uppercase;
}
.hdr-sub span { color: #ffaa00; }
.hdr-badge {
    display: inline-block;
    background: #00f5ff15;
    border: 1px solid #00f5ff40;
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 0.75em;
    color: #00f5ff;
    margin-right: 8px;
    letter-spacing: 1px;
}
.hdr-right {
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
}
.hdr-author { color: #a855f7; font-size: 0.75em; letter-spacing: 2px; text-transform: uppercase; }
.hdr-roll { color: #6070a0; font-size: 0.7em; margin-top: 4px; }
</style>
<div class="hdr-wrap">
    <div class="hdr-grid"></div>
    <div class="hdr-scan"></div>
    <p class="hdr-title" data-text="PDA SIMULATOR">PDA SIMULATOR</p>
    <p class="hdr-sub">
        <span class="hdr-badge">v2.0</span>
        <span class="hdr-badge">Context-Free Languages</span>
        pushdown automata &nbsp;·&nbsp; interactive execution engine
    </p>
    <div class="hdr-right">
        <div class="hdr-author">Rahul Jha</div>
        <div class="hdr-roll">2024UCS1554</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        'current_state': "q0",
        'stack': ["Z"],
        'remaining_input': "aabb",
        'status': "Awaiting initialisation...",
        'game_over': True,
        'trace': [],          # list of dicts: step, state, input, stack_top, rule, new_state, new_stack
        'step_count': 0,
        'start_state_val': "q0",
        'accept_state_val': "q2",
        'input_val': "aabb",
        'start_stack_val': "Z",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════════════════════
#  CORE LOGIC
# ══════════════════════════════════════════════════════════════════════════════
def parse_rules(text):
    rules = []
    for line in text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('->')
        if len(parts) == 2:
            left  = [s.strip() for s in parts[0].split(',')]
            right = [s.strip() for s in parts[1].split(',')]
            if len(left) == 3 and len(right) == 2:
                rules.append({
                    'state': left[0], 'input': left[1], 'pop': left[2],
                    'nextState': right[0], 'push': right[1]
                })
    return rules

def find_matching_rule(rules, state, curr_in, top_stack):
    # Pass 1 — consuming transitions
    consuming = next(
        (r for r in rules
         if r['state'] == state
         and r['input'] == curr_in
         and (r['pop'] == top_stack or r['pop'] == 'e')),
        None
    )
    if consuming:
        return consuming
    # Pass 2 — epsilon transitions
    return next(
        (r for r in rules
         if r['state'] == state
         and r['input'] == 'e'
         and (r['pop'] == top_stack or r['pop'] == 'e')),
        None
    )

def apply_rule(matched):
    """Apply a matched rule and update session state. Returns status string."""
    st.session_state.current_state = matched['nextState']
    if matched['input'] != 'e':
        st.session_state.remaining_input = st.session_state.remaining_input[1:]
    if matched['pop'] != 'e' and st.session_state.stack:
        st.session_state.stack.pop()
    if matched['push'] != 'e':
        for ch in reversed(matched['push']):
            st.session_state.stack.append(ch)

    d_in   = 'ε' if matched['input'] == 'e' else matched['input']
    d_pop  = 'ε' if matched['pop']   == 'e' else matched['pop']
    d_push = 'ε' if matched['push']  == 'e' else matched['push']
    return (matched['state'], d_in, d_pop, matched['nextState'], d_push)

def batch_test(rules, start_state, start_stack, accept_state, test_str):
    """Run a full simulation and return (accepted:bool, steps:int)."""
    state  = start_state
    stack  = [start_stack]
    inp    = test_str
    steps  = 0
    MAX    = 500
    while steps < MAX:
        curr_in   = inp[0] if inp else 'e'
        top_stack = stack[-1] if stack else 'e'
        matched   = find_matching_rule(rules, state, curr_in, top_stack)
        if not matched:
            return False, steps
        state = matched['nextState']
        if matched['input'] != 'e':
            inp = inp[1:]
        if matched['pop'] != 'e' and stack:
            stack.pop()
        if matched['push'] != 'e':
            for ch in reversed(matched['push']):
                stack.append(ch)
        steps += 1
        if not inp and state == accept_state:
            return True, steps
    return False, steps

# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1.1, 1.9])

# ─────────────────────────────────────────────────────────────────
#  LEFT — Configuration
# ─────────────────────────────────────────────────────────────────
with left:
    st.markdown("""
    <style>
    .panel-hdr {
        font-family: 'Orbitron', monospace;
        font-size: 0.75em;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6070a0;
        border-bottom: 1px solid #2a2a50;
        padding-bottom: 8px;
        margin-bottom: 14px;
        margin-top: 0;
    }
    .panel-hdr span { color: #00f5ff; }
    .field-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7em;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ffaa00;
        margin-bottom: 4px;
        display: block;
    }
    .panel-box {
        background: #0d0d18;
        border: 1px solid #2a2a50;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="panel-hdr"><span>01</span> — Configuration</p>', unsafe_allow_html=True)

    # Transitions
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<span class="field-lbl">⬡ Transition Rules</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.68em; color:#6070a0; margin-bottom:8px; font-family:'JetBrains Mono',monospace; line-height:1.6;">
    Format: <span style="color:#00f5ff">state, input, pop → nextState, push</span><br>
    Use <span style="color:#ffaa00">e</span> for epsilon (ε)
    </div>
    """, unsafe_allow_html=True)
    default_rules = "q0, a, Z -> q0, aZ\nq0, a, a -> q0, aa\nq0, b, a -> q1, e\nq1, b, a -> q1, e\nq1, e, Z -> q2, Z"
    rules_text = st.text_area("Transitions", default_rules, height=145, label_visibility="collapsed", key="rules_text_area")
    st.markdown('</div>', unsafe_allow_html=True)
    current_rules = parse_rules(rules_text)

    # Params grid
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<span class="field-lbl">⬡ Parameters</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<span class="field-lbl" style="font-size:0.65em;">Start State</span>', unsafe_allow_html=True)
        start_state = st.text_input("ss", "q0", label_visibility="collapsed", key="s_state")
        st.markdown('<span class="field-lbl" style="font-size:0.65em;">Stack Init</span>', unsafe_allow_html=True)
        start_stack = st.text_input("sk", "Z", label_visibility="collapsed", key="s_stack")
    with c2:
        st.markdown('<span class="field-lbl" style="font-size:0.65em;">Accept State</span>', unsafe_allow_html=True)
        accept_state = st.text_input("as", "q2", label_visibility="collapsed", key="a_state")
        st.markdown('<span class="field-lbl" style="font-size:0.65em;">Input String</span>', unsafe_allow_html=True)
        input_string = st.text_input("is", "aabb", label_visibility="collapsed", key="i_str")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⟳  Load & Reset", type="primary", use_container_width=True):
        st.session_state.current_state   = start_state
        st.session_state.stack           = [start_stack]
        st.session_state.remaining_input = input_string
        st.session_state.trace           = []
        st.session_state.step_count      = 0
        if not input_string and start_state == accept_state:
            st.session_state.status    = "ACCEPTED — empty input at accept state"
            st.session_state.game_over = True
        else:
            st.session_state.status    = "READY — press STEP FORWARD to begin"
            st.session_state.game_over = False

    st.markdown("<br>", unsafe_allow_html=True)
    # ── Transition Table ──
    st.markdown('<p class="panel-hdr" style="margin-top:4px;"><span>02</span> — Transition Table</p>', unsafe_allow_html=True)
    if current_rules:
        rows = ""
        for i, r in enumerate(current_rules):
            d_in   = 'ε' if r['input'] == 'e' else r['input']
            d_pop  = 'ε' if r['pop']   == 'e' else r['pop']
            d_push = 'ε' if r['push']  == 'e' else r['push']
            bg = "#12121f" if i % 2 == 0 else "#0d0d18"
            rows += f"""<tr style="background:{bg};">
  <td style="color:#a855f7;padding:8px 10px;font-weight:700;">{r['state']}</td>
  <td style="color:#00f5ff;padding:8px 10px;">{d_in}</td>
  <td style="color:#ffaa00;padding:8px 10px;">{d_pop}</td>
  <td style="color:#a855f7;padding:8px 10px;font-weight:700;">{r['nextState']}</td>
  <td style="color:#39ff14;padding:8px 10px;">{d_push}</td>
</tr>"""
        tbl = f"""
<style>
.tt {{ width:100%; border-collapse:collapse; border-radius:8px; overflow:hidden; font-family:'JetBrains Mono',monospace; font-size:0.78em; border:1px solid #2a2a50; }}
.tt thead tr {{ background:linear-gradient(135deg,#0f0f20,#1a0a30); }}
.tt th {{ padding:9px 10px; text-align:left; color:#6070a0; letter-spacing:1.5px; text-transform:uppercase; font-size:0.85em; font-weight:700; border-bottom:1px solid #2a2a50; }}
.tt tbody tr:hover {{ background:#00f5ff08 !important; }}
</style>
<table class="tt"><thead><tr>
  <th>State</th><th>In</th><th>Pop</th><th>Next</th><th>Push</th>
</tr></thead><tbody>{rows}</tbody></table>"""
        st.markdown(tbl, unsafe_allow_html=True)

    # ── Batch Test ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="panel-hdr"><span>03</span> — Batch Test</p>', unsafe_allow_html=True)
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<span class="field-lbl">Test Strings (one per line)</span>', unsafe_allow_html=True)
    batch_input = st.text_area("Batch", "aabb\nab\naaabbb\nba\naabb\naabbcc\nε", height=110, label_visibility="collapsed", key="batch_area")
    if st.button("⚡  Run Batch Test", use_container_width=True):
        lines = [l.strip() for l in batch_input.strip().split('\n') if l.strip()]
        results_html = ""
        for line in lines:
            test = "" if line in ("ε", "e", "eps") else line
            accepted, steps = batch_test(current_rules, start_state, start_stack, accept_state, test)
            disp = "ε" if test == "" else test
            icon  = "✓" if accepted else "✗"
            clr   = "#39ff14" if accepted else "#ff2d55"
            badge = "ACCEPT" if accepted else "REJECT"
            results_html += f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:7px 12px;margin-bottom:4px;border-radius:5px;
                background:{'#39ff1410' if accepted else '#ff2d5510'};
                border:1px solid {'#39ff1430' if accepted else '#ff2d5530'};">
              <span style="color:{clr};font-weight:700;font-size:1.1em;">{icon}</span>
              <code style="color:#e0e0ff;flex:1;margin:0 10px;font-size:0.82em;">{disp}</code>
              <span style="color:{clr};font-size:0.7em;letter-spacing:1px;font-weight:700;">{badge}</span>
              <span style="color:#6070a0;font-size:0.68em;margin-left:8px;">{steps} steps</span>
            </div>"""
        st.markdown(f'<div style="margin-top:6px;">{results_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
#  RIGHT — Simulation Engine
# ─────────────────────────────────────────────────────────────────
with right:
    st.markdown('<p class="panel-hdr"><span>04</span> — Simulation Engine</p>', unsafe_allow_html=True)

    # ── Metrics Row ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current State",  st.session_state.current_state)
    m2.metric("Steps Taken",    st.session_state.step_count)
    m3.metric("Stack Depth",    len(st.session_state.stack))
    remaining_disp = st.session_state.remaining_input if st.session_state.remaining_input else "ε"
    m4.metric("Remaining",      remaining_disp[:8] + ("…" if len(remaining_disp) > 8 else ""))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Status Bar ──
    s = st.session_state.status
    if "ACCEPTED" in s.upper():
        sc, sb, si = "#39ff14", "#39ff1415", "#39ff1450"
        icon = "✓"
    elif "REJECTED" in s.upper() or "No valid" in s:
        sc, sb, si = "#ff2d55", "#ff2d5515", "#ff2d5550"
        icon = "✗"
    elif "READY" in s.upper():
        sc, sb, si = "#00f5ff", "#00f5ff10", "#00f5ff40"
        icon = "◈"
    else:
        sc, sb, si = "#ffaa00", "#ffaa0010", "#ffaa0040"
        icon = "▷"

    st.markdown(f"""
    <div style="background:{sb};border:1px solid {si};border-radius:8px;
                padding:12px 20px;margin-bottom:16px;display:flex;align-items:center;gap:12px;">
      <span style="font-size:1.4em;color:{sc};">{icon}</span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:0.82em;
                   color:{sc};font-weight:700;letter-spacing:0.5px;">{s}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls ──
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        step_btn = st.button("▶  Step Forward", disabled=st.session_state.game_over, use_container_width=True)
    with b2:
        auto_btn = st.button("⚡  Auto Run", disabled=st.session_state.game_over, use_container_width=True)
    with b3:
        clear_trace_btn = st.button("⌫  Clear Trace", use_container_width=True)

    if clear_trace_btn:
        st.session_state.trace = []
        st.rerun()

    # ── Step Logic ──
    def do_step():
        curr_in   = st.session_state.remaining_input[0] if st.session_state.remaining_input else 'e'
        top_stack = st.session_state.stack[-1] if st.session_state.stack else 'e'
        matched   = find_matching_rule(current_rules, st.session_state.current_state, curr_in, top_stack)

        if matched:
            prev_state = st.session_state.current_state
            prev_stack = list(st.session_state.stack)
            tup = apply_rule(matched)
            st.session_state.step_count += 1
            st.session_state.trace.append({
                'step':      st.session_state.step_count,
                'from':      tup[0],
                'input':     tup[1],
                'pop':       tup[2],
                'to':        tup[3],
                'push':      tup[4],
                'rem_after': st.session_state.remaining_input if st.session_state.remaining_input else 'ε',
                'stack_str': ''.join(reversed(st.session_state.stack)) if st.session_state.stack else 'empty',
            })
            st.session_state.status = f"APPLIED  {tup[0]}, {tup[1]}, {tup[2]}  →  {tup[3]}, {tup[4]}"
            if not st.session_state.remaining_input and st.session_state.current_state == accept_state:
                st.session_state.status    = "✓  STRING ACCEPTED — reached accept state"
                st.session_state.game_over = True
                return False  # stop
            return True  # keep going
        else:
            st.session_state.status    = "✗  STRING REJECTED — no valid transitions"
            st.session_state.game_over = True
            return False

    if step_btn:
        do_step()
        st.rerun()

    if auto_btn:
        for _ in range(500):
            if not do_step():
                break
        st.rerun()

    # ── Graph + Stack columns ──
    g_col, s_col = st.columns([1.7, 1])

    with g_col:
        st.markdown('<span class="field-lbl" style="font-size:0.65em;display:block;margin-bottom:8px;">State Machine</span>', unsafe_allow_html=True)
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR', bgcolor='transparent', size="5,3.5",
                 fontname="JetBrains Mono", fontcolor="#6070a0")
        dot.attr('node', fontname="JetBrains Mono", fontsize="11", penwidth="2")
        dot.attr('edge', fontname="JetBrains Mono", fontsize="9", fontcolor="#6070a0", color="#2a2a50")

        all_states = set(
            [r['state'] for r in current_rules] +
            [r['nextState'] for r in current_rules] +
            [start_state, accept_state]
        )
        for state in all_states:
            is_current = (state == st.session_state.current_state)
            is_accept  = (state == accept_state)
            if is_current:
                dot.node(state, state, shape='doublecircle' if is_accept else 'circle',
                         style='filled', fillcolor='#ffaa00', fontcolor='#0a0a0f',
                         color='#ffaa00', penwidth='3')
            elif is_accept:
                dot.node(state, state, shape='doublecircle',
                         style='filled', fillcolor='#39ff1430',
                         fontcolor='#39ff14', color='#39ff14')
            else:
                dot.node(state, state, shape='circle',
                         style='filled', fillcolor='#12121f',
                         fontcolor='#a0a0d0', color='#3a3a60')

        for r in current_rules:
            d_in   = 'ε' if r['input'] == 'e' else r['input']
            d_pop  = 'ε' if r['pop']   == 'e' else r['pop']
            d_push = 'ε' if r['push']  == 'e' else r['push']
            lbl = f"{d_in},{d_pop}/{d_push}"
            dot.edge(r['state'], r['nextState'], label=lbl)

        st.graphviz_chart(dot, use_container_width=True)

    with s_col:
        st.markdown('<span class="field-lbl" style="font-size:0.65em;display:block;margin-bottom:8px;">Stack Memory</span>', unsafe_allow_html=True)
        if st.session_state.stack:
            items = ""
            for i, item in enumerate(reversed(st.session_state.stack)):
                is_top = (i == 0)
                bg     = "#ffaa0090" if is_top else "#1a1a2e"
                clr    = "#0a0a0f"   if is_top else "#c0c0e0"
                bdr    = "#ffaa00"   if is_top else "#2a2a50"
                tag    = " TOP" if is_top else ""
                items += f"""<div style="background:{bg};border:1px solid {bdr};border-radius:6px;
                    padding:9px 14px;margin-bottom:4px;display:flex;justify-content:space-between;
                    align-items:center;font-family:'JetBrains Mono',monospace;font-weight:700;
                    color:{clr};font-size:0.9em;transition:all 0.3s;">
                  <span>{item}</span>
                  <span style="font-size:0.6em;opacity:0.6;letter-spacing:1px;">{tag}</span>
                </div>"""
            depth_bar = min(len(st.session_state.stack) * 10, 100)
            st.markdown(f"""
            <div style="background:#0d0d18;border:1px solid #2a2a50;border-radius:10px;padding:14px;">
              <div style="margin-bottom:10px;font-family:'JetBrains Mono',monospace;font-size:0.68em;
                          color:#6070a0;display:flex;justify-content:space-between;">
                <span>LIFO STACK</span>
                <span style="color:#ffaa00;">DEPTH: {len(st.session_state.stack)}</span>
              </div>
              <div style="height:3px;background:#1a1a2e;border-radius:2px;margin-bottom:12px;">
                <div style="height:100%;width:{depth_bar}%;background:linear-gradient(90deg,#ffaa00,#ff6600);border-radius:2px;transition:width 0.4s;"></div>
              </div>
              {items}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#0d0d18;border:1px solid #2a2a50;border-radius:10px;padding:20px;text-align:center;">
              <div style="color:#6070a0;font-size:0.8em;font-family:'JetBrains Mono',monospace;">STACK EMPTY</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Execution Trace Log ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="panel-hdr" style="margin-top:0;"><span>05</span> — Execution Trace Log</p>', unsafe_allow_html=True)
    if st.session_state.trace:
        header = """<style>
.trace-tbl { width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;
             font-size:0.76em;border:1px solid #2a2a50;border-radius:8px;overflow:hidden; }
.trace-tbl th { background:#0f0f20;color:#6070a0;padding:8px 12px;text-align:left;
                letter-spacing:1.5px;text-transform:uppercase;font-size:0.8em;
                border-bottom:1px solid #2a2a50;font-weight:700; }
.trace-tbl td { padding:7px 12px;border-bottom:1px solid #1a1a30; }
.trace-tbl tr:last-child td { border-bottom:none; }
.trace-tbl tr:hover td { background:#00f5ff06; }
.trace-tbl tr:nth-child(even) td { background:#0a0a15; }
</style>
<table class="trace-tbl">
<thead><tr>
  <th>#</th><th>From</th><th>Input</th><th>Pop</th>
  <th>→ To</th><th>Push</th><th>Remaining</th><th>Stack</th>
</tr></thead><tbody>"""
        rows = ""
        for t in st.session_state.trace:
            rows += f"""<tr>
  <td style="color:#6070a0;">{t['step']}</td>
  <td style="color:#a855f7;font-weight:700;">{t['from']}</td>
  <td style="color:#00f5ff;">{t['input']}</td>
  <td style="color:#ffaa00;">{t['pop']}</td>
  <td style="color:#a855f7;font-weight:700;">{t['to']}</td>
  <td style="color:#39ff14;">{t['push']}</td>
  <td style="color:#6070a0;">{t['rem_after']}</td>
  <td style="color:#c0c0e0;">{t['stack_str']}</td>
</tr>"""
        st.markdown(header + rows + "</tbody></table>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#0d0d18;border:1px dashed #2a2a50;border-radius:8px;
                    padding:20px;text-align:center;font-family:'JetBrains Mono',monospace;
                    color:#6070a0;font-size:0.8em;letter-spacing:2px;">
          NO TRACE DATA — LOAD A STRING AND STEP FORWARD
        </div>""", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div style="text-align:center;padding:20px 0 10px;font-family:'JetBrains Mono',monospace;
            font-size:0.7em;color:#2a2a50;letter-spacing:2px;text-transform:uppercase;
            border-top:1px solid #1a1a2e;margin-top:24px;">
  PDA Simulator &nbsp;·&nbsp; Rahul Jha (2024UCS1554) &nbsp;·&nbsp; TOC Project
</div>
""", unsafe_allow_html=True)
