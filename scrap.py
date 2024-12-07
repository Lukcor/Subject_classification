import requests
from bs4 import BeautifulSoup
import pandas as pd

# Stocker les articles et les sujets dans un dictionnaire
data = {"article": [], "subject": []}

header = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
  "Connection": "keep-alive",
  "Cookie": "_pcid=%7B%22browserId%22%3A%22m293hq6gtrqp3wf3%22%2C%22_t%22%3A%22mhxkkdh0%7Cm293hqd0%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbABYAPANajWggIwAffgCYAnAGZBAR1ZSQAXyA; lmd_gdpr_token=96; atauthority=%7B%22name%22%3A%22atauthority%22%2C%22val%22%3A%7B%22authority_name%22%3A%22default%22%2C%22visitor_mode%22%3A%22optin%22%7D%2C%22options%22%3A%7B%22end%22%3A%222025-11-18T07%3A36%3A13.256Z%22%2C%22path%22%3A%22%2F%22%7D%7D; pa_privacy=%22optin%22; atidx=857A2098-7E48-42A...%2C%22gratuit%22%5D%7D; _cs_id=ade6ba36-0281-a5ec-9c90-0d93fc7fecbf.1732390672.2.1732412956.1732412284.1730815733.1766554672444.1; _sp_ses.fb3f=*; lmd_ab=mcT7V5Z8i91dFu330dOrwklb%2BVPa2J0%2Fvi4Xwv8%2BHXLcNpCAX1jygac4ScPIOmKabh73ved%2FRx0KaEkBmped1Z2nHLnWDKuynablS2mBv5jZfnuD8uRWA3OVKWs6ndRU81bDXJhTvWajCnomiybkQjuZO9loUyl1t86ZHRqk0T4GJ1YE6evePr%2BP9RPVTPKqmbYeNhY%3D; kw.session_ts=1732412275009; _cs_s=12.0.0.9.1732414788297; lmd_autopromo_cap=61aff89d576da54f66e8ce34b9807867; _cb_svref=external; _chartbeat5=",
  "Host": "www.lemonde.fr",
  "Priority": "u=0, i",
  "Referer": "https://www.lemonde.fr/recherche/",
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-User": "?1",
  "TE": "trailers",
  "Upgrade-Insecure-Requests": "1",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0"
}


# Scraping d'articles sur plusieurs pages
for l in ["sport", "politique", "economie", "intelligence+artificielle", "quantique"]:
    for i in range(1, 10):
        print(f"page {i}/10 de {l}")
        url = f"https://www.lemonde.fr/recherche/?search_keywords={l}&page={i}"

        r = requests.get(url, headers=header)
        soup = BeautifulSoup(r.content, 'html.parser')

        
        for page in soup.find_all(class_="teaser__link"):
            article_url = page.get('href')
            article_r = requests.get(article_url)
            article_soup = BeautifulSoup(article_r.content, 'html.parser')
            article_content = ""
            for n in article_soup.find_all(class_="article__paragraph"):
                article_content += n.text

            # Ajouter l'article et son sujet
            data["article"].append(article_content)
            data["subject"].append(l)

# Convertir les données en DataFrame
df = pd.DataFrame(data)
print(df)
df.to_csv("articles.csv", index=False)