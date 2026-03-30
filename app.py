import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Lead Finder", layout="wide")

st.title("🎬 Lead Finder PRO")
st.write("Encontra pessoas à procura de editores (Cinema, Docs, Ads, Real Estate)")

KEYWORDS = [
"film editor", "movie editor", "short film", "feature film",
"documentary editor", "film project", "indie film",
"advertisement", "commercial editing",
"real estate video", "property video"
]

INTENT_KEYWORDS = [
"looking for", "need", "hiring", "editor wanted", "paid", "budget"
]

SOURCES = [
"https://www.reddit.com/search.json?q=film+editor&sort=new",
"https://www.reddit.com/search.json?q=documentary+editor&sort=new",
"https://www.reddit.com/search.json?q=advertisement+editor&sort=new",
"https://www.reddit.com/search.json?q=real+estate+video&sort=new"
]

HEADERS = {
"User-Agent": "Mozilla/5.0"
}

def fetch_leads():
leads = []
seen = set()

```
for url in SOURCES:
    try:
        r = requests.get(url, headers=HEADERS)
        data = r.json()

        for post in data.get("data", {}).get("children", []):
            title = post["data"].get("title", "")
            link = "https://reddit.com" + post["data"].get("permalink", "")
            date = datetime.fromtimestamp(post["data"].get("created_utc", 0))

            t = title.lower()

            if link not in seen and any(k in t for k in KEYWORDS) and any(k in t for k in INTENT_KEYWORDS):
                leads.append({
                    "title": title,
                    "link": link,
                    "date": date.strftime("%Y-%m-%d %H:%M")
                })
                seen.add(link)

    except Exception as e:
        st.error(e)

return leads
```

if st.button("🔍 Procurar Leads"):
results = fetch_leads()

```
if results:
    for lead in results:
        st.markdown(f"**[{lead['title']}]({lead['link']})**")
        st.caption(lead["date"])
        st.divider()
else:
    st.warning("Nenhum lead encontrado 😕")
```
