"""Reviewed, topic-specific reading aids; no invented authors or publication dates."""
import html
import re
import unicodedata

PRACTICAL = {
    "wet-en-regelgeving-bali-vastgoed": ["Maak per object een register met landrecht, ruimtelijke bestemming, bouwdocumenten en beoogde exploitatie. Noteer wie elk onderdeel controleert.", "Bewaar bij iedere conclusie het documentnummer, de bevoegde instantie en de controledatum. Een verkoopbrochure vervangt dit dossier niet."],
    "wet-regelgeving-updates-bali": ["Houd een wijzigingslog bij met bron, publicatiedatum, ingangsdatum en de projecten waarop een wijziging mogelijk invloed heeft.", "Laat bij iedere relevante wijziging vastleggen welke bestaande conclusie opnieuw moet worden getoetst. Alleen een link opslaan is geen herbeoordeling."],
    "bouwnormen-bali": ["Vraag de constructeur om het funderingsontwerp, de gebruikte bodemgegevens en een inspectieplan voor de bouwfase.", "Koppel ieder opleverpunt aan een foto, locatie in het gebouw, verantwoordelijke partij en hersteltermijn. Sluit een punt pas na een aantoonbare hercontrole."],
    "bouwen-in-bali": ["Vergelijk offertes op dezelfde hoeveelheden, materialen, afwerking en uitsluitingen. Een lagere totaalprijs is zonder die vergelijking niet goed te beoordelen.", "Koppel betaaltermijnen aan controleerbare bouwmijlpalen. Leg voor meerwerk eerst prijs, planningseffect en schriftelijke goedkeuring vast."],
    "projectontwikkeling-bali": ["Maak een investeringsdossier met grondkosten, ontwerp, vergunningroute, bouwbudget, financiering en exit. Wijs elke aanname toe aan een bron of verantwoordelijke.", "Test wat vertraging en lagere verkoop- of verhuuropbrengsten met de kaspositie doen. Noteer wanneer aanvullende financiering nodig zou zijn."],
    "land-eigendom-overdracht-bali": ["Laat een lokale bevoegde adviseur titel, perceelidentiteit, tekenbevoegdheid en eventuele lasten naast het conceptcontract leggen.", "Maak vóór betaling een overzicht van overdrachtsdocumenten, betalingstriggers en nog openstaande controles. Leg ook toegang tot het perceel schriftelijk vast."],
    "pt-pma-opzetten-bali": ["Beschrijf eerst de feitelijke activiteiten: eigendom, ontwikkeling, verhuur of beheer. Laat daarna per activiteit de passende registratie en vergunningroute bepalen.", "Vraag naast oprichtingskosten ook een jaarlijks overzicht van administratie, rapportage, belastingen en beheer. Beoordeel de structuur over de hele exploitatieperiode."],
    "boekhouding-bouwprojecten-bali": ["Gebruik per bouwpost vier kolommen: oorspronkelijk budget, goedgekeurd meerwerk, verplichtingen en betaald. Zo wordt niet-betaald werk niet ten onrechte als budgetruimte gezien.", "Verbind iedere betaling aan contract, factuur, goedkeuring en bankbewijs. Houd valuta en gebruikte wisselkoers apart zichtbaar."],
    "project-management-bali-vastgoed": ["Maak per mijlpaal duidelijk wie uitvoert, wie controleert en wie mag goedkeuren. Geef beslissingen en meerwerk een eigen registratienummer.", "Vraag wekelijks dezelfde voortgangsset: planning, foto's, budgetafwijkingen, risico's en besluiten. Vergelijk deze met de vorige rapportage, niet alleen met de einddatum."],
    "buitenlandse-investeerders-bali-vastgoed": ["Leg vast of je contractuele rechten, aandelen, een lening of een ander belang verkrijgt. Vraag wie inkomsten ontvangt en wie besluiten over verkoop of beheer neemt.", "Werk een exitscenario uit met overdrachtsvoorwaarden, kosten, resterende looptijd en informatieplicht van de lokale partij."],
    "juridische-hulp-indonesie-vastgoed": ["Vraag vooraf een schriftelijke opdracht met onderzoeksvragen, uitgesloten werkzaamheden, kosten en verwachte documenten.", "Controleer wie de adviseur betaalt en of er een relatie is met verkoper of ontwikkelaar. Vraag om een schriftelijk oordeel over de concrete stukken, niet alleen algemene uitleg."],
    "certificeringen-vergunningen-bali": ["Maak een vergunningenmatrix: document, houder, perceel, toegestaan gebruik, geldigheid en verificatiebron. Vergelijk de matrix met het feitelijke gebouw en exploitatieplan.", "Bewaar originele bestanden en verifieerbare registratienummers. Noteer wie ontbrekende documenten aanvraagt, wanneer dat gebeurt en wat de gevolgen van vertraging zijn."],
    "verzekeringen-bali-vastgoed": ["Laat in de offerte vastleggen welk gebruik is verzekerd: bouw, eigen bewoning of commerciële verhuur. Vergelijk dekking, eigen risico, uitsluitingen en maximale uitkering.", "Bespreek afzonderlijk schade aan het gebouw, aansprakelijkheid en omzetverlies. Vraag welke meldingen en bewijsstukken bij een claim nodig zijn."],
    "verhuur-bali-villa": ["Vraag de beheerder een maandrapport met geboekte nachten, beschikbare nachten, dagprijs, platformkosten en uitbetaling aan de eigenaar.", "Test een laagseizoen met minder boekingen en een onderhoudsmaand zonder verhuur. Vergelijk de resterende kasstroom met vaste lasten en reserveringen."],
    "personeel-aannemen-bali": ["Leg vast welke partij werkgever is, wie de dagelijkse aansturing doet en wie loonadministratie en verplichte regelingen controleert.", "Begroot naast het basissalaris ook vervanging, verlof en overige werkgeverslasten. Laat de toepasselijke bedragen en verplichtingen lokaal bevestigen."],
    "rechten-plichten-bali-vastgoed": ["Zet per partij de rechten, verplichtingen, deadlines en gevolgen van niet-nakoming in één overzicht. Vergelijk dit overzicht met de ondertekende contracten.", "Werk vooraf uit hoe onderhoud, wijzigingen, wanbetaling, geschillen en beëindiging worden behandeld. Een mondelinge toezegging hoort niet als vast recht in je begroting."],
}

