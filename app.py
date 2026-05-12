import streamlit as st
import hashlib
import base64
from datetime import datetime
import anthropic

# ══════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Karim Maher · Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DEFAULT_PW_HASH = hashlib.sha256("karim2024".encode()).hexdigest()

# ══════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "admin_logged_in": False,
        "chat_messages":   [],
        "chat_open":       False,
        "_page":           "portfolio",
        "lang":            "ar",   # ar or en
        "profile": {
            "name_en":   "Karim Maher",
            "title_ar":  "محلل بيانات",
            "title_en":  "Data Analyst",
            "subtitle":  "Streamlit Developer · Power BI · Python",
            "location":  "Alexandria, Egypt",
            "phone":     "01063872784",
            "email":     "",
            "linkedin":  "",
            "github":    "",
            "edu_ar":    "دبلومة تحليل البيانات — أكاديمية Tech Trek",
            "edu_en":    "Data Analysis Diploma — Tech Trek Academy",
            "bio_ar":    "محلل بيانات شغوف بتحويل الأرقام إلى قرارات. أبني نماذج تحليلية وتطبيقات Streamlit تفاعلية تجعل البيانات في متناول الجميع.",
            "bio_en":    "Passionate data analyst who turns numbers into decisions. I build analytical models and interactive Streamlit apps that make data accessible to everyone.",
            "skills":    "Python, SQL, Power BI, Streamlit, Pandas, Scikit-learn, Excel, Matplotlib, Seaborn",
            "photo_b64": "",
            "pw_hash":   DEFAULT_PW_HASH,
        },
        "projects": [],
        "certs": [
            {"icon":"🏕️","name_ar":"Data Analyst Track",    "name_en":"Data Analyst Track",      "issuer":"DataCamp",               "color":"#f97316"},
            {"icon":"🎓","name_ar":"دبلومة تحليل البيانات", "name_en":"Data Analysis Diploma",   "issuer":"Tech Trek Academy",       "color":"#00d4ff"},
            {"icon":"🏛️","name_ar":"شهادة تحليل البيانات",  "name_en":"Data Analysis Certificate","issuer":"Egyptian Engineers Syndicate","color":"#a855f7"},
        ],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════
def hp(pw):     return hashlib.sha256(pw.encode()).hexdigest()
def P(k):       return st.session_state.profile.get(k, "")
def ar():       return st.session_state.lang == "ar"
def t(a, e):    return a if ar() else e   # translate helper

TYPE_META = {
    "dashboard": ("📊", "Dashboard",        "Dashboard",        "#00d4ff"),
    "streamlit": ("🚀", "Streamlit App",    "Streamlit App",    "#ec4899"),
    "notebook":  ("📓", "Jupyter Notebook", "Jupyter Notebook", "#f97316"),
    "pdf":       ("📄", "تقرير PDF",        "PDF Report",       "#a855f7"),
    "video":     ("🎬", "فيديو",            "Video",            "#22c55e"),
    "link":      ("🔗", "رابط خارجي",       "External Link",    "#64748b"),
}

def file_to_b64(file) -> str:
    return base64.b64encode(file.read()).decode()

def b64_img_src(b64: str, mime: str) -> str:
    return f"data:{mime};base64,{b64}"

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=Cairo:wght@400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root{
  --ink:#07070f;--ink2:#0f0f1a;--ink3:#171724;--ink4:#21212f;
  --frost:#eeeeff;--frost2:#9898b8;--frost3:#484868;
  --cyan:#00e5ff;--pink:#f72585;--purple:#7b2fff;--green:#06d6a0;--orange:#f97316;
  --border:rgba(255,255,255,0.07);--r:14px;
}
html,body,[class*="css"],.stApp{
  font-family:'DM Sans','Cairo',sans-serif !important;
  background:var(--ink) !important;color:var(--frost) !important;
}
#MainMenu,footer,header{display:none !important;}
[data-testid="collapsedControl"]{display:none !important;}
section[data-testid="stSidebar"]{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--ink);}
::-webkit-scrollbar-thumb{background:rgba(0,229,255,0.2);border-radius:3px;}

/* BG */
.stApp::after{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);
  background-size:70px 70px;
  mask-image:radial-gradient(ellipse at 50% 0%,black 20%,transparent 80%);
}

/* HERO */
.km-hero{
  min-height:100vh;position:relative;z-index:1;
  display:flex;align-items:center;padding:6rem 3rem 5rem;overflow:hidden;
}
.km-hero-glow{
  position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse 55% 60% at 78% 50%,rgba(0,229,255,.07) 0%,transparent 70%),
    radial-gradient(ellipse 40% 50% at 10% 70%,rgba(123,47,255,.08) 0%,transparent 70%),
    radial-gradient(ellipse 30% 40% at 50% 5%,rgba(247,37,133,.05) 0%,transparent 60%);
}
.km-hero-content{position:relative;z-index:1;max-width:580px;}
.km-badge{
  display:inline-flex;align-items:center;gap:.6rem;
  font-family:'JetBrains Mono',monospace;font-size:.67rem;font-weight:600;
  color:var(--cyan);letter-spacing:1.5px;text-transform:uppercase;
  background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.18);
  border-radius:100px;padding:.35rem 1rem;margin-bottom:1.5rem;
}
.ldot{width:7px;height:7px;background:var(--green);border-radius:50%;box-shadow:0 0 8px var(--green);animation:lpulse 2s ease-in-out infinite;}
@keyframes lpulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}
.km-hname{
  font-family:'Syne',sans-serif;font-weight:800;
  font-size:clamp(3rem,6.5vw,5.5rem);letter-spacing:-3px;line-height:.95;
  background:linear-gradient(140deg,#fff 30%,#8888cc 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.8rem;
}
.km-hrole{font-family:'Syne',sans-serif;font-size:clamp(1.1rem,2vw,1.5rem);font-weight:700;color:var(--cyan);margin-bottom:1.5rem;letter-spacing:-.3px;}
.km-hbio{font-size:.95rem;color:var(--frost2);line-height:1.85;font-weight:300;margin-bottom:2.5rem;}
.km-pills{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:2rem;}
.km-pill{font-family:'JetBrains Mono',monospace;font-size:.67rem;font-weight:500;padding:.32rem .85rem;border:1px solid var(--border);border-radius:100px;color:var(--frost3);background:rgba(255,255,255,.03);}

/* AVATAR */
.km-av-area{position:absolute;right:4rem;top:50%;transform:translateY(-50%);z-index:1;}
.km-av-ring{width:220px;height:220px;border-radius:50%;padding:3px;background:conic-gradient(var(--cyan) 0%,var(--purple) 40%,var(--pink) 70%,var(--cyan) 100%);animation:spinring 8s linear infinite;}
@keyframes spinring{to{transform:rotate(360deg);}}
.km-av-inner{width:100%;height:100%;border-radius:50%;background:var(--ink2);display:flex;align-items:center;justify-content:center;font-size:6rem;overflow:hidden;}
.km-av-inner img{width:100%;height:100%;object-fit:cover;border-radius:50%;}

/* SECTIONS */
.km-sec{padding:4rem 3rem;max-width:1200px;margin:0 auto;position:relative;z-index:1;}
.km-eyebrow{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:600;color:var(--frost3);letter-spacing:3px;text-transform:uppercase;display:flex;align-items:center;gap:1rem;margin-bottom:.8rem;}
.km-eyebrow::after{content:'';flex:1;height:1px;background:var(--border);}
.km-sec-title{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(2rem,4vw,3rem);letter-spacing:-1.5px;line-height:1.05;margin-bottom:2rem;}
.km-sec-title .hl{color:var(--cyan);}

/* CARDS */
.km-card{background:var(--ink2);border:1px solid var(--border);border-radius:var(--r);padding:1.6rem;transition:border-color .3s,transform .3s,box-shadow .3s;}
.km-card:hover{border-color:rgba(0,229,255,.22);transform:translateY(-5px);box-shadow:0 20px 50px rgba(0,0,0,.4),0 0 30px rgba(0,229,255,.07);}
.km-card-icon{font-size:2rem;margin-bottom:.8rem;}
.km-card-title{font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;color:var(--cyan);margin-bottom:.4rem;}
.km-card-body{font-size:.82rem;color:var(--frost3);line-height:1.75;font-weight:300;}
.km-about-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;}
.km-skill{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:.67rem;font-weight:500;padding:.28rem .7rem;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:6px;color:var(--frost2);margin:.18rem;transition:all .2s;}
.km-skill:hover{border-color:var(--cyan);color:var(--cyan);}

