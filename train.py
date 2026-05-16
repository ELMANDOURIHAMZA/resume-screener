import re
import os
import argparse
import unicodedata
import time
import json
import pandas as pd
import numpy as np
import joblib
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ── NETTOYAGE ────────────────────────────────────────────────────────────────

def ultra_clean(text):
    text = unicodedata.normalize("NFKC", str(text).lower())
    # Garde les lettres et les langages info (C++, C#)
    text = re.sub(r'[^a-z+#]', ' ', text)
    # Filtrage des mots courts (bruit)
    words = [w for w in text.split() if len(w) > 2 or w in ['c', 'c#']]
    return " ".join(words)

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main(csv_path):
    print("\n🔥 ULTIME TENTATIVE : OBJECTIF 90% 🔥")
    
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Resume_str', 'Category'])
    df['Category'] = df['Category'].str.strip().str.upper()
    
    print("[1/4] Nettoyage des textes...")
    X_raw = [ultra_clean(t) for t in df['Resume_str']]
    y = df['Category'].values

    print("[2/4] Vectorisation TF-IDF...")
    tfidf = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=60000,
        sublinear_tf=True,
        stop_words='english',
        max_df=0.5
    )
    X_tfidf = tfidf.fit_transform(X_raw)

    print("[3/4] Génération de données synthétiques (SMOTE) if available...")
    # Lazy import of optional dependencies so module can be imported without them
    try:
        from imblearn.over_sampling import SMOTE
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X_tfidf, y)
    except Exception:
        # Fallback: no resampling
        X_res, y_res = X_tfidf, y

    X_train, X_test, y_train, y_test = train_test_split(
        X_res, y_res, test_size=0.10, stratify=y_res, random_state=42 # 10% test pour plus de data train
    )

    # Définition des experts (multi_class supprimé)
    lr = LogisticRegression(C=20, max_iter=3000, class_weight='balanced') # C augmenté pour précision
    rf = RandomForestClassifier(n_estimators=200, n_jobs=-1)
    # Try to include LightGBM if available
    try:
        from lightgbm import LGBMClassifier
        lgb = LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=80, verbose=-1)
        estimators = [('lr', lr), ('lgb', lgb), ('rf', rf)]
        weights = [3, 3, 1]
    except Exception:
        estimators = [('lr', lr), ('rf', rf)]
        weights = [3, 1]

    ensemble = VotingClassifier(
        estimators=estimators,
        voting='soft',
        weights=weights
    )

    print(f"[4/4] Entraînement final sur {X_train.shape[0]} exemples...")
    t0 = time.time()
    ensemble.fit(X_train, y_train)
    print(f"Terminé en {time.time()-t0:.1f}s")

    # Évaluation
    preds = ensemble.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    print(f"\n🚀 SCORE DÉLIVRÉ : {acc*100:.2f}% Accuracy")
    print("\n" + classification_report(y_test, preds))

    os.makedirs("data/models", exist_ok=True)
    # Use configured model directory if available
    try:
        from app.core.config import VECTORIZER_PATH, CLASSIFIER_PATH, CLASSIFIER_META_PATH
        model_dir = VECTORIZER_PATH.parent
        model_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(tfidf, VECTORIZER_PATH)
        joblib.dump(ensemble, CLASSIFIER_PATH)
        meta = {
            "accuracy": float(acc),
            "classes": list(ensemble.classes_),
            "vectorizer": str(VECTORIZER_PATH.name),
            "classifier": str(CLASSIFIER_PATH.name),
            "saved_at": time.ctime(),
            "notes": "Trained with TF-IDF (1-3grams) + VotingClassifier (LR,LGBM,RF)",
        }
        with open(CLASSIFIER_META_PATH, "w", encoding="utf8") as fh:
            json.dump(meta, fh, indent=2, ensure_ascii=False)
        print(f"✅ Modèles sauvegardés dans {model_dir}")
    except Exception:
        # Fallback to legacy paths if project package not importable
        os.makedirs("data/models", exist_ok=True)
        joblib.dump(tfidf, "data/models/vectorizer.joblib")
        joblib.dump(ensemble, "data/models/category_classifier.joblib")
        print("✅ Modèles sauvegardés (fallback data/models)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=False, default=None,
                        help='Path to Resume.csv (default: data/Resume.csv)')
    args = parser.parse_args()
    csv_path = args.csv or (os.path.join('data', 'Resume.csv'))
    main(csv_path)