SIMBG = ("https://simbg.pu.go.id/dashboard", "SIMBG: officiële informatie en documentcontrole voor PBG en SLF")
OSS = ("https://oss.go.id/", "OSS: registratie en risicogebaseerde bedrijfsvergunningen; laat de route voor jouw activiteit bevestigen")
TARU = ("https://tarubali.baliprov.go.id/", "TARUBALI: ruimtelijke plannen en kaarten; geen vervanging voor perceelspecifieke bevestiging")
BPS = ("https://bali.bps.go.id/en", "BPS Bali: officiële regionale statistiek; geen rendementsprognose voor een individuele villa")
TAX = ("https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/vermogen_en_aanmerkelijk_belang/vermogen/wat_zijn_uw_bezittingen_en_schulden/uw_bezittingen/2e_woning", "Belastingdienst: tweede woning; laat woonplaats, structuur en verdragspositie afzonderlijk toetsen")
LAND = ("https://peraturan.go.id/files3/pp-no-18-tahun-2021_asli.pdf", "PP 18/2021: primaire regelgeving over landrechten, waaronder Hak Pakai")
SOURCES = {
    "kenniscentrum/pbg-slf-bali/index.html": [SIMBG, TARU],
    "kenniscentrum/airbnb-verhuur-bali-vergunningen/index.html": [OSS, SIMBG, TARU],
    "kenniscentrum/beste-gebieden-investeren-bali/index.html": [BPS, TARU],
    "kenniscentrum/nederlander-investeren-bali-belasting/index.html": [TAX],
    "hak-pakai-bali/index.html": [LAND],
    "toekomst-van-bali/index.html": [BPS, TARU],
    "vakantiewoning-bali-kopen/index.html": [OSS, SIMBG, BPS],
    "gids/index.html": [SIMBG, OSS, TARU],
}


