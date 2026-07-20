from __future__ import annotations

import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.investinbali.nl"
TODAY = date.today().isoformat()

MONTHS_NL = [
    "januari",
    "februari",
    "maart",
    "april",
    "mei",
    "juni",
    "juli",
    "augustus",
    "september",
    "oktober",
    "november",
    "december",
]
UPDATED_LABEL = f"{date.today().day} {MONTHS_NL[date.today().month - 1]} {date.today().year}"


PAGES = [
    {
        "slug": "investeren-in-bali",
        "title": "Investeren in Bali vastgoed | Rendement en risico helder",
        "description": "Investeren in Bali? Vergelijk rendement, risico, leasehold, zoning en kosten voor huizen en villa's voordat je een object beoordeelt.",
        "h1": "Investeren in Bali: begin met de vragen die ertoe doen",
        "eyebrow": "INVESTEREN IN BALI",
        "intro": "Bali trekt veel aandacht van Nederlandse investeerders. Dat is logisch: de vraag naar goede woningen en short-stay verblijf blijft groot. Toch begint een goede beslissing niet bij een rendementspercentage, maar bij de vraag of locatie, juridische structuur, kosten en gebruiksdoel bij elkaar passen.",
        "intent": "Deze pagina is bedoeld voor wie Bali vastgoed serieus onderzoekt en een eerste kader wil voordat er met makelaars, ontwikkelaars of beheerders wordt gesproken.",
        "sections": [
            ("Wat maakt Bali interessant?", [
                "Bali combineert internationale vraag, beperkte toplocaties en een sterke lifestyle-markt. Vooral gebieden met duidelijke bereikbaarheid, voorzieningen en uitstraling kunnen interessant zijn voor eigen gebruik, waardegroei of short-stay verhuur.",
                "Dat betekent niet dat elk object automatisch een goede investering is. Twee villa's met vergelijkbare foto's kunnen totaal anders scoren op leaseperiode, bestemming, onderhoud, beheer en doorverkoopbaarheid.",
            ]),
            ("Waar kijk je eerst naar?", [
                "Begin met vier onderdelen: locatie, juridische structuur, bestemming en kosten. Pas daarna wordt rendement zinvol. Een berekening zonder zicht op beheer, platformkosten, lokale lasten, onderhoud en leegstand geeft vooral schijnzekerheid.",
                "Voor buitenlandse kopers zijn leasehold, Hak Pakai of een zakelijke structuur zoals PT PMA onderwerpen die per situatie moeten worden uitgezocht. De juiste route hangt af van doel, budget, gebruik en risicobereidheid.",
            ]),
            ("Wanneer is het een serieuze optie?", [
                "Een object wordt interessanter wanneer de documenten kloppen, de zoning past bij het beoogde gebruik, de leasevoorwaarden overdraagbaar zijn en het rendement niet alleen op optimistische bezetting leunt.",
                "Vraag daarom altijd om onderbouwing: welke dagprijs is realistisch, welke kosten zijn meegenomen, wie beheert het object, en wat gebeurt er als de markt tijdelijk afkoelt?",
            ]),
        ],
        "checklist": [
            "Past het gebied bij jouw doel: eigen gebruik, verhuur, waardegroei of exit?",
            "Is duidelijk welk recht je krijgt en hoe lang dat recht loopt?",
            "Zijn zoning, PBG/SLF en eventueel exploitatievergunningen gecontroleerd?",
            "Zijn beheer, OTA-kosten, onderhoud en lokale belastingen meegenomen?",
            "Is er een realistisch scenario naast het optimistische scenario?",
        ],
        "faq": [
            ("Is investeren in Bali vastgoed veilig?", "Nee, niet automatisch. Het kan interessant zijn, maar alleen wanneer documenten, structuur, locatie en exploitatie goed worden gecontroleerd."),
            ("Wat is een realistische eerste stap?", "Download een gids, vergelijk objecten op vaste criteria en bespreek daarna je doel, budget en risicobereidheid met iemand die de lokale praktijk kent."),
        ],
        "sources": [
            ("BPS Bali tourism statistics", "https://bali.bps.go.id/"),
            ("Indonesian land regulation PP 18/2021", "https://www.peraturan.go.id/files2/pp-no-18-tahun-2021_terjemah.pdf"),
        ],
    },
    {
        "slug": "huis-kopen-bali",
        "title": "Huis kopen Bali | Regels, leasehold en kosten",
        "description": "Huis kopen op Bali? Lees de regels voor Nederlandse kopers: leasehold, zoning, kosten, juridische structuur en doorverkoopbaarheid.",
        "h1": "Huis kopen op Bali: kijk verder dan de foto's",
        "eyebrow": "HUIS KOPEN BALI",
        "intro": "Een huis op Bali kopen klinkt overzichtelijk: je ziet een mooie woning, vraagt de prijs op en vergelijkt locaties. In de praktijk zit de echte beoordeling dieper. Je wilt weten welk recht je krijgt, of het gebruik past bij de bestemming en welke kosten na aankoop blijven terugkomen.",
        "intent": "Deze pagina helpt Nederlandse kopers om een woning op Bali zakelijker te beoordelen, ook als het object deels voor eigen gebruik bedoeld is.",
        "sections": [
            ("Eigen gebruik of investering?", [
                "Een huis voor eigen gebruik mag anders worden beoordeeld dan een woning die vooral cashflow moet opleveren. Voor eigen gebruik wegen comfort, omgeving en persoonlijke voorkeur zwaarder. Voor investering tellen overdraagbaarheid, beheerbaarheid en verhuurpotentie sterker mee.",
                "Veel kopers willen een combinatie. Dat kan, maar dan moet je vooraf accepteren dat persoonlijk gebruik invloed heeft op bezetting en netto-opbrengst.",
            ]),
            ("De juridische laag", [
                "Buitenlandse kopers kunnen niet zomaar dezelfde eigendomspositie krijgen als Indonesische kopers. Leasehold, Hak Pakai of een passende juridische structuur moeten door lokale specialisten worden gecontroleerd.",
                "Let vooral op resterende looptijd, verlengopties, overdraagbaarheid, betalingsmomenten en wat er gebeurt bij verkoop of overlijden.",
            ]),
            ("Praktische due diligence", [
                "Vraag niet alleen om een brochure, maar om documenten. Denk aan landcertificaat, leasecontract, bouwdocumentatie, bestemming, toegangsweg, water, stroom, beheerafspraken en eventuele verhuurlicenties.",
                "Een huis dat goedkoop lijkt, kan duur worden als onderhoud, legalisatie of infrastructuur achteraf nog geregeld moet worden.",
            ]),
        ],
        "checklist": [
            "Is het doel van de aankoop helder?",
            "Is de juridische structuur schriftelijk uitgewerkt?",
            "Is de resterende leaseperiode lang genoeg voor jouw plan?",
            "Past het beoogde gebruik binnen zoning en vergunningen?",
            "Is er een exit-scenario als je later wilt verkopen?",
        ],
        "faq": [
            ("Kan een Nederlander een huis op Bali kopen?", "Een Nederlander kan belangen in vastgoed structureren, maar niet simpelweg dezelfde vrije grondeigendom krijgen als een Indonesische koper. Laat de structuur lokaal controleren."),
            ("Is leasehold altijd slecht?", "Nee. Leasehold kan werkbaar zijn wanneer looptijd, verlenging, overdraagbaarheid en prijs bij je doel passen."),
        ],
        "sources": [
            ("PP 18/2021 land rights", "https://www.peraturan.go.id/files2/pp-no-18-tahun-2021_terjemah.pdf"),
            ("Bali zoning information", "https://tarubali.baliprov.go.id/"),
        ],
    },
    {
        "slug": "villa-kopen-bali",
        "title": "Villa kopen Bali | Kosten, verhuur en risico's",
        "description": "Een villa kopen op Bali? Beoordeel locatie, bouwkwaliteit, leasehold, beheer, short-stay potentie, kosten en risico's voordat je beslist.",
        "h1": "Villa kopen op Bali: wanneer klopt het totaalplaatje?",
        "eyebrow": "VILLA KOPEN BALI",
        "intro": "Een villa op Bali verkoopt zichzelf vaak via beeld: zwembad, tropische tuin, open leefruimte en een populaire locatie. Voor een investering is dat pas de eerste laag. De vraag is of de villa juridisch, technisch en commercieel verdedigbaar is.",
        "intent": "Deze pagina is voor kopers die een villa zoeken voor eigen gebruik, verhuurpotentie of latere verkoop.",
        "sections": [
            ("Locatie blijft leidend", [
                "Een villa in Canggu, Berawa, Pererenan, Uluwatu, Sanur of Seminyak heeft niet automatisch dezelfde vraag. Binnen elk gebied maken bereikbaarheid, geluid, uitzicht, toegang en directe omgeving veel verschil.",
                "Vraag jezelf af wie de toekomstige gebruiker is: familie, digital nomad, high-end vakantiehuurder of koper bij doorverkoop. Die doelgroep bepaalt mede wat een goede villa is.",
            ]),
            ("Bouwkwaliteit en onderhoud", [
                "Tropisch klimaat is hard voor gebouwen. Ventilatie, dakdetails, waterafvoer, vocht, zwembadtechniek en materiaalkeuze zijn geen details. Ze bepalen onderhoudskosten en gastbeleving.",
                "Laat bij bestaande villa's technische inspectie doen. Bij nieuwbouw wil je duidelijke tekeningen, planning, betalingsschema en oplevercriteria.",
            ]),
            ("Verhuur is geen vanzelfsprekendheid", [
                "Een mooie villa kan goed verhuren, maar alleen met juiste prijsstelling, beheer, vergunningen, reviews, foto's, OTA-strategie en service. Reken daarom met meerdere scenario's.",
                "Netto-opbrengst ligt vaak lager dan bruto omzet doordat beheer, platformkosten, onderhoud, personeel, belastingen en reserveringen eerst betaald moeten worden.",
            ]),
        ],
        "checklist": [
            "Wie is de doelgroep van deze villa?",
            "Zijn bouwkwaliteit en onderhoud realistisch beoordeeld?",
            "Is short-stay gebruik toegestaan en praktisch uitvoerbaar?",
            "Zijn beheerpartij en kostenstructuur duidelijk?",
            "Is het object later goed overdraagbaar?",
        ],
        "faq": [
            ("Is een villa op Bali vooral lifestyle of investering?", "Dat verschilt per object. De beste beoordeling kijkt naar beide: persoonlijk gebruik en zakelijke onderbouwing."),
            ("Waar gaat het vaak mis?", "Bij te optimistische verhuurprognoses, onduidelijke leasevoorwaarden en onderschat onderhoud."),
        ],
        "sources": [
            ("BPS Bali", "https://bali.bps.go.id/"),
            ("OSS business licensing", "https://oss.go.id/"),
        ],
    },
    {
        "slug": "vastgoed-bali-rendement",
        "title": "Vastgoed Bali rendement | Bruto en netto realistisch",
        "description": "Lees hoe je vastgoedrendement op Bali beoordeelt: bruto omzet, netto resultaat, bezetting, dagprijs, beheer, OTA-kosten en risico's.",
        "h1": "Vastgoedrendement op Bali: bruto is nog geen netto",
        "eyebrow": "BALI VASTGOED RENDEMENT",
        "intro": "Rendement is vaak het eerste getal waarnaar wordt gekeken. Juist daarom moet je er kritisch mee omgaan. Een bruto indicatie zegt weinig wanneer bezetting, dagprijs, beheer, onderhoud, belastingen en platformkosten niet helder zijn.",
        "intent": "Deze pagina helpt je rendementsclaims op Bali vastgoed nuchter te lezen en naast meerdere scenario's te leggen.",
        "sections": [
            ("Begin met omzet, niet met percentage", [
                "Een rendementspercentage lijkt handig, maar de berekening erachter is belangrijker. Kijk eerst naar gemiddelde dagprijs, bezettingsgraad en seizoenspatroon. Daarna pas naar kosten en netto-opbrengst.",
                "Vraag bij elk object of de cijfers gebaseerd zijn op historische resultaten, vergelijkbare villa's of een verkoopprognose.",
            ]),
            ("Kosten maken het verschil", [
                "Bij short-stay verhuur kunnen beheer, OTA-commissies, schoonmaak, onderhoud, personeel, vervangingen, lokale heffingen en reserveringen stevig drukken op de bruto omzet.",
                "Een scenario zonder onderhoudsreserve is meestal te optimistisch. Tropisch vastgoed vraagt doorlopend aandacht.",
            ]),
            ("Werk met drie scenario's", [
                "Gebruik minimaal een voorzichtig, basis- en optimistisch scenario. Het voorzichtige scenario is vaak het nuttigst, omdat het laat zien of het object ook bij lagere bezetting verdedigbaar blijft.",
                "Rendement moet nooit los worden gezien van juridische structuur, leaseperiode en exit. Een goed percentage op een zwakke structuur is nog steeds een zwakke investering.",
            ]),
        ],
        "checklist": [
            "Is het rendement bruto of netto?",
            "Welke bezettingsgraad en dagprijs zijn gebruikt?",
            "Zijn beheer, OTA en onderhoud meegenomen?",
            "Is er een reserve voor leegstand en vervanging?",
            "Past het rendement bij het risico van locatie en structuur?",
        ],
        "faq": [
            ("Wat is een goed rendement op Bali vastgoed?", "Dat hangt af van locatie, structuur, kosten en risico. Een percentage zonder onderbouwing is niet genoeg."),
            ("Waarom is netto belangrijker dan bruto?", "Omdat de investeerder uiteindelijk leeft met wat overblijft na kosten, beheer, onderhoud en belastingen."),
        ],
        "sources": [
            ("BPS Bali tourism data", "https://bali.bps.go.id/"),
            ("AirDNA market data", "https://www.airdna.co/"),
        ],
    },
    {
        "slug": "leasehold-bali",
        "title": "Leasehold Bali | Looptijd, verlenging en risico's",
        "description": "Leasehold op Bali uitgelegd: looptijd, verlenging, overdraagbaarheid, risico's, contractvoorwaarden en vragen voor due diligence.",
        "h1": "Leasehold op Bali: niet eng, wel precies lezen",
        "eyebrow": "LEASEHOLD BALI",
        "intro": "Leasehold is voor veel Nederlandse kopers wennen. Je koopt niet simpelweg volle eigendom van de grond, maar krijgt een contractueel gebruiksrecht voor een afgesproken periode. Dat kan werken, mits de voorwaarden passen bij je plan.",
        "intent": "Deze pagina legt uit welke vragen je moet stellen voordat je een leasehold woning of villa op Bali serieus beoordeelt.",
        "sections": [
            ("De looptijd bepaalt veel", [
                "Een resterende lease van 18 jaar voelt anders dan 28 of 30 jaar met duidelijke verlengoptie. De looptijd beïnvloedt gebruik, doorverkoopbaarheid, financieringslogica en rendement.",
                "Kijk niet alleen naar de hoofdlijn in de brochure. Lees wie partij is bij het contract, wanneer betaald moet worden en hoe verlenging wordt berekend.",
            ]),
            ("Overdraagbaarheid en verlenging", [
                "Een belangrijk punt is of je het recht later kunt overdragen aan een koper. Ook wil je weten of verlenging een recht, optie of intentie is, en tegen welke prijs.",
                "Als verlenging afhankelijk is van toekomstige onderhandelingen, hoort dat in je risicoanalyse en prijsbeoordeling.",
            ]),
            ("Leasehold en verhuur", [
                "Leasehold zegt nog niet automatisch iets over verhuur. Daarvoor kijk je ook naar zoning, vergunningen, beheer en de afspraken in het contract.",
                "Een leasehold villa kan interessant zijn voor short-stay, maar alleen wanneer het beoogde gebruik juridisch en praktisch klopt.",
            ]),
        ],
        "checklist": [
            "Wat is de resterende looptijd?",
            "Is verlenging schriftelijk geregeld?",
            "Is overdracht aan een koper toegestaan?",
            "Wie is de grondeigenaar en zijn documenten gecontroleerd?",
            "Past de prijs bij de resterende rechten?",
        ],
        "faq": [
            ("Is leasehold hetzelfde als eigendom?", "Nee. Leasehold is een gebruiksrecht voor een bepaalde periode, met voorwaarden die contractueel worden vastgelegd."),
            ("Kan leasehold interessant zijn?", "Ja, maar alleen wanneer looptijd, verlenging, overdraagbaarheid en gebruiksdoel helder zijn."),
        ],
        "sources": [
            ("PP 18/2021 land rights", "https://www.peraturan.go.id/files2/pp-no-18-tahun-2021_terjemah.pdf"),
            ("ATR/BPN land administration", "https://www.atrbpn.go.id/"),
        ],
    },
    {
        "slug": "airbnb-rendement-bali",
        "title": "Airbnb rendement Bali | Kosten, bezetting en regels",
        "description": "Airbnb rendement op Bali beoordelen? Lees hoe dagprijs, bezetting, beheer, OTA-kosten, vergunningen en seizoenen het netto resultaat bepalen.",
        "h1": "Airbnb-rendement op Bali: kijk naar het hele exploitatiemodel",
        "eyebrow": "AIRBNB RENDEMENT BALI",
        "intro": "Airbnb-potentie is een veelgebruikt argument bij Bali vastgoed. Het kan een serieuze factor zijn, maar alleen wanneer je verder kijkt dan bezetting en mooie reviews. De exploitatie moet juridisch, operationeel en financieel kloppen.",
        "intent": "Deze pagina helpt je short-stay verhuur op Bali beoordelen zonder te snel te vertrouwen op optimistische prognoses.",
        "sections": [
            ("Dagprijs en bezetting", [
                "Een hoge gemiddelde dagprijs is alleen relevant als die past bij locatie, seizoen, doelgroep en concurrentie. Bezetting kan per maand sterk verschillen.",
                "Gebruik geen enkel jaargemiddelde zonder te vragen hoe laagseizoen, onderhoudsdagen en eigen gebruik zijn verwerkt.",
            ]),
            ("Beheer en gastbeleving", [
                "Short-stay verhuur draait op uitvoering: communicatie, schoonmaak, onderhoud, check-in, reviews, pricing en probleemoplossing. Een zwakke beheerpartij kan een sterke villa alsnog matig laten presteren.",
                "Vraag daarom naar beheercontract, kosten, rapportage, reserveringen en wie verantwoordelijk is voor klachten of schade.",
            ]),
            ("Vergunningen en compliance", [
                "Niet elk woonobject is automatisch geschikt voor commerciële short-stay verhuur. Zoning, bedrijfsregistratie, lokale regels en belastingpositie moeten per object worden gecontroleerd.",
                "Als een rendementsmodel leunt op verhuur die nog niet juridisch is onderbouwd, is het model nog niet klaar.",
            ]),
        ],
        "checklist": [
            "Is de dagprijs gebaseerd op vergelijkbare objecten?",
            "Is bezetting per seizoen doorgerekend?",
            "Zijn OTA- en beheerkosten zichtbaar?",
            "Zijn vergunningen en lokale regels gecontroleerd?",
            "Is er een plan voor onderhoud en reviewkwaliteit?",
        ],
        "faq": [
            ("Is Airbnb op Bali altijd toegestaan?", "Nee. Het hangt af van bestemming, vergunningen, structuur en lokale regels. Laat dit vooraf controleren."),
            ("Welke kosten worden vaak vergeten?", "OTA-commissies, beheer, schoonmaak, onderhoud, vervanging, lokale heffingen en leegstand."),
        ],
        "sources": [
            ("OSS licensing", "https://oss.go.id/"),
            ("BPS Bali tourism statistics", "https://bali.bps.go.id/"),
            ("AirDNA", "https://www.airdna.co/"),
        ],
    },
    {
        "slug": "bali-vastgoed-belasting",
        "title": "Bali vastgoed belasting | Fiscale vragen en risico's",
        "description": "Welke belastingvragen spelen bij Bali vastgoed? Lees over lokale heffingen, verhuurinkomsten, structuur, Nederland en fiscale due diligence.",
        "h1": "Belasting bij Bali vastgoed: neem het vroeg mee",
        "eyebrow": "BALI VASTGOED BELASTING",
        "intro": "Belasting is niet het spannendste deel van een vastgoedplan, maar het bepaalt wel je netto resultaat. Bij Bali vastgoed spelen mogelijk Indonesische heffingen, verhuurinkomsten, lokale belastingen en je Nederlandse fiscale positie mee.",
        "intent": "Deze pagina geeft geen fiscaal advies, maar helpt je de juiste vragen klaarzetten voor een fiscalist of lokale adviseur.",
        "sections": [
            ("Netto begint na belasting", [
                "Een verhuurprognose zonder fiscale laag is onvolledig. Lokale heffingen, inkomstenbelasting, bedrijfsstructuur en rapportageverplichtingen kunnen invloed hebben op wat er netto overblijft.",
                "Ook de vraag wie juridisch verhuurt is belangrijk: jij persoonlijk, een lokale partij, een PT PMA of een beheerstructuur.",
            ]),
            ("Nederlandse positie", [
                "Nederlandse investeerders moeten ook hun eigen fiscale positie bekijken. Denk aan woonplaats, vermogen, buitenlandse inkomsten, rapportage en eventuele verdragsvragen.",
                "Dit is precies het type onderwerp dat je niet via een brochure wilt oplossen. Laat het beoordelen door iemand die jouw persoonlijke situatie kent.",
            ]),
            ("Documentatie", [
                "Bewaar contracten, facturen, beheerafrekeningen, betalingsbewijzen en rapportages. Zonder administratie wordt rendement achteraf lastig te controleren.",
                "Goede administratie helpt ook bij verkoop, omdat een koper wil zien welke opbrengsten en kosten werkelijk zijn gemaakt.",
            ]),
        ],
        "checklist": [
            "Wie ontvangt de verhuurinkomsten?",
            "Welke lokale heffingen en belastingen zijn relevant?",
            "Is de Nederlandse fiscale positie bekeken?",
            "Worden kosten en inkomsten goed gerapporteerd?",
            "Is de structuur afgestemd met een fiscalist?",
        ],
        "faq": [
            ("Is dit fiscaal advies?", "Nee. Dit is een vragenlijst voor voorbereiding. Laat je situatie beoordelen door een fiscalist."),
            ("Waarom hoort belasting in de aankoopfase?", "Omdat belasting invloed heeft op netto rendement, structuur en administratie."),
        ],
        "sources": [
            ("Indonesian tax authority", "https://www.pajak.go.id/"),
            ("Dutch tax authority foreign assets", "https://www.belastingdienst.nl/"),
        ],
    },
    {
        "slug": "bali-vastgoed-risico",
        "title": "Bali vastgoed risico | Waar moet je kritisch naar kijken?",
        "description": "Bali vastgoed risico's uitgelegd: leasehold, zoning, vergunningen, beheer, kosten, bezetting, onderhoud, valuta en doorverkoopbaarheid.",
        "h1": "Risico's bij Bali vastgoed: helder krijgen vóór je beslist",
        "eyebrow": "BALI VASTGOED RISICO",
        "intro": "Risico is geen reden om Bali vastgoed te negeren. Het is wel reden om langzamer en scherper te kijken. De meeste problemen ontstaan niet door één groot punt, maar door een stapeling van onduidelijke documenten, te optimistische aannames en haast.",
        "intent": "Deze pagina geeft een praktisch risicokader voor Nederlandse kopers en investeerders.",
        "sections": [
            ("Juridische risico's", [
                "Denk aan onduidelijke leasevoorwaarden, korte resterende looptijd, zwakke verlengopties, beperkte overdraagbaarheid of een structuur die niet past bij het beoogde gebruik.",
                "Laat contracten niet alleen vertalen, maar inhoudelijk toetsen. De vraag is wat je werkelijk krijgt en wat je later kunt overdragen.",
            ]),
            ("Locatie en regelgeving", [
                "Een gebied kan populair zijn, maar toch problemen hebben met toegang, geluid, water, infrastructuur of bestemming. Zoning en vergunningen horen daarom vroeg in de beoordeling.",
                "Toeristische vraag is waardevol, maar lokale handhaving, community issues en infrastructuur kunnen de exploitatie beïnvloeden.",
            ]),
            ("Financiële risico's", [
                "Rendement kan tegenvallen door lagere bezetting, lagere dagprijs, hogere kosten, onderhoud, valutabewegingen of zwak beheer.",
                "Werk daarom met buffers. Als een object alleen interessant is in het meest optimistische scenario, is dat een signaal om verder te vragen.",
            ]),
        ],
        "checklist": [
            "Is de juridische structuur helder en passend?",
            "Is zoning op perceelniveau gecontroleerd?",
            "Zijn vergunningen en exploitatievoorwaarden bekend?",
            "Is het rendement ook bij lagere bezetting verdedigbaar?",
            "Is er een realistische exit of doorverkooproute?",
        ],
        "faq": [
            ("Wat is het grootste risico?", "Vaak niet één punt, maar de combinatie van onduidelijke rechten, zwakke documentatie en te rooskleurige cijfers."),
            ("Hoe beperk je risico?", "Door documenten, bestemming, kosten, beheer en scenario's vooraf te toetsen en niet te beslissen op foto's alleen."),
        ],
        "sources": [
            ("Bali spatial planning portal", "https://tarubali.baliprov.go.id/"),
            ("PP 18/2021", "https://www.peraturan.go.id/files2/pp-no-18-tahun-2021_terjemah.pdf"),
        ],
    },
    {
        "slug": "pt-pma-bali-vastgoed",
        "title": "PT PMA Bali vastgoed | Structuur, OSS en risico's",
        "description": "PT PMA bij Bali vastgoed uitgelegd: wanneer relevant, wat betekent OSS/NIB, welke vragen stel je en welke risico's moet je toetsen?",
        "h1": "PT PMA voor Bali vastgoed: nuttig in sommige situaties, niet standaard",
        "eyebrow": "PT PMA BALI VASTGOED",
        "intro": "Een PT PMA wordt vaak genoemd zodra buitenlandse investeerders over Bali vastgoed praten. Soms is zo'n Indonesische vennootschap relevant, bijvoorbeeld bij exploitatie of grotere zakelijke plannen. Maar het is geen magische oplossing voor elke aankoop.",
        "intent": "Deze pagina helpt je bepalen wanneer een PT PMA-vraag serieus onderzocht moet worden met een lokale jurist of corporate advisor.",
        "sections": [
            ("Wanneer komt PT PMA in beeld?", [
                "Een PT PMA kan relevant worden wanneer er sprake is van zakelijke exploitatie, personeel, meerdere objecten, vergunningen of een activiteit die formeel door een Indonesische entiteit moet worden gedragen.",
                "Voor puur persoonlijk gebruik is een PT PMA niet automatisch logisch. Kosten, administratie, kapitaaleisen en compliance moeten meewegen.",
            ]),
            ("OSS, NIB en KBLI", [
                "Bij een zakelijke structuur kom je termen tegen als OSS, NIB en KBLI. Die gaan over bedrijfsregistratie, identificatie en activiteitenclassificatie.",
                "De gekozen activiteit moet passen bij wat je werkelijk doet. Een verkeerde of te algemene classificatie kan later problemen geven bij vergunningen of exploitatie.",
            ]),
            ("Laat structuur volgen uit doel", [
                "Begin niet met de vraag 'moet ik een PT PMA?'. Begin met doel, gebruik, risico, exploitatie en exit. Daarna kan een adviseur bepalen welke structuur past.",
                "Een goede structuur is begrijpelijk, uitvoerbaar en administratief vol te houden. Als niemand kan uitleggen waarom de structuur nodig is, is dat een rode vlag.",
            ]),
        ],
        "checklist": [
            "Is er zakelijke exploitatie of alleen eigen gebruik?",
            "Welke activiteit moet formeel worden geregistreerd?",
            "Zijn OSS, NIB en KBLI passend gekozen?",
            "Zijn administratie en compliancekosten realistisch?",
            "Is de structuur uitgelegd door een lokale specialist?",
        ],
        "faq": [
            ("Heb je altijd een PT PMA nodig?", "Nee. Dat hangt af van doel, gebruik, exploitatie en juridische structuur."),
            ("Is een PT PMA juridisch advies?", "De keuze voor een PT PMA moet met lokale juridische en fiscale adviseurs worden gemaakt."),
        ],
        "sources": [
            ("OSS Indonesia", "https://oss.go.id/"),
            ("BKPM / Ministry of Investment", "https://www.bkpm.go.id/"),
        ],
    },
]


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def header() -> str:
    return """<header class="site-header">
      <a class="brand" href="/" aria-label="Invest in Bali home"><span class="brand-mark">⌂</span><span class="brand-text">INVEST IN BALI</span></a>
      <nav class="main-nav" aria-label="Hoofdnavigatie">
        <a href="/projecten/">Projecten</a>
        <a href="/kenniscentrum/">Kenniscentrum</a>
        <a href="/over-ons/">Over ons</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </nav>
      <a class="button button-gold header-cta" href="/contact/">PLAN EEN CALL</a>
    </header>"""


