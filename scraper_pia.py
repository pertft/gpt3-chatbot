import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import re
import json
import string


links = ["https://www.bouvet.no/prosjekter/skalerbar-stordataplattform-gir-store-innovasjonsmuligheter",
"https://www.bouvet.no/prosjekter/kunstig-intelligens-for-smartere-bemanning-av-sikkerhetskontroll",
"https://www.bouvet.no/prosjekter/flomvarsling-med-sensorteknologi-og-datasjo",
"https://www.bouvet.no/prosjekter/skyss--prototyping-og-proof-of-concept-av-power-bi",
r"https://www.bouvet.no/prosjekter/digital-tvilling-av-kolonnekj%C3%B8ring",
"https://www.bouvet.no/prosjekter/sanntidsinformasjon-til-alle-som-tar-buss-i-rogaland",
"https://www.bouvet.no/prosjekter/gode-opplevelser-og-bedre-rapportering-med-maskinlaering-og-datavarehus",
"https://www.bouvet.no/prosjekter/effektiv-utnyttelse-av-data-med-ny-business-intelligence-plattform",
"https://www.bouvet.no/prosjekter/smart-prediksjon-av-isdannelse-gir-tryggere-drift-av-bybanen-i-bergen",
"https://www.bouvet.no/prosjekter/utvikling-av-power-bi-rapport-for-innkjopsseksjonen-i-vestland-fylkeskommune",
"https://www.bouvet.no/prosjekter/frilager.no",
"https://www.bouvet.no/prosjekter/bolgevarsel",
"https://www.bouvet.no/prosjekter/baerekraft-i-havbruk",
"https://www.bouvet.no/prosjekter/nordbohus",
"https://www.bouvet.no/prosjekter/ny-rapportdatabase-skal-sorge-for-bedre-innsikt-og-samarbeid-pa-tvers-for-hovedredningssentralen-i-bodo",
"https://www.bouvet.no/prosjekter/ved-hjelp-av-en-kreativ-konsulent-og-et-hjemmekontor-omgjort-til-lab-gikk-bane-nor-fra-manuell-overvakning-av-strommen-til-smart-og-prediktivt-vedlikehold",
"https://www.bouvet.no/prosjekter/nettdesign-pa-brukernes-premisser",
"https://www.bouvet.no/prosjekter/avansert-ai-loser-morgendagens-transportbehov-i-sporveien",
"https://www.bouvet.no/prosjekter/kunstig-intellgens-for-ekstrahering-av-metadata-fra-dokumenter",
"https://www.bouvet.no/prosjekter/bildeanalyse-og-maskinlaering-for-mer-effektive-arbeidsprosesser",
"https://www.bouvet.no/prosjekter/industriell-iot-for-baerekraftig-og-lonnsomt-fiskeoppdrett",
"https://www.bouvet.no/prosjekter/cappelen-damm",
"https://www.bouvet.no/prosjekter/takting-smart-flatestyring-copy-2",
"https://www.bouvet.no/prosjekter/overvaker-stromnettet-med-kunstig-intelligens-og-azure",
"https://www.bouvet.no/prosjekter/ny-hafslund-nett-app"]


tree = ET.parse('sitemap.xml')
root = tree.getroot()
for elem in root:
   for subelem in elem:
      if "vi-jobber-med/innsikt-data-og-analyse/" in subelem.text:
        links.append(subelem.text)

ps = []
for url in links:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        p = soup.find_all("p")

        # Find the lead for this URL to get more context.
        lead = ""
        for i in p:
            if i.has_attr("class") and i["class"][0] == "Lead":
                lead = i.text

        for i in p:
            if len(str(i)) < 300:
                None
            else:
                t = lead + " " + i.text
                t = t.replace("\n", "")
                t = t.replace("\"", "'")
                t = t.replace("“", "'")
                t = t.replace("”", "'")
                t = "{\"text\": \"%s\", \"metadata\": \"%s\"}" % (t, url)
                ps.append(t + "\n")


json_file = "".join(ps)
f = open("myfile_pia.jsonl", "w", encoding="utf-8")
f.write(json_file)
f.close()