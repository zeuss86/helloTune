"""
styles.py - all custom CSS and static markup for the interface.

Palette (black, grey, cherry red, white)
  Black     #0F0F10   sidebar, masthead, primary text
  Grey      #5E5E63 / #D4D4D8 / #EDEDEE   secondary text, hairlines, page
  Cherry    #C4122F   the single action colour: buttons, focus, active tab
  White     #FFFFFF   cards and inputs

Every widget colour is set explicitly below, so the look is the same whether
the browser or Streamlit is in light or dark mode.

Type: Newsreader (serif) for headings, Public Sans for everything else.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;500;600&display=swap');

:root {
  --black: #0F0F10;
  --grey-600: #5E5E63;
  --grey-400: #B4B4BA;
  --grey-300: #D4D4D8;
  --grey-200: #E4E4E7;
  --grey-100: #F4F4F5;
  --page: #EDEDEE;
  --cherry: #C4122F;
  --cherry-dark: #9E0F26;
}

/* ---------- Page ---------- */
html, body, .stApp { font-family: 'Public Sans', system-ui, sans-serif; }
.stApp { background: var(--page); color: var(--black); }
.block-container { max-width: 1120px; padding-top: 1.5rem; padding-bottom: 4rem; }
[data-testid="stHeader"] { background: var(--page) !important; }
[data-testid="stHeader"] *, [data-testid="stToolbar"] * { color: var(--black) !important; }

.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
  font-family: 'Newsreader', Georgia, serif !important;
  color: var(--black);
  font-weight: 600;
  letter-spacing: -0.01em;
}
.stApp p, .stApp li { color: var(--black); }

/* ---------- Masthead ---------- */
.masthead {
  background: var(--black);
  border-bottom: 4px solid var(--cherry);
  border-radius: 10px;
  padding: 2.2rem 2.4rem;
  margin-bottom: 1.6rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}
.stApp .masthead h1 { color: #FFFFFF !important; font-size: 2.6rem; line-height: 1.1; margin: 0 0 0.7rem; padding: 0; }
.stApp .masthead p { color: var(--grey-400) !important; font-size: 1.05rem; line-height: 1.55; max-width: 44ch; margin: 0; }

/* Audio-progress motif: played bars white, the playhead cherry, the rest grey */
.wave { display: flex; align-items: center; gap: 5px; height: 84px; flex-shrink: 0; }
.wave i { display: block; width: 5px; border-radius: 2px; background: #4A4A4F; }
.wave i.done { background: #F4F4F5; }
.wave i.now { background: var(--cherry); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--black); border-right: none; }
[data-testid="stSidebar"] * { color: var(--grey-200) !important; }
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; font-size: 1.2rem; margin-top: 0.6rem; }
.status { display: flex; align-items: center; margin: 0.35rem 0; font-size: 0.92rem; }
.status span { display: inline-block; width: 0.6rem; height: 0.6rem; border-radius: 50%; margin-right: 0.65rem; flex-shrink: 0; }
.status.on span { background: #FFFFFF; }
.status.off span { border: 2px solid var(--cherry); }

/* ---------- Cards (st.container(key="card_...")) ---------- */
[class*="st-key-card"] {
  background: #FFFFFF;
  border: 1px solid var(--grey-300);
  border-radius: 10px;
  padding: 1.5rem 1.6rem 1.7rem;
  box-shadow: 0 1px 2px rgba(15, 15, 16, 0.06), 0 12px 28px rgba(15, 15, 16, 0.08);
}
[class*="st-key-card"] h3 { margin: 0 0 0.9rem; padding-bottom: 0.7rem; font-size: 1.5rem; border-bottom: 1px solid var(--grey-200); }

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 0.25rem; border-bottom: 1px solid var(--grey-300); margin-bottom: 1.2rem; }
.stTabs [data-baseweb="tab"] { padding: 0.7rem 1.3rem; background: transparent; }
.stTabs [data-baseweb="tab"] p { color: var(--grey-600) !important; font-weight: 600; font-size: 1rem; }
.stTabs [aria-selected="true"] p { color: var(--black) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--cherry) !important; height: 3px; }
.stTabs [data-baseweb="tab-border"] { background: transparent !important; }

/* ---------- Labels ---------- */
.stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] * { color: var(--black) !important; font-weight: 600; font-size: 0.9rem; }
.stApp [data-testid="stCheckbox"] *, .stApp [data-testid="stRadio"] label * { color: var(--black) !important; }

/* ---------- Inputs ---------- */
[data-baseweb="select"] > div { background: #FFFFFF !important; border: 1px solid var(--grey-300) !important; border-radius: 6px !important; }
[data-baseweb="select"] *, [data-baseweb="select"] input { color: var(--black) !important; -webkit-text-fill-color: var(--black) !important; }
[data-baseweb="select"] svg { fill: var(--black) !important; }
[data-baseweb="select"] > div:focus-within { border-color: var(--cherry) !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] [data-baseweb="menu"] { background: #FFFFFF !important; }
div[data-baseweb="popover"] li { background: #FFFFFF !important; color: var(--black) !important; }
div[data-baseweb="popover"] li:hover, div[data-baseweb="popover"] li[aria-selected="true"] { background: var(--grey-100) !important; }

[data-baseweb="textarea"], [data-baseweb="textarea"] > div, [data-baseweb="base-input"] { background: #FFFFFF !important; border-radius: 6px !important; }
[data-baseweb="textarea"] { border: 1px solid var(--grey-300) !important; }
[data-baseweb="textarea"]:focus-within { border-color: var(--cherry) !important; }
.stApp textarea { background: #FFFFFF !important; color: var(--black) !important; -webkit-text-fill-color: var(--black) !important; font-size: 0.92rem; line-height: 1.6; }

/* ---------- File upload ---------- */
[data-testid="stFileUploaderDropzone"] { background: #FFFFFF; border: 2px dashed var(--grey-300); border-radius: 8px; padding: 1.3rem; transition: border-color 0.15s; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--cherry); }
[data-testid="stFileUploaderDropzoneInstructions"] * { color: var(--grey-600) !important; }
[data-testid="stFileUploaderDropzone"] svg { fill: var(--grey-600); }
[data-testid="stFileUploaderFile"] { background: var(--grey-100); border-radius: 6px; padding: 0.4rem 0.7rem; }
[data-testid="stFileUploaderFile"] * { color: var(--black) !important; }

/* ---------- Buttons ---------- */
.stApp .stButton button, .stApp [data-testid="stDownloadButton"] button {
  width: 100%;
  border-radius: 6px;
  font-weight: 600;
  padding: 0.65rem 1.2rem;
  transition: background 0.15s, border-color 0.15s;
}
.stApp button[kind="primary"], .stApp button[data-testid="stBaseButton-primary"] { background: var(--cherry) !important; border: 1px solid var(--cherry) !important; }
.stApp button[kind="primary"] *, .stApp button[data-testid="stBaseButton-primary"] * { color: #FFFFFF !important; }
.stApp button[kind="primary"]:hover, .stApp button[data-testid="stBaseButton-primary"]:hover { background: var(--cherry-dark) !important; border-color: var(--cherry-dark) !important; }
.stApp button[kind="secondary"], .stApp button[data-testid="stBaseButton-secondary"] { background: #FFFFFF !important; border: 1px solid var(--black) !important; }
.stApp button[kind="secondary"] *, .stApp button[data-testid="stBaseButton-secondary"] * { color: var(--black) !important; }
.stApp button[kind="secondary"]:hover, .stApp button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--cherry) !important; }
.stApp button[kind="secondary"]:hover *, .stApp button[data-testid="stBaseButton-secondary"]:hover * { color: var(--cherry) !important; }
.stApp button:disabled { opacity: 0.4; }
.stApp button:focus-visible { outline: 3px solid var(--cherry); outline-offset: 2px; }

/* ---------- Metrics, expander, alerts, progress ---------- */
[data-testid="stMetric"] { background: var(--grey-100); border: 1px solid var(--grey-200); border-radius: 6px; padding: 0.7rem 0.9rem; }
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { color: var(--grey-600) !important; font-size: 0.8rem; }
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * { color: var(--black) !important; font-family: 'Newsreader', Georgia, serif; font-size: 1.55rem; }

[data-testid="stExpander"] details { background: #FFFFFF; border: 1px solid var(--grey-300); border-radius: 8px; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * { color: var(--black) !important; font-weight: 600; }

[data-testid="stAlert"] { background: #FFFFFF !important; border: 1px solid var(--grey-300); border-left: 4px solid var(--cherry); border-radius: 6px; }
[data-testid="stAlert"] * { color: var(--black) !important; }

[data-testid="stProgress"] p, [data-testid="stSpinner"] * { color: var(--black) !important; }
audio { width: 100%; }

/* ---------- Custom blocks ---------- */
.note-ok { background: var(--grey-100); border-left: 4px solid var(--black); border-radius: 4px; padding: 0.7rem 1rem; margin-bottom: 0.9rem; font-weight: 600; color: var(--black); }
.empty-state { background: var(--grey-100); border-radius: 8px; padding: 1.5rem 1.6rem; }
.empty-state .lead { font-weight: 600; margin: 0 0 0.7rem; color: var(--black); }
.empty-state ol { margin: 0; padding-left: 1.3rem; }
.empty-state li { color: var(--grey-600); line-height: 1.8; }
.empty-state li::marker { color: var(--cherry); font-weight: 600; }

@media (max-width: 760px) {
  .wave { display: none; }
  .stApp .masthead h1 { font-size: 2rem; }
  .masthead { padding: 1.6rem 1.4rem; }
}
</style>
"""