def enhance_editorial(markup, relative):
    slug = relative.split('/')[-2] if '/' in relative else ''
    if relative.startswith('kenniscentrum/') and slug in PRACTICAL:
        boilerplate = [
            'De juiste beoordeling hangt af van het concrete object, de juridische structuur, zoning, vergunningen, kosten en je doel met de woning. Gebruik deze pagina daarom als startpunt voor due diligence, niet als aankoopadvies.',
            'Zie deze punten als reden om rustiger te kijken. Ze maken een object niet automatisch onbruikbaar, maar ze horen wel vóór een beslissing op tafel te liggen.',
            'Gebruik officiële bronnen en lokale specialisten waar het om documenten, vergunningen of belasting gaat. Marktinformatie is nuttig voor context, maar vervangt geen controle van het concrete object.',
        ]
        for text in boilerplate:
            markup = markup.replace('<p>' + text + '</p>', '')
        old = r'<p>Leg de verkoopinformatie naast drie dingen:.*?</p>\s*<p>Bij vastgoed op Bali zit de waarde.*?</p>'
        block = ''.join('<p>' + html.escape(p) + '</p>' for p in PRACTICAL[slug])
        markup = re.sub(old, block, markup, flags=re.S)
    if relative in SOURCES and 'id="officiele-bronnen"' not in markup:
        links = ''.join(f'<li><a href="{html.escape(url)}">{html.escape(label)}</a></li>' for url, label in SOURCES[relative])
        block = f'<section class="content-shell"><article class="content-card"><h2 id="officiele-bronnen">Officiële bronnen en verdere controle</h2><p>Deze bronnen helpen bij controle van de onderwerpen op deze pagina. Ze bevestigen niet dat een specifiek project is goedgekeurd. Bronverwijzingen toegevoegd op 2 oktober 2026; geen volledige juridische herbeoordeling.</p><ul class="source-list">{links}</ul></article></section>'
        markup = markup.replace('</main>', block + '\n</main>', 1)
    if relative in SOURCES or slug in PRACTICAL:
        markup = re.sub(r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"', '"dateModified": "2026-10-02"', markup)
        markup = markup.replace('Laatst bijgewerkt: 1 juli 2026.', 'Redactioneel bijgewerkt: 2 oktober 2026; geen volledige juridische herbeoordeling.')
    if relative.startswith('kenniscentrum/') and relative not in ('kenniscentrum/index.html', 'kenniscentrum/wiki/index.html'):
        markup = add_toc(markup)
    return markup


def add_toc(markup):
    if 'article-toc' in markup or 'Inhoudsopgave' in markup or 'In dit artikel' in markup:
        return markup
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', markup, re.S)
    if not main_match or len(re.findall(r'<h2\b', main_match[1])) < 4:
        return markup
    links = []
    used = set(re.findall(r'\bid="([^"]+)"', markup))
    def heading(match):
        attrs, title = match[1], match[2]
        found = re.search(r'\bid="([^"]+)"', attrs)
        if found:
            target = found[1]
        else:
            plain = html.unescape(re.sub(r'<[^>]+>', '', title))
            target = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', plain).encode('ascii', 'ignore').decode().lower()).strip('-') or 'onderdeel'
            base, n = target, 2
            while target in used:
                target, n = f'{base}-{n}', n + 1
            used.add(target)
            attrs += f' id="{target}"'
        links.append(f'<li><a href="#{target}">{title}</a></li>')
        return f'<h2{attrs}>{title}</h2>'
    main = re.sub(r'<h2([^>]*)>(.*?)</h2>', heading, main_match[1], flags=re.S)
    toc = '<nav class="article-toc content-shell" aria-label="Inhoudsopgave"><details><summary>In dit artikel</summary><ol>' + ''.join(links) + '</ol></details></nav>'
    main = main.replace('</section>', '</section>\n' + toc, 1)
    return markup[:main_match.start(1)] + main + markup[main_match.end(1):]
