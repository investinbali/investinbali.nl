"""Regression checks for the October UX and content corrections."""
import json
import re
from decimal import Decimal
from pathlib import Path
from render_seseh_returns import calculate, render
from knowledge_catalogue import refresh_catalogue, category

ROOT = Path(__file__).resolve().parents[1]
model = json.loads((ROOT/'data/seseh-scenarios.json').read_text(encoding='utf-8'))
rows = calculate(model)
assert [row['nights'] for row in rows] == [18,21,27]
assert [row['annual'] for row in rows] == [Decimal('517416000'),Decimal('611652000'),Decimal('794124000')]
seseh = (ROOT/'projecten/seseh-boutique-villas/index.html').read_text(encoding='utf-8')
assert render(model) in seseh, 'Generated scenario table drifted from its model'
assert '11-15%' not in seseh and '606-794' not in seseh
casa = (ROOT/'projecten/casa-surya-villas/index.html').read_text(encoding='utf-8')
assert '12-18%' not in casa and '7-15%' not in casa
assert 'https://schema.org/SoldOut' in casa
assert 'uitverkocht' in casa.lower()
home = (ROOT/'index.html').read_text(encoding='utf-8')
assert home.index('id="uitgelichte-projecten"') < home.index('Investeren in Bali vastgoed begint')
assert '<cite>' not in home and 'Wie mobiel zoekt' not in home
knowledge = (ROOT/'kenniscentrum/index.html').read_text(encoding='utf-8')
links = re.findall(r'<a class="article-link-card"[^>]+href="([^"]+)"', knowledge)
assert len(links) == len(set(links)) == 40
assert 'knowledge-search' in knowledge and 'knowledge-category' in knowledge
assert refresh_catalogue(knowledge) == knowledge
assert category('/kenniscentrum/project-management-bali-vastgoed/') == 'Bouwen en projecten'
script = (ROOT/'script.js').read_text(encoding='utf-8')
assert 'trackEvent("qualify_lead"' not in script
assert 'result.ok !== true' in script
assert 'guide_email_status' in script
assert 'setupMobileNavigation();' in script
contact = (ROOT/'contact/index.html').read_text(encoding='utf-8')
assert 'https://calendar.app.google/KmYX9vj1hj8wEcLe6' in contact
assert 'data-contact-panel' in contact
print('Audit regression checks passed: arithmetic, content, schema, catalogue and form contract.')