/* CERTS */
.km-cert{display:flex;align-items:center;gap:1.2rem;background:var(--ink2);border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:.8rem;transition:all .25s;}
.km-cert:hover{border-color:rgba(0,229,255,.18);transform:translateX(5px);}
.km-cert-icon{font-size:1.4rem;width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.km-cert-name{font-family:'Syne',sans-serif;font-size:.9rem;font-weight:700;margin-bottom:.15rem;}
.km-cert-issuer{font-size:.72rem;color:var(--frost3);}
.km-cert-chip{font-family:'JetBrains Mono',monospace;font-size:.6rem;font-weight:600;padding:.2rem .6rem;border-radius:6px;white-space:nowrap;flex-shrink:0;}

/* METRICS */
.km-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;}
.km-metric{background:var(--ink2);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;text-align:center;transition:all .3s;position:relative;overflow:hidden;}
.km-metric::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);transform:scaleX(0);transition:transform .4s;}
.km-metric:hover::after{transform:scaleX(1);}
.km-metric:hover{transform:translateY(-3px);}
.km-metric-val{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:var(--cyan);line-height:1;}
.km-metric-label{font-size:.72rem;color:var(--frost3);margin-top:.4rem;font-weight:300;}

/* PROJ */
.km-proj-card{background:var(--ink2);border:1px solid var(--border);border-radius:18px;overflow:hidden;transition:all .35s cubic-bezier(.34,1.4,.64,1);}
.km-proj-card:hover{border-color:rgba(0,229,255,.22);transform:translateY(-8px);box-shadow:0 30px 60px rgba(0,0,0,.5),0 0 30px rgba(0,229,255,.07);}
.km-proj-thumb{height:170px;background:var(--ink3);display:flex;align-items:center;justify-content:center;font-size:4rem;position:relative;overflow:hidden;}
.km-proj-thumb img{width:100%;height:100%;object-fit:cover;}
.km-proj-thumb video{width:100%;height:100%;object-fit:cover;}
.km-thumb-ov{position:absolute;inset:0;background:linear-gradient(to top,rgba(7,7,15,.7) 0%,transparent 50%);}
.km-proj-chip{position:absolute;bottom:10px;right:10px;font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:600;padding:.22rem .6rem;border-radius:6px;backdrop-filter:blur(8px);}
.km-proj-body{padding:1.2rem 1.4rem 1rem;}
.km-proj-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;margin-bottom:.4rem;letter-spacing:-.3px;}
.km-proj-desc{font-size:.78rem;color:var(--frost3);line-height:1.65;margin-bottom:.8rem;font-weight:300;}
.km-proj-tools{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.8rem;}
.km-proj-tool{font-family:'JetBrains Mono',monospace;font-size:.58rem;padding:.14rem .42rem;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:5px;color:var(--frost3);}

/* CONTACT */
.km-contact-item{background:var(--ink2);border:1px solid var(--border);border-radius:12px;padding:1.2rem;text-align:center;transition:all .25s;}
.km-contact-item:hover{border-color:rgba(0,229,255,.2);transform:translateY(-3px);}
.km-contact-icon{font-size:1.8rem;margin-bottom:.5rem;}
.km-contact-label{font-size:.78rem;font-weight:600;color:var(--frost2);margin-bottom:.5rem;}

/* CHAT FAB */
div[data-testid="stButton"]>button[title="chatfab"]{
  position:fixed !important;bottom:2rem !important;left:2rem !important;
  z-index:1000 !important;width:56px !important;height:56px !important;
  border-radius:50% !important;padding:0 !important;font-size:1.3rem !important;
  background:linear-gradient(135deg,var(--cyan),var(--purple)) !important;
  border:none !important;color:var(--ink) !important;
  box-shadow:0 8px 30px rgba(0,229,255,.3) !important;
}
.km-chatwin{position:fixed;bottom:5.5rem;left:2rem;z-index:900;width:360px;background:var(--ink2);border:1px solid rgba(0,229,255,.15);border-radius:20px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6);}
.km-chat-hdr{padding:.9rem 1.1rem;border-bottom:1px solid var(--border);background:rgba(0,229,255,.04);display:flex;align-items:center;gap:.7rem;}
.km-chat-av{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--cyan),var(--purple));display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0;}
.km-chat-nm{font-family:'Syne',sans-serif;font-size:.82rem;font-weight:700;}
.km-chat-st{font-size:.62rem;color:var(--green);}
.km-chat-body{display:flex;flex-direction:column;gap:.7rem;padding:.8rem;max-height:240px;overflow-y:auto;}
.km-chat-body::-webkit-scrollbar{width:3px;}
.km-chat-body::-webkit-scrollbar-thumb{background:rgba(255,255,255,.08);border-radius:2px;}
.km-msg-u{align-self:flex-end;max-width:80%;}
.km-msg-b{align-self:flex-start;max-width:85%;}
.km-bub-u{background:linear-gradient(135deg,var(--cyan),var(--purple));color:var(--ink);border-radius:14px 14px 4px 14px;padding:.6rem .9rem;font-size:.8rem;font-weight:500;}
.km-bub-b{background:var(--ink3);border:1px solid var(--border);color:var(--frost);border-radius:14px 14px 14px 4px;padding:.6rem .9rem;font-size:.8rem;line-height:1.6;font-weight:300;}
.km-suggs{padding:.4rem .8rem;display:flex;gap:.4rem;flex-wrap:wrap;}
.km-sugg{font-size:.67rem;font-weight:500;padding:.28rem .65rem;background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.15);border-radius:100px;color:var(--cyan);white-space:nowrap;}

