"""Keep the searchable static catalogue and its structured data in sync."""
import html
import json
import re


def category(url):
    if re.search('belasting|boekhouding|rendement', url): return 'Kosten en rendement'
    if re.search('bouwen|bouwnormen|projectontwikkeling|project-management', url): return 'Bouwen en projecten'
    if re.search('management|verhuur|personeel|verzekeringen', url): return 'Verhuur en beheer'
    if re.search('leasehold|pma|zoning|pakai|regels|regelgeving|vergunning|pbg|eigendom|jurid|rechten|due-diligence', url): return 'Rechten en vergunningen'
    return 'Kopen en locaties'


def refresh_catalogue(markup, extra_cards=''):
    if 'class="knowledge-results"' not in markup: return markup
    pattern = r'<a class="article-link-card"[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
    cards = dict(re.findall(pattern, markup, re.S))
    cards.update(dict(re.findall(pattern, extra_cards, re.S)))
    latest = ['/kenniscentrum/villa-management-bali/', '/kenniscentrum/nieuwe-regels-bali-vastgoed-2026/']
    urls = [u for u in latest if u in cards] + [u for u in cards if u not in latest]
    rendered = '\n'.join(f'<a class="article-link-card" data-category="{category(u)}" href="{u}">{cards[u]}</a>' for u in urls)
    markup = re.sub(r'(<div class="knowledge-results">).*?(</div>)', lambda m:m[1]+rendered+m[2], markup, count=1, flags=re.S)
    markup = re.sub(r'(<p id="knowledge-count"[^>]*>).*?(</p>)', lambda m:m[1]+str(len(urls))+' artikelen'+m[2], markup, count=1, flags=re.S)
    items = []
    for i,u in enumerate(urls,1):
        title = re.search(r'<h3>(.*?)</h3>', cards[u], re.S)
        items.append({'@type':'ListItem','position':i,'url':'https://www.investinbali.nl'+u,'name':html.unescape(re.sub('<[^>]+>','',title[1])) if title else u})
    def update_schema(match):
        schema = json.loads(match[1])
        for node in schema.get('@graph',[schema]):
            if node.get('@type') == 'CollectionPage': node['mainEntity'] = {'@type':'ItemList','itemListElement':items}
        return '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>',update_schema,markup,flags=re.S)