def footer() -> str:
    return """<footer class="site-footer">
      <div>
        <h3>Invest in Bali</h3>
        <p>Huizen op Bali voor kopers en investeerders die duidelijkheid willen over potentie, risico en structuur.</p>
        <a class="footer-email" href="mailto:info@investinbali.nl">info@investinbali.nl</a>
      </div>
      <div class="footer-column">
        <h4>Navigatie</h4>
        <a href="/projecten/">Projecten</a>
        <a href="/kenniscentrum/">Kenniscentrum</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </div>
      <div class="footer-column">
        <h4>Populaire zoekvragen</h4>
        <a href="/investeren-in-bali/">Investeren in Bali</a>
        <a href="/huis-kopen-bali/">Huis kopen Bali</a>
        <a href="/villa-kopen-bali/">Villa kopen Bali</a>
        <a href="/vastgoed-bali-rendement/">Bali vastgoed rendement</a>
        <a href="/leasehold-bali/">Leasehold Bali</a>
        <a href="/toekomst-van-bali/">Toekomst van Bali</a>
      </div>
    </footer>
    <script src="/analytics-config.js"></script>
    <script src="/script.js"></script>"""


def schema(page: dict) -> str:
    canonical = f"{BASE_URL}/{page['slug']}/"
    faq_entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in page["faq"]
    ]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "inLanguage": "nl-NL",
                "dateModified": TODAY,
                "author": {"@type": "Organization", "name": "Invest in Bali"},
                "publisher": {"@type": "Organization", "name": "Invest in Bali"},
                "mainEntityOfPage": canonical,
                "image": f"{BASE_URL}/assets/gids-2026/due-diligence-zoning.webp",
            },
            {"@type": "FAQPage", "mainEntity": faq_entities},
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": page["h1"], "item": canonical},
                ],
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def page_html(page: dict) -> str:
    canonical = f"{BASE_URL}/{page['slug']}/"
    sections = "\n".join(
        f"""          <article class="content-card">
            <h2>{esc(title)}</h2>
            {''.join(f'<p>{esc(paragraph)}</p>' for paragraph in paragraphs)}
          </article>"""
        for title, paragraphs in page["sections"]
    )
    checklist = "\n".join(f"<li>{esc(item)}</li>" for item in page["checklist"])
    faqs = "\n".join(
        f"""          <details class="faq-item">
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
          </details>"""
        for q, a in page["faq"]
    )
    sources = "\n".join(f'<li><a href="{esc(url)}">{esc(label)}</a></li>' for label, url in page["sources"])
    related = [
        ("/projecten/", "Bekijk projecten", "Vergelijk beschikbare objecten op locatie, structuur, doel en indicatief rendement."),
        ("/kenniscentrum/", "Lees het kenniscentrum", "Verdiep je in leasehold, zoning, due diligence, exploitatie en risico's."),
        ("/gids/", "Download de gids", "Gebruik de gids als eerste filter voordat je concrete objecten beoordeelt."),
        ("/contact/", "Plan een call", "Bespreek jouw budget, doel en vragen voordat je verder gaat met een object."),
    ]
    if page["slug"] == "investeren-in-bali":
        related = [
            ("/kenniscentrum/due-diligence-bali/", "Due diligence Bali", "Controleer documenten, zoning, contracten en aannames voordat je beslist."),
            ("/bali-vastgoed-belasting/", "Belasting bij Bali vastgoed", "Neem lokale en Nederlandse fiscale vragen mee in je netto rendement."),
            ("/vastgoed-bali-rendement/", "Vastgoedrendement Bali", "Vertaal bruto verhuurprognoses naar realistische netto scenario's."),
            ("/pt-pma-bali-vastgoed/", "PT PMA Bali vastgoed", "Bekijk wanneer een Indonesische structuur relevant kan zijn."),
            *related,
        ]
    related_links = "\n".join(
        f'<a class="article-link-card" href="{href}"><h3>{label}</h3><p>{esc(description)}</p></a>'
        for href, label, description in related
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(page['title'])}</title>
    <meta name="description" content="{esc(page['description'])}" />
    <meta name="robots" content="index,follow" />
    <meta name="theme-color" content="#161311" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="nl_NL" />
    <meta property="og:site_name" content="Invest in Bali" />
    <meta property="og:title" content="{esc(page['title'])}" />
    <meta property="og:description" content="{esc(page['description'])}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:image" content="{BASE_URL}/assets/gids-2026/due-diligence-zoning.webp" />
    <meta property="og:image:alt" content="Documenten, zoningkaart en rendementsanalyse voor Bali vastgoed." />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{schema(page)}</script>
  </head>
  <body class="subpage seo-landing">
    {header()}
    <main>
      <section class="subpage-hero">
        <p class="eyebrow">{esc(page['eyebrow'])}</p>
        <h1>{esc(page['h1'])}</h1>
        <p>{esc(page['intro'])}</p>
        <p class="form-note">{esc(page['intent'])} Laatst bijgewerkt: {UPDATED_LABEL}.</p>
        <div class="hero-actions">
          <a class="button button-gold" href="/contact/">Plan een call</a>
          <a class="button button-outline" href="/gids/">Download gids</a>
        </div>
      </section>
      <section class="content-shell longform">
        <div class="grid grid-two">
{sections}
          <article class="content-card">
            <h2>Snelle checklist</h2>
            <ul class="plain-list">{checklist}</ul>
          </article>
          <article class="content-card">
            <h2>Veelgestelde vragen</h2>
{faqs}
          </article>
        </div>
        <article class="content-card">
          <h2>Bronnen en verdieping</h2>
          <p>Gebruik deze pagina als startpunt. Laat contracten, vergunningen en fiscale keuzes altijd controleren door lokale en Nederlandse specialisten.</p>
          <ul class="source-list">{sources}</ul>
        </article>
        <article class="content-card">
          <h2>Verder lezen of vergelijken</h2>
          <div class="article-list">
            {related_links}
          </div>
        </article>
        <div class="cta-panel">
          <div>
            <h2>Wil je dit toepassen op een concreet object?</h2>
            <p>Plan een gesprek. Dan kijken we naar jouw doel, budget, locatievoorkeuren, juridische structuur, kosten en risico's voordat je verder gaat.</p>
          </div>
          <div class="cta-actions">
            <a class="button button-gold" href="/contact/">Plan een call</a>
            <a class="button button-outline" href="/projecten/">Bekijk projecten</a>
          </div>
        </div>
      </section>
    </main>
    {footer()}
  </body>