/* FOOTER */
.km-footer{border-top:1px solid var(--border);padding:2.5rem 3rem;text-align:center;}
.km-footer-logo{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:var(--cyan);margin-bottom:.3rem;}
.km-footer-copy{font-size:.73rem;color:var(--frost3);font-weight:300;}
.km-div{height:1px;background:var(--border);margin:0 3rem;}

/* ADMIN */
.km-admin-top{margin-bottom:2rem;padding:1.2rem 1.5rem;background:rgba(247,37,133,.05);border:1px solid rgba(247,37,133,.15);border-radius:12px;}
.km-admin-title{font-family:'Syne',sans-serif;font-size:1rem;font-weight:800;color:var(--pink);}
.km-admin-sub{font-size:.72rem;color:var(--frost3);margin-top:.2rem;}
.km-login{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem;}
.km-login-box{background:var(--ink2);border:1px solid rgba(247,37,133,.2);border-radius:24px;padding:3rem;width:100%;max-width:400px;text-align:center;box-shadow:0 40px 100px rgba(0,0,0,.5);}

/* FILE UPLOAD */
[data-testid="stFileUploader"]{background:var(--ink3) !important;border:1px dashed rgba(0,229,255,.25) !important;border-radius:10px !important;}

/* ST OVERRIDES */
.stButton>button{font-family:'DM Sans',sans-serif !important;font-weight:600 !important;border-radius:10px !important;transition:all .25s !important;}
.stButton>button[kind="primary"]{background:var(--cyan) !important;color:var(--ink) !important;border:none !important;}
.stButton>button[kind="primary"]:hover{transform:translateY(-2px) !important;box-shadow:0 8px 25px rgba(0,229,255,.3) !important;}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,.05) !important;border:1px solid var(--border) !important;color:var(--frost) !important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div{background:var(--ink3) !important;border-color:var(--border) !important;color:var(--frost) !important;font-family:'DM Sans',sans-serif !important;border-radius:10px !important;}
.stTabs [data-baseweb="tab"]{font-family:'Syne',sans-serif !important;font-weight:700 !important;color:var(--frost3) !important;}
.stTabs [data-baseweb="tab"][aria-selected="true"]{color:var(--cyan) !important;}
.stTabs [data-baseweb="tab-list"]{background:var(--ink2) !important;border-radius:12px !important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--cyan) !important;}
a[data-testid="stLinkButton"]>button{background:var(--cyan) !important;color:var(--ink) !important;border:none !important;font-weight:700 !important;border-radius:9px !important;font-size:.8rem !important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CHATBOT
# ══════════════════════════════════════════════════════════
def build_system_prompt() -> str:
    p     = st.session_state.profile
    projs = st.session_state.projects
    certs = st.session_state.certs
    lang  = "عربي" if ar() else "English"

    proj_lines = "\n".join([
        f"- {TYPE_META.get(pr.get('type','link'),('📁','','',''))[0]} {pr.get('name','')} "
        f"({TYPE_META.get(pr.get('type','link'),('','','Project',''))[2]}): "
        f"{pr.get('desc','')} | Tools: {pr.get('tools','')} | Link: {pr.get('link','—')}"
        for pr in projs
    ]) or "No projects added yet"

    cert_lines = "\n".join([f"- {c['icon']} {c['name_en']} — {c['issuer']}" for c in certs])

    return f"""You are a smart assistant for {p.get('name_en','Karim Maher')}'s portfolio.
Reply in {'Arabic' if ar() else 'English'} since the portfolio is in {lang} mode.
Be friendly, concise, and professional.

━━ Profile ━━
Name: {p.get('name_en','')}
Title: {p.get('title_en','')} / {p.get('title_ar','')}
Location: {p.get('location','')} | Phone: {p.get('phone','')}
Email: {p.get('email','N/A')} | LinkedIn: {p.get('linkedin','N/A')}
GitHub: {p.get('github','N/A')}
Education: {p.get('edu_en','')}
Bio: {p.get('bio_en','')}
Skills: {p.get('skills','')}

━━ Certificates ━━
{cert_lines}

━━ Projects ({len(projs)}) ━━
{proj_lines}

Rule: Never invent info. If not found say so honestly."""

def ask_claude(msg: str) -> str:
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY","")
        if not key:
            # Smart fallback replies
            return smart_fallback(msg)
        client  = anthropic.Anthropic(api_key=key)
        history = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_messages[-10:]]
        history.append({"role":"user","content":msg})
        resp = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=400,
            system=build_system_prompt(), messages=history
        )
        return resp.content[0].text
    except Exception as e:
        return smart_fallback(msg)

