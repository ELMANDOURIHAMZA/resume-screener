import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.ranker import get_ranker

ranker = get_ranker()
res = ranker.rank('python developer', [])
print(json.dumps(res, ensure_ascii=False, indent=2))