</html>
"""


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for page in PAGES:
        loc = f"{BASE_URL}/{page['slug']}/"
        if loc in text:
            continue
        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
"""
        text = text.replace("</urlset>", entry + "</urlset>")
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(text, encoding="utf-8")


def update_knowledge_index() -> None:
    path = ROOT / "kenniscentrum" / "index.html"
    text = path.read_text(encoding="utf-8")
    marker = "Startvragen voor kopers en investeerders"
    if marker in text:
        text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        path.write_text(text, encoding="utf-8")
        return
    cards = "\n".join(
        f'''              <a class="article-link-card" href="/{esc(page['slug'])}/">
                <h3>{esc(page['h1'])}</h3>
                <p>{esc(page['description'])}</p>
              </a>'''
        for page in PAGES
    )
    block = f"""          <article class="content-card knowledge-wide-card">
            <h2>{marker}</h2>
            <p>Deze pagina's helpen je snel grip te krijgen op de eerste keuzes: investeren, kopen, leasehold, rendement, belasting, risico's en de toekomst van Bali.</p>
            <div class="article-list">
{cards}
            </div>
          </article>"""
    text = text.replace("</div>\n      </section>\n    </main>", f"{block}\n        </div>\n      </section>\n    </main>", 1)
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for page in PAGES:
        target = ROOT / page["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_html(page), encoding="utf-8")
    update_knowledge_index()
    update_sitemap()


if __name__ == "__main__":
    main()
    from site_postprocess import enhance_site

    enhance_site()