def smart_fallback(msg: str) -> str:
    """Intelligent rule-based responses from profile data"""
    p     = st.session_state.profile
    projs = st.session_state.projects
    m     = msg.lower()

    if any(w in m for w in ["مهار","skill","tools","تقني","tech"]):
        skills = p.get("skills","Python, SQL, Power BI")
        return t(f"مهاراتي التقنية تشمل: **{skills}**", f"My technical skills include: **{skills}**")

    if any(w in m for w in ["مشروع","project","شغل","work","portfolio"]):
        if not projs:
            return t("لم تُضف مشاريع بعد 📭","No projects added yet 📭")
        proj_list = "\n".join([f"• {p.get('name','')} ({TYPE_META.get(p.get('type','link'),('','','Project',''))[2]})" for p in projs[:5]])
        return t(f"إليك مشاريعي:\n{proj_list}", f"Here are my projects:\n{proj_list}")

    if any(w in m for w in ["تواصل","contact","email","phone","تليفون","linkedin","github"]):
        phone = p.get('phone','')
        email = p.get('email','')
        li    = p.get('linkedin','')
        gh    = p.get('github','')
        info  = f"📞 {phone}" if phone else ""
        if email: info += f"\n✉️ {email}"
        if li:    info += f"\n💼 LinkedIn: {li}"
        if gh:    info += f"\n🐙 GitHub: {gh}"
        return t(f"معلومات التواصل:\n{info}", f"Contact info:\n{info}")

    if any(w in m for w in ["شهاد","certif","دبلوم","diploma"]):
        certs = st.session_state.certs
        c_list = "\n".join([f"• {c['icon']} {c['name_en']} — {c['issuer']}" for c in certs])
        return t(f"شهاداتي المهنية:\n{c_list}", f"My certifications:\n{c_list}")

    if any(w in m for w in ["تعليم","edu","دراس","study","جامع","univ","أكاديم","academy"]):
        edu = p.get('edu_ar','') if ar() else p.get('edu_en','')
        return t(f"تعليمي: {edu}", f"My education: {edu}")

    if any(w in m for w in ["مين","من","who","name","اسم"]):
        name = p.get('name_en','Karim Maher')
        bio  = p.get('bio_ar','') if ar() else p.get('bio_en','')
        return t(f"أنا {name}، {bio}", f"I'm {name}. {bio}")

    if any(w in m for w in ["streamlit","تطبيق","app","بني","build"]):
        st_apps = [p for p in projs if p.get("type") == "streamlit"]
        if st_apps:
            apps = "\n".join([f"• {a.get('name','')} — {a.get('link','')}" for a in st_apps])
            return t(f"تطبيقاتي على Streamlit:\n{apps}", f"My Streamlit apps:\n{apps}")
        return t("أبني تطبيقات Streamlit تفاعلية! لم تُضف تطبيقات بعد.","I build Streamlit apps! None added yet.")

    if any(w in m for w in ["خبر","experience","سن","year","كام"]):
        return t("لدي خبرة في تحليل البيانات، بناء لوحات المعلومات، وتطوير تطبيقات Streamlit.",
                 "I have experience in data analysis, dashboard building, and Streamlit app development.")

    # Default
    name = p.get('name_en','Karim Maher')
    return t(
        f"👋 أهلاً! أنا المساعد الذكي لبورتفوليو {name}. اسألني عن المهارات، المشاريع، الشهادات، أو التواصل!",
        f"👋 Hi! I'm the smart assistant for {name}'s portfolio. Ask me about skills, projects, certificates, or how to get in touch!"
    )

# ══════════════════════════════════════════════════════════
#  NAV — Streamlit Native (no HTML fixed nav)
# ══════════════════════════════════════════════════════════
def render_nav():
    name = P("name_en").split()[0] if P("name_en") else "KM"
    lang_label = "🌐 English" if ar() else "🌐 عربي"

    col_logo, col_links, col_actions = st.columns([2, 4, 2])

    with col_logo:
        st.markdown(f"""
        <div style="padding:.8rem 0;font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#eeeeff">
          {name} <span style="color:#00e5ff">◈</span>
        </div>""", unsafe_allow_html=True)

    with col_links:
        st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;gap:2rem;padding:.8rem 0">
          <span style="font-size:.82rem;font-weight:500;color:#484868">{t("البروفايل","Profile")}</span>
          <span style="font-size:.82rem;font-weight:500;color:#484868">{t("الشهادات","Certificates")}</span>
          <span style="font-size:.82rem;font-weight:500;color:#484868">{t("المشاريع","Projects")}</span>
          <span style="font-size:.82rem;font-weight:500;color:#484868">{t("تواصل","Contact")}</span>
        </div>""", unsafe_allow_html=True)

    with col_actions:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button(lang_label, key="lang_btn", use_container_width=True):
                st.session_state.lang = "en" if ar() else "ar"
                st.rerun()
        with btn_col2:
            page = st.session_state._page
            if page == "portfolio":
                if st.button(t("⚙️ تحكم","⚙️ Admin"), key="nav_btn", use_container_width=True):
                    st.session_state._page = "admin"
                    st.rerun()
            else:
                if st.button(t("← رجوع","← Back"), key="nav_btn", use_container_width=True):
                    st.session_state._page = "portfolio"
                    st.session_state.admin_logged_in = False
                    st.rerun()

    st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════
def render_hero():
    photo_b64 = P("photo_b64")
    if photo_b64:
        avatar = f'<div class="km-av-inner"><img src="data:image/jpeg;base64,{photo_b64}" alt="{P("name_en")}"></div>'
    else:
        avatar = '<div class="km-av-inner">👤</div>'

    role = P("title_ar") if ar() else P("title_en")
    bio  = P("bio_ar")   if ar() else P("bio_en")
    badge_text = "متاح للعمل · Available for Work" if ar() else "Available for Work · متاح للعمل"

    st.markdown(f"""
    <div class="km-hero">
      <div class="km-hero-glow"></div>
      <div class="km-hero-content">
        <div class="km-badge"><span class="ldot"></span> {badge_text}</div>
        <div class="km-hname">{P("name_en")}</div>
        <div class="km-hrole">{role}</div>
        <div class="km-hbio">{bio}</div>
        <div class="km-pills">
          <span class="km-pill">📍 {P("location")}</span>
          <span class="km-pill">📞 {P("phone")}</span>
          <span class="km-pill">🐍 Python · SQL · Power BI</span>
          <span class="km-pill">🚀 Streamlit</span>
        </div>
      </div>
      <div class="km-av-area"><div class="km-av-ring">{avatar}</div></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  METRICS
