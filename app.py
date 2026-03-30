import streamlit as st
from datetime import datetime, timedelta
import requests

st.set_page_config(page_title="Lead Finder Últimos 30 Dias", layout="wide")
st.title("🎬 Lead Finder PRO – Últimos 30 dias")
st.write("Procurar leads públicos de editores (Cinema, Docs, Ads, Imobiliário).")

# Data limite 30 dias
data_limite = datetime.now() - timedelta(days=30)

# --- FONTES PÚBLICAS IMPLEMENTADAS ---
SOURCES = {
    "Reddit": ["https://www.reddit.com/search.json?q=film+editor&sort=new"],
    "Craigslist": ["https://geo.craigslist.org/iso/us"],  # exemplo placeholder
    "OLX.pt": ["https://www.olx.pt/emprego/?search%5Bfilter_enum_type%5D=job"],  # placeholder
    "Net-empregos": ["https://www.net-empregos.com/empregos?q=editor"],  # placeholder
    "CustoJusto": ["https://www.custojusto.pt/emprego"],  # placeholder
    "99Freelas": ["https://www.99freelas.com.br/projects"],  # placeholder
    "Workana": ["https://www.workana.com/jobs?category=design"],  # placeholder
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_reddit(urls):
    leads = []
    seen = set()
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS)
            data = r.json()
            for post in data.get("data", {}).get("children", []):
                utc = post["data"].get("created_utc", 0)
                date = datetime.fromtimestamp(utc)
                if date >= data_limite:
                    link = "https://reddit.com"+post["data"].get("permalink","")
                    if link not in seen:
                        leads.append({
                            "title": post["data"].get("title",""),
                            "link": link,
                            "date": date.strftime("%Y-%m-%d")
                        })
                        seen.add(link)
        except Exception as e:
            st.error(f"Erro Reddit: {e}")
    return leads

# Função genérica placeholder para outros sites
def fetch_placeholder(site_name, urls):
    st.info(f"{site_name}: scraping placeholder (funcionalidade futura)")
    return []

def fetch_all_leads():
    all_leads = {}
    all_leads["Reddit"] = fetch_reddit(SOURCES["Reddit"])
    # Outros sites apenas placeholders
    for site, urls in SOURCES.items():
        if site != "Reddit":
            all_leads[site] = fetch_placeholder(site, urls)
    return all_leads

if st.button("🔍 Procurar Leads Últimos 30 Dias"):
    leads_dict = fetch_all_leads()
    for site, leads in leads_dict.items():
        st.subheader(f"{site} ({len(leads)} leads)")
        for lead in leads:
            st.markdown(f"[{lead['title']}]({lead['link']}) ({lead['date']})")
        st.divider()
