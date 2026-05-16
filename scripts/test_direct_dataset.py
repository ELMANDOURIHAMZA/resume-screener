from app.services.ranker import get_ranker
from app.core.config import RESUME_CSV
import pandas as pd
import json

try:
    df = pd.read_csv(RESUME_CSV)
    resumes = [{"id": str(i), "text": str(t)} for i,t in enumerate(df['Resume_str'].astype(str).tolist())]
except Exception as e:
    print('failed to load csv', e)
    resumes = []

ranker = get_ranker()
res = ranker.rank('python developer', resumes)
print(json.dumps(res[:5], ensure_ascii=False, indent=2))