# ══════════════════════════════════════════════════════════
def render_metrics():
    n  = len(st.session_state.projects)
    ns = len([p for p in st.session_state.projects if p.get("type")=="streamlit"])
    labels = (
        [f"{n}+", "3", f"{ns}", "98%"],
        [t("مشروع","Projects"), t("شهادة","Certs"), "Streamlit Apps", t("رضا العملاء","Client Satisfaction")]
    )
    st.markdown(f"""
    <div class="km-sec" style="padding-top:2rem;padding-bottom:2rem">
      <div class="km-metrics">
        {''.join([f'<div class="km-metric"><div class="km-metric-val">{v}</div><div class="km-metric-label">{l}</div></div>' for v,l in zip(labels[0],labels[1])])}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  ABOUT
# ══════════════════════════════════════════════════════════
def render_about():
    skills_html = "".join([f'<span class="km-skill">{s.strip()}</span>' for s in P("skills").split(",") if s.strip()])
    edu  = P("edu_ar")  if ar() else P("edu_en")
    bio  = P("bio_ar")  if ar() else P("bio_en")
    sec  = t("01 — عن كريم","01 — About")
    titl = t('الخبرة و<span class="hl">المهارات</span>','Experience & <span class="hl">Skills</span>')
    st.markdown(f"""
    <div class="km-sec">
      <div class="km-eyebrow">{sec}</div>
      <div class="km-sec-title">{titl}</div>
      <div class="km-about-grid">
        <div class="km-card"><div class="km-card-icon">🎓</div>
          <div class="km-card-title">{t("التعليم والدبلومة","Education")}</div>
          <div class="km-card-body">{edu}</div></div>
        <div class="km-card"><div class="km-card-icon">💼</div>
          <div class="km-card-title">{t("نبذة مهنية","About Me")}</div>
          <div class="km-card-body">{bio}</div></div>
        <div class="km-card" style="grid-column:1/-1"><div class="km-card-icon">⚙️</div>
          <div class="km-card-title">{t("المهارات التقنية","Technical Skills")}</div>
          <div style="margin-top:.6rem">{skills_html}</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CERTS
# ══════════════════════════════════════════════════════════
def render_certs():
    html = ""
    for c in st.session_state.certs:
        col  = c["color"]
        name = c["name_ar"] if ar() else c["name_en"]
        html += f"""<div class="km-cert">
          <div class="km-cert-icon" style="background:color-mix(in srgb,{col} 12%,transparent)">{c["icon"]}</div>
          <div style="flex:1"><div class="km-cert-name">{name}</div><div class="km-cert-issuer">{c["issuer"]}</div></div>
          <span class="km-cert-chip" style="background:color-mix(in srgb,{col} 12%,transparent);color:{col};border:1px solid color-mix(in srgb,{col} 30%,transparent)">{c["issuer"].split("—")[0].strip()}</span>
        </div>"""
    sec  = t("02 — الشهادات","02 — Certificates")
    titl = t('الشهادات <span class="hl">المهنية</span>','Professional <span class="hl">Certificates</span>')
    st.markdown(f"""
    <div class="km-sec">
      <div class="km-eyebrow">{sec}</div>
      <div class="km-sec-title">{titl}</div>
      {html}
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  PROJECTS
# ══════════════════════════════════════════════════════════
def render_projects():
    projects = st.session_state.projects
    sec  = t("03 — المشاريع","03 — Projects")
    titl = t('معرض <span class="hl">المشاريع</span>','My <span class="hl">Projects</span>')
    st.markdown(f"""
    <div class="km-sec" style="padding-bottom:1rem">
      <div class="km-eyebrow">{sec}</div>
      <div class="km-sec-title">{titl}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 3rem 4rem">', unsafe_allow_html=True)
        if not projects:
            st.info(t("📭 لم تُضف مشاريع بعد — ادخل لوحة التحكم وأضف أول مشروع!",
                      "📭 No projects added yet — go to Admin panel to add your first project!"))
            st.markdown("</div>", unsafe_allow_html=True)
            return

        types_in = list(dict.fromkeys([p.get("type","link") for p in projects]))
        opts     = [t("🗂️ الكل","🗂️ All")] + [
            f"{TYPE_META[tp][0]} {TYPE_META[tp][1] if ar() else TYPE_META[tp][2]}"
            for tp in types_in if tp in TYPE_META
        ]
        sel = st.selectbox("", opts, label_visibility="collapsed", key="proj_filter")
        filtered = projects if sel in [t("🗂️ الكل","🗂️ All")] else [
            p for p in projects
            if f"{TYPE_META.get(p.get('type','link'),('','','',''))[0]} {TYPE_META.get(p.get('type','link'),('','','',''))[1 if ar() else 2]}" == sel
        ]

        cols = st.columns(3)
        for i, proj in enumerate(filtered):
            tp = proj.get("type","link")
            emoji, lbl_ar, lbl_en, color = TYPE_META.get(tp,("📁","مشروع","Project","#aaa"))
            lbl   = lbl_ar if ar() else lbl_en
            link  = proj.get("link","")
            tools = proj.get("tools","")
            tools_html = "".join([f'<span class="km-proj-tool">{t_.strip()}</span>' for t_ in tools.split(",") if t_.strip()])

            # Thumbnail
            file_b64  = proj.get("file_b64","")
            file_mime = proj.get("file_mime","")
            if file_b64 and file_mime and file_mime.startswith("image/"):
                thumb = f'<img src="data:{file_mime};base64,{file_b64}">'
            elif file_b64 and file_mime and file_mime.startswith("video/"):
                thumb = f'<video src="data:{file_mime};base64,{file_b64}" autoplay muted loop></video>'
            elif proj.get("img_url",""):
                thumb = f'<img src="{proj["img_url"]}">'
            else:
                thumb = f'<span style="font-size:3.8rem">{proj.get("emoji","📁")}</span>'

            with cols[i % 3]:
                st.markdown(f"""
                <div class="km-proj-card">
                  <div class="km-proj-thumb">
                    {thumb}
                    <div class="km-thumb-ov"></div>
                    <span class="km-proj-chip" style="background:color-mix(in srgb,{color} 20%,rgba(0,0,0,.6));color:{color};border:1px solid color-mix(in srgb,{color} 35%,transparent)">{emoji} {lbl}</span>
                  </div>
                  <div class="km-proj-body">
                    <div class="km-proj-name">{proj.get("name","")}</div>
                    <div class="km-proj-desc">{proj.get("desc","")}</div>
                    <div class="km-proj-tools">{tools_html}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if link:
                    st.link_button(t("فتح المشروع ↗","Open Project ↗"), url=link, use_container_width=True)
                elif file_b64 and file_mime == "application/pdf":
                    st.download_button(
                        t("تحميل PDF ⬇","Download PDF ⬇"),
                        data=base64.b64decode(file_b64),
                        file_name=proj.get("file_name","file.pdf"),
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"dl_{proj.get('id')}"
                    )
                st.write("")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CONTACT
# ══════════════════════════════════════════════════════════
def render_contact():
    phone    = P("phone")
    email    = P("email")
    linkedin = P("linkedin")
    github   = P("github")
    sec  = t("04 — تواصل","04 — Contact")
    titl = t('تواصل <span class="hl">معي</span>','Get In <span class="hl">Touch</span>')
    st.markdown(f"""
    <div class="km-sec" style="padding-bottom:1rem">
      <div class="km-eyebrow">{sec}</div>
      <div class="km-sec-title" style="text-align:center">{titl}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding:0 3rem 5rem">', unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="km-contact-item"><div class="km-contact-icon">📞</div><div class="km-contact-label">{phone}</div></div>', unsafe_allow_html=True)
            if phone: st.link_button(t("اتصل الآن","Call Now"), url=f"tel:{phone}", use_container_width=True)
        with c2:
            st.markdown(f'<div class="km-contact-item"><div class="km-contact-icon">✉️</div><div class="km-contact-label">{t("البريد الإلكتروني","Email")}</div></div>', unsafe_allow_html=True)
            if email: st.link_button(t("راسلني","Email Me"), url=f"mailto:{email}", use_container_width=True)
            else: st.caption(t("أضف بريدك من لوحة التحكم","Add email in Admin"))
        with c3:
            st.markdown('<div class="km-contact-item"><div class="km-contact-icon">💼</div><div class="km-contact-label">LinkedIn</div></div>', unsafe_allow_html=True)
            if linkedin: st.link_button(t("الملف الشخصي","View Profile"), url=linkedin, use_container_width=True)
            else: st.caption(t("أضف LinkedIn من لوحة التحكم","Add LinkedIn in Admin"))
        with c4:
            st.markdown('<div class="km-contact-item"><div class="km-contact-icon">🐙</div><div class="km-contact-label">GitHub</div></div>', unsafe_allow_html=True)
            if github: st.link_button(t("الكود المصدري","View Code"), url=github, use_container_width=True)
            else: st.caption(t("أضف GitHub من لوحة التحكم","Add GitHub in Admin"))
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  CHATBOT
# ══════════════════════════════════════════════════════════
def render_chatbot():
    fab = "✕" if st.session_state.chat_open else "💬"
    if st.button(fab, key="chatfab", help="chatfab"):
        st.session_state.chat_open = not st.session_state.chat_open
        st.rerun()
    if not st.session_state.chat_open:
        return

    msgs_html = ""
    if not st.session_state.chat_messages:
        msgs_html = f'<div class="km-msg-b"><div class="km-bub-b">👋 {t(f"أهلاً! اسألني عن {P(chr(110)+chr(97)+chr(109)+chr(101)+chr(95)+chr(101)+chr(110))}","Hi! Ask me anything about "+P("name_en"))}</div></div>'
    else:
        for m in st.session_state.chat_messages[-8:]:
            if m["role"]=="user": msgs_html += f'<div class="km-msg-u"><div class="km-bub-u">{m["content"]}</div></div>'
            else:                 msgs_html += f'<div class="km-msg-b"><div class="km-bub-b">{m["content"]}</div></div>'

    suggs = [t("ما مهاراتك؟","What are your skills?"), t("اعرض المشاريع","Show projects"),
             t("كيف أتواصل؟","How to contact?"),      t("ما شهاداتك؟","Your certificates?")]
    sugg_html = "".join([f'<span class="km-sugg">{s}</span>' for s in suggs])

    st.markdown(f"""
    <div class="km-chatwin">
      <div class="km-chat-hdr">
        <div class="km-chat-av">◈</div>
        <div><div class="km-chat-nm">KM Assistant</div><div class="km-chat-st">● {t("متصل الآن","Online now")}</div></div>
      </div>
      <div class="km-chat-body">{msgs_html}</div>
      <div class="km-suggs">{sugg_html}</div>
    </div>
    """, unsafe_allow_html=True)

    placeholder = t("اسألني عن كريم ماهر...","Ask me about Karim Maher...")
    user_msg = st.chat_input(placeholder, key="chat_input")
    if user_msg:
        st.session_state.chat_messages.append({"role":"user","content":user_msg})
        with st.spinner(""):
            reply = ask_claude(user_msg)
        st.session_state.chat_messages.append({"role":"assistant","content":reply})
        st.rerun()

# ══════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════
def render_login():
    st.markdown('<div class="km-login">', unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.5,1])
    with col:
        st.markdown(f"""
        <div class="km-login-box">
          <div style="font-size:3.5rem;margin-bottom:.8rem">🔐</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:.3rem">{t("لوحة التحكم","Admin Panel")}</div>
          <div style="font-size:.8rem;color:var(--frost3);margin-bottom:1.5rem;font-weight:300">{t(f"خاص بـ {P('name_en')} فقط",f"Only for {P('name_en')}")}</div>
        </div>
        """, unsafe_allow_html=True)
        pw = st.text_input("", type="password", placeholder="• • • • • • • •", label_visibility="collapsed")
        if st.button(t("دخول ↗","Login ↗"), use_container_width=True, type="primary"):
            if hp(pw) == P("pw_hash"):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error(t("❌ باسورد غلط!","❌ Wrong password!"))
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  ADMIN
# ══════════════════════════════════════════════════════════
def render_admin():
    p = st.session_state.profile
    st.markdown(f"""
    <div style="padding:1rem 3rem 0">
      <div class="km-admin-top">
        <div class="km-admin-title">◈ {t("لوحة تحكم","Admin Panel")} — {p.get("name_en","")}</div>
        <div class="km-admin-sub">{t("أي تغيير يظهر فوراً · الـ Chatbot يتعلم تلقائياً","Changes appear instantly · Chatbot learns automatically")}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t("🚪 تسجيل الخروج","🚪 Logout"), key="logout_btn"):
        st.session_state.admin_logged_in = False
        st.session_state._page = "portfolio"
        st.rerun()

    with st.container():
        st.markdown('<div style="padding:0 3rem 3rem">', unsafe_allow_html=True)
        tab1, tab2, tab3, tab4 = st.tabs([
            t("👤  البروفايل والصورة","👤  Profile & Photo"),
            t("🗂️  المشاريع","🗂️  Projects"),
            t("🏅  الشهادات","🏅  Certificates"),
            t("🤖  الـ Chatbot","🤖  Chatbot"),
        ])

        # ── TAB 1: PROFILE ──
        with tab1:
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"#### 📷 {t('صورتك الشخصية','Your Photo')}")
                photo_b64 = p.get("photo_b64","")
                if photo_b64:
                    st.image(f"data:image/jpeg;base64,{photo_b64}", width=170)
                else:
                    st.markdown('<div style="width:170px;height:170px;background:#17172a;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:5rem;border:2px dashed rgba(0,229,255,.15)">👤</div>', unsafe_allow_html=True)

                # ✅ Direct file upload for photo
                photo_file = st.file_uploader(
                    t("ارفع صورتك مباشر","Upload your photo"),
                    type=["jpg","jpeg","png","webp"],
                    key="photo_upload"
                )
                if photo_file:
                    new_b64 = file_to_b64(photo_file)
                    st.session_state.profile["photo_b64"] = new_b64
                    st.success(t("✅ تم رفع الصورة!","✅ Photo uploaded!"))
                    st.rerun()
                if photo_b64:
                    if st.button(t("🗑️ حذف الصورة","🗑️ Remove Photo")):
                        st.session_state.profile["photo_b64"] = ""
                        st.rerun()

            with c2:
                st.markdown(f"#### ✏️ {t('بياناتك الشخصية','Your Info')}")
                r1,r2 = st.columns(2)
                with r1:
                    n_name  = st.text_input(t("الاسم (إنجليزي)","Name (English)"), value=p.get("name_en",""))
                    n_loc   = st.text_input(t("الموقع","Location"),                 value=p.get("location",""))
                    n_li    = st.text_input("LinkedIn",                              value=p.get("linkedin",""))
                    n_edu_ar= st.text_input(t("التعليم (عربي)","Education (AR)"),   value=p.get("edu_ar",""))
                with r2:
                    n_tar   = st.text_input(t("المسمى (عربي)","Title (AR)"),        value=p.get("title_ar",""))
                    n_ten   = st.text_input(t("المسمى (إنجليزي)","Title (EN)"),     value=p.get("title_en",""))
                    n_phone = st.text_input(t("رقم الهاتف","Phone"),                value=p.get("phone",""))
                    n_gh    = st.text_input("GitHub",                               value=p.get("github",""))
                n_email = st.text_input(t("البريد الإلكتروني","Email"),             value=p.get("email",""))
                n_sub   = st.text_input(t("العنوان الثانوي","Subtitle"),            value=p.get("subtitle",""))
                n_edu_en= st.text_input(t("التعليم (إنجليزي)","Education (EN)"),   value=p.get("edu_en",""))
                n_bio_ar= st.text_area(t("نبذة (عربي)","Bio (AR)"),                value=p.get("bio_ar",""), height=80)
                n_bio_en= st.text_area(t("نبذة (إنجليزي)","Bio (EN)"),             value=p.get("bio_en",""), height=80)
                n_sk    = st.text_input(t("المهارات (فاصلة)","Skills (comma-sep)"), value=p.get("skills",""))

                st.markdown(f"#### 🔑 {t('تغيير الباسورد','Change Password')}")
                pc1,pc2 = st.columns(2)
                with pc1: n_pw  = st.text_input(t("باسورد جديد","New password"),    type="password", placeholder=t("اتركه فاضي لو مش عايز تغيره","Leave empty to keep current"))
                with pc2: n_pw2 = st.text_input(t("تأكيد الباسورد","Confirm"),      type="password")

                if st.button(t("💾 حفظ كل التغييرات","💾 Save All Changes"), type="primary", use_container_width=True):
                    pw_hash = p.get("pw_hash", DEFAULT_PW_HASH)
                    if n_pw:
                        if n_pw != n_pw2: st.error(t("❌ الباسوردان مختلفان!","❌ Passwords don't match!")); st.stop()
                        if len(n_pw) < 4:  st.error(t("❌ الباسورد قصير جداً!","❌ Password too short!")); st.stop()
                        pw_hash = hp(n_pw)
                    st.session_state.profile.update({
                        "name_en":n_name,"title_ar":n_tar,"title_en":n_ten,"subtitle":n_sub,
                        "location":n_loc,"phone":n_phone,"email":n_email,
                        "linkedin":n_li,"github":n_gh,
                        "edu_ar":n_edu_ar,"edu_en":n_edu_en,
                        "bio_ar":n_bio_ar,"bio_en":n_bio_en,
                        "skills":n_sk,"pw_hash":pw_hash,
                    })
                    st.success(t("✅ تم الحفظ! 🎉","✅ Saved! Changes are live 🎉"))
                    st.rerun()

        # ── TAB 2: PROJECTS ──
        with tab2:
            cf, cl = st.columns([1, 2])
            with cf:
                st.markdown(f"#### ➕ {t('مشروع جديد','New Project')}")
                p_type  = st.selectbox(t("النوع","Type"), list(TYPE_META.keys()),
                                       format_func=lambda x:f"{TYPE_META[x][0]} {TYPE_META[x][1] if ar() else TYPE_META[x][2]}")
                p_name  = st.text_input(t("الاسم *","Name *"), key="pn")
                p_desc  = st.text_area(t("الوصف","Description"), key="pd", height=80)
                p_tools = st.text_input(t("التقنيات (فاصلة)","Tools (comma-sep)"), placeholder="Python, Pandas", key="pt")
                p_link  = st.text_input(t("الرابط الخارجي","External URL"), placeholder="https://...", key="pl")
                p_emoji = st.text_input(t("إيموجي","Emoji"), max_chars=2, key="pe",
                                        placeholder=TYPE_META.get(p_type,("📁","","",""))[0])

                # ✅ Direct file upload for project
                st.markdown(f"**📁 {t('رفع ملف مباشر','Upload File Directly')}**")
                uploaded = st.file_uploader(
                    t("صورة / فيديو / PDF","Image / Video / PDF"),
                    type=["jpg","jpeg","png","gif","webp","mp4","mov","pdf"],
                    key="proj_file"
                )
                if uploaded:
                    st.success(f"✅ {uploaded.name}")

                if st.button(t("✅ إضافة للبورتفوليو","✅ Add to Portfolio"), type="primary", use_container_width=True):
                    if not p_name:
                        st.error(t("❌ أدخل الاسم!","❌ Enter a name!")); st.stop()

                    file_b64  = ""
                    file_mime = ""
                    file_name = ""
                    if uploaded:
                        uploaded.seek(0)
                        file_b64  = file_to_b64(uploaded)
                        file_mime = uploaded.type
                        file_name = uploaded.name

                    st.session_state.projects.insert(0, {
                        "id":       str(int(datetime.now().timestamp())),
                        "type":     p_type,
                        "name":     p_name,
                        "desc":     p_desc,
                        "tools":    p_tools,
                        "link":     p_link,
                        "emoji":    p_emoji or TYPE_META.get(p_type,("📁","","",""))[0],
                        "file_b64": file_b64,
                        "file_mime":file_mime,
                        "file_name":file_name,
                        "img_url":  "",
                        "date":     datetime.now().strftime("%Y-%m-%d"),
                    })
                    st.success(t(f"✅ تم إضافة '{p_name}'!",f"✅ '{p_name}' added!"))
                    st.rerun()

            with cl:
                projs = st.session_state.projects
                st.markdown(f"#### {t('المشاريع','Projects')} — {len(projs)}")
                if not projs:
                    st.info(t("📭 لا توجد مشاريع بعد","📭 No projects yet"))
                for proj in projs:
                    emoji,lbl_ar,lbl_en,_ = TYPE_META.get(proj.get("type","link"),("📁","مشروع","Project",""))
                    lbl = lbl_ar if ar() else lbl_en
                    has_file = bool(proj.get("file_b64",""))
                    ca, cb = st.columns([6,1])
                    with ca:
                        lnk = proj.get("link","")
                        fn  = proj.get("file_name","")
                        st.markdown(f"""
                        <div style="background:var(--ink3);border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;margin-bottom:.5rem">
                          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem">{emoji} {proj.get("name","")}</div>
                          <div style="font-size:.68rem;color:var(--frost3)">{lbl} · {proj.get("date","")} · {proj.get("tools","")}</div>
                          {"<div style='font-size:.67rem;color:var(--cyan);margin-top:.2rem'>🔗 "+lnk+"</div>" if lnk else ""}
                          {"<div style='font-size:.67rem;color:var(--green);margin-top:.2rem'>📁 "+fn+"</div>" if has_file and fn else ""}
                        </div>""", unsafe_allow_html=True)
                    with cb:
                        if st.button("🗑️", key=f"del_{proj.get('id')}"):
                            st.session_state.projects = [x for x in st.session_state.projects if x.get("id")!=proj.get("id")]
                            st.rerun()

        # ── TAB 3: CERTIFICATES ──
        with tab3:
            st.markdown(f"#### 🏅 {t('إدارة الشهادات','Manage Certificates')}")
            st.info(t(
                "أضف شهاداتك الحقيقية هنا — بتظهر في البورتفوليو والـ Chatbot فوراً!",
                "Add your real certificates here — they appear in the portfolio and chatbot instantly!"
            ))

            # Add new cert
            st.markdown(f"##### ➕ {t('إضافة شهادة جديدة','Add New Certificate')}")
            cc1, cc2 = st.columns(2)
            with cc1:
                c_name_ar = st.text_input(t("اسم الشهادة (عربي)","Certificate Name (AR)"), key="cn_ar")
                c_issuer  = st.text_input(t("جهة الإصدار","Issuing Organization"), key="ci", placeholder="DataCamp / Coursera / ...")
            with cc2:
                c_name_en = st.text_input(t("اسم الشهادة (إنجليزي)","Certificate Name (EN)"), key="cn_en")
                c_color   = st.selectbox(t("اللون","Color"), [
                    ("#00d4ff","🔵 Cyan"),("f97316","🟠 Orange"),
                    ("#a855f7","🟣 Purple"),("#22c55e","🟢 Green"),
                    ("#f72585","🔴 Pink"),("#eab308","🟡 Yellow"),
                ], format_func=lambda x: x[1], key="cc")[0]
            c_icon = st.text_input(t("إيموجي الشهادة","Certificate Emoji"), max_chars=2, placeholder="🎓", key="cion")

            # Upload cert image
            st.markdown(f"**📄 {t('رفع صورة الشهادة (اختياري)','Upload Certificate Image (optional)')}**")
            cert_file = st.file_uploader(
                t("صورة الشهادة","Certificate Image"),
                type=["jpg","jpeg","png","pdf"],
                key="cert_upload"
            )

            if st.button(t("✅ إضافة الشهادة","✅ Add Certificate"), type="primary", use_container_width=True, key="add_cert"):
                if not c_name_ar and not c_name_en:
                    st.error(t("❌ أدخل اسم الشهادة!","❌ Enter certificate name!")); st.stop()
                cert_b64  = ""
                cert_mime = ""
                if cert_file:
                    cert_file.seek(0)
                    cert_b64  = file_to_b64(cert_file)
                    cert_mime = cert_file.type
                st.session_state.certs.append({
                    "icon":     c_icon or "🎓",
                    "name_ar":  c_name_ar or c_name_en,
                    "name_en":  c_name_en or c_name_ar,
                    "issuer":   c_issuer,
                    "color":    c_color,
                    "cert_b64": cert_b64,
                    "cert_mime":cert_mime,
                })
                st.success(t(f"✅ تم إضافة شهادة '{c_name_ar or c_name_en}'!",
                              f"✅ Certificate '{c_name_en or c_name_ar}' added!"))
                st.rerun()

            # List existing certs
            st.markdown("---")
            st.markdown(f"##### {t('الشهادات الحالية','Current Certificates')} — {len(st.session_state.certs)}")
            for i, cert in enumerate(st.session_state.certs):
                cname = cert.get("name_ar","") if ar() else cert.get("name_en","")
                ca, cb, cc_btn = st.columns([5, 3, 1])
                with ca:
                    st.markdown(f"""
                    <div style="background:var(--ink3);border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;margin-bottom:.5rem">
                      <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.88rem">{cert.get("icon","🎓")} {cname}</div>
                      <div style="font-size:.68rem;color:var(--frost3)">{cert.get("issuer","")}</div>
                    </div>""", unsafe_allow_html=True)
                with cb:
                    if cert.get("cert_b64") and cert.get("cert_mime","").startswith("image/"):
                        st.image(f"data:{cert['cert_mime']};base64,{cert['cert_b64']}", width=80)
                    elif cert.get("cert_b64") and cert.get("cert_mime") == "application/pdf":
                        st.download_button(
                            t("⬇ PDF","⬇ PDF"),
                            data=base64.b64decode(cert["cert_b64"]),
                            file_name=f"cert_{i}.pdf",
                            mime="application/pdf",
                            key=f"dl_cert_{i}"
                        )
                with cc_btn:
                    if st.button("🗑️", key=f"del_cert_{i}"):
                        st.session_state.certs.pop(i)
                        st.rerun()

        # ── TAB 4: CHATBOT ──
        with tab4:
            st.markdown(f"### 🤖 {t('إعداد الـ Chatbot','Chatbot Setup')}")
            st.info(t(
                "الـ Chatbot يتعلم تلقائياً من بياناتك! أي مشروع أو معلومة تضيفها تظهر فوراً في إجاباته. يعمل بردود ذكية حتى بدون API Key.",
                "The chatbot learns from your data automatically! Any project or info you add appears instantly. Works with smart replies even without an API Key."
            ))
            ok = bool(st.secrets.get("ANTHROPIC_API_KEY",""))
            if ok:
                st.success(t("✅ Claude AI مفعّل — ردود ذكاء اصطناعي حقيقي!","✅ Claude AI active — Real AI responses!"))
            else:
                st.warning(t("⚠️ بيعمل بردود ذكية جاهزة — أضف API Key لتفعيل Claude AI الكامل",
                             "⚠️ Running smart fallback replies — Add API Key to enable full Claude AI"))
            st.code('ANTHROPIC_API_KEY = "sk-ant-api03-..."', language="toml")
            st.caption(t("حط ده في .streamlit/secrets.toml","Add this to .streamlit/secrets.toml"))
            if ok:
                tq = st.text_input(t("سؤال تجريبي","Test question"))
                if st.button(t("إرسال","Send")) and tq:
                    with st.spinner(""):
                        st.info(ask_claude(tq))

        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════
def main():
    inject_css()
    page = st.session_state._page

    if page == "portfolio":
        render_nav()
        render_hero()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_metrics()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_about()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_certs()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_projects()
        st.markdown('<div class="km-div"></div>', unsafe_allow_html=True)
        render_contact()
        st.markdown(f"""
        <div class="km-footer">
          <div class="km-footer-logo">{P("name_en")} ◈</div>
          <div class="km-footer-copy">Alexandria, Egypt 🇪🇬 · Data Analyst · © 2026</div>
        </div>""", unsafe_allow_html=True)
        render_chatbot()

    elif page == "admin":
        render_nav()
        if not st.session_state.admin_logged_in:
            render_login()
        else:
            render_admin()

if __name__ == "__main__":
    main()
