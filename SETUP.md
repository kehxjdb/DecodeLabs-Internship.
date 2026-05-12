# 🚀 دليل تشغيل البورتفوليو — Karim Maher v3

## الملفات المطلوبة
- app.py          ← الكود الرئيسي
- requirements.txt ← المكتبات
- .streamlit/secrets.toml ← الـ API Key

---

## خطوة 1 — شغّله محلياً (اختياري)
```bash
pip install streamlit anthropic
streamlit run app.py
```

---

## خطوة 2 — ارفعه على GitHub
1. اعمل repo جديد اسمه `karim-portfolio`
2. ارفع `app.py` و `requirements.txt` بس
3. لا ترفع `secrets.toml` ❌

---

## خطوة 3 — Streamlit Cloud (مجاني)
1. روح share.streamlit.io
2. New App → اختار الـ repo
3. Main file: `app.py`
4. Secrets → حط:
```
ANTHROPIC_API_KEY = "sk-ant-..."
```
5. Deploy ✅

---

## الـ API Key للـ Chatbot
- روح console.anthropic.com
- اعمل API Key جديد
- حطه في الـ Secrets

## الباسورد الافتراضي
karim2024 (غيّره من لوحة التحكم)