_BARS = [14, 24, 38, 26, 48, 34, 60, 42, 28, 54, 70, 46, 32, 58, 40, 22, 36, 18, 30, 12]
_PLAYHEAD = 10


def _wave() -> str:
    parts = []
    for index, height in enumerate(_BARS):
        state = "done" if index < _PLAYHEAD else ("now" if index == _PLAYHEAD else "")
        parts.append(f'<i class="{state}" style="height:{height}px"></i>')
    return "".join(parts)


MASTHEAD = (
    '<div class="masthead"><div class="masthead-text">'
    "<h1>Audio and Document Converter</h1>"
    "<p>Turn a PDF into an MP3 you can listen to, or an MP3 recording into text you can edit.</p>"
    f'</div><div class="wave" aria-hidden="true">{_wave()}</div></div>'
)

EMPTY_PDF = (
    '<div class="empty-state"><p class="lead">Your audio will appear here.</p><ol>'
    "<li>Upload a PDF on the left.</li><li>Choose the voice language.</li>"
    "<li>Select Generate MP3.</li></ol></div>"
)

EMPTY_MP3 = (
    '<div class="empty-state"><p class="lead">Your transcript will appear here.</p><ol>'
    "<li>Upload an MP3 on the left.</li><li>Choose the spoken language.</li>"
    "<li>Select Transcribe audio.</li></ol></div>"
)

READY_NOTE = '<div class="note-ok">{}</div>'
