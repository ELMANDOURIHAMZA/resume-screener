# Resume Screening Assistant

An intelligent, automated system for screening and ranking CVs based on job descriptions. Leverages machine learning to accelerate recruitment processes while maintaining interpretability.

## 🎯 Features

- **Automated CV Screening** — Rank resumes based on relevance to job descriptions
- **TF-IDF Vectorization** — Efficient text similarity matching using term frequency-inverse document frequency
- **Category Classification** — Predict job categories for resumes using scikit-learn pipelines
- **Web Interface** — User-friendly UI for submitting job descriptions and viewing ranked results
- **Explainability** — Display matched keywords and relevance scores for transparency
- **Batch Processing** — Support for large-scale resume screening
- **Docker Deployment** — Containerized for production environments

## 📋 Requirements

- Python 3.8+
- Virtual environment (venv or conda)
- Dependencies listed in `requirements.txt`

## 🚀 Quick Start

### 1. Setup Environment

```powershell
# Clone the repository
git clone https://github.com/ELMANDOURIHAMZA/resume-screener.git
cd resume-screener

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
# Launch the application
python main.py

# Open http://127.0.0.1:8000/ in your browser
```

### 3. Using the Web Interface

1. Enter a job description in the text area
2. Specify the number of top candidates to display
3. Click "Classer les CV" to rank resumes
4. View results with scores and matched keywords

## 📂 Project Structure

```
resume-screener/
├── main.py                    # Application entry point
├── train.py                   # Model training script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Multi-container orchestration
├── REPORT.md                  # Detailed project report
├── README.md                  # This file
├── frontend/
│   └── index.html             # Web UI
├── data/
│   ├── Resume.csv             # Training/demo dataset
│   ├── models/
│   │   ├── vectorizer.joblib           # Pre-trained TF-IDF vectorizer
│   │   ├── category_classifier.joblib  # Category classifier model
│   │   └── classifier_meta.json        # Model metadata
│   └── samples/
│       └── sample_data.py              # Example usage and demo data
├── tools/
│   └── generate_report_pdf.py  # Script to convert REPORT.md to PDF
└── tests/
    └── test_all.py            # Unit and integration tests
```

## 🏗️ Architecture

### Components

- **Frontend** (`frontend/index.html`) — React-free, vanilla JavaScript UI
- **API** (`main.py`) — FastAPI application serving ranking and classification endpoints
- **Preprocessing** — Text cleaning, normalization, keyword extraction
- **Vectorization** — TF-IDF transformation for similarity computation
- **Scoring Engine** — Combines TF-IDF similarity, keyword overlap, and section weighting
- **Storage** — Joblib-persisted models in `data/models/`

### Data Flow

```
Job Description
       ↓
  Preprocessing → Vectorization → TF-IDF Similarity Calculation
       ↓                              ↓
  Keyword Extraction         Resume Corpus (Pre-vectorized)
       ↓                              ↓
  ────────────────────────────────────
       ↓
  Scoring Engine (Combine metrics)
       ↓
  Category Classifier (Optional filtering)
       ↓
  Ranked Results with Explanations
       ↓
  Frontend Display
```

## 🔧 API Endpoints

### POST `/api/v1/rank`

Submit a job description and receive ranked resumes.

**Request:**
```json
{
  "job_description": "We are looking for a senior Python developer with...",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "resume_id": "resume_001",
      "score": 0.85,
      "category": "Software Engineer",
      "keywords_matched": ["python", "fastapi", "machine learning"],
      "relevance": "Very Relevant"
    }
  ]
}
```

## 📊 Model Information

### Vectorizer
- **Type:** `TfidfVectorizer` (scikit-learn)
- **File:** `data/models/vectorizer.joblib`
- **Purpose:** Transform text → TF-IDF vectors

### Classifier
- **Type:** Scikit-learn Pipeline (LightGBM + SMOTE)
- **File:** `data/models/category_classifier.joblib`
- **Purpose:** Predict job category from resume text

### Metadata
- **File:** `data/models/classifier_meta.json`
- **Contents:** Model version, training date, evaluation metrics

## 🔄 Retraining Models

To retrain models on new data:

```powershell
python train.py
```

This will:
1. Load `data/Resume.csv`
2. Preprocess text
3. Train TF-IDF vectorizer and classifier
4. Save updated models to `data/models/`

## 🐳 Docker Deployment

### Build and Run

```powershell
# Build image
docker build -t resume-screener .

# Run container
docker run -p 8000:8000 resume-screener
```

### Docker Compose

```powershell
docker-compose up --build
```

Access the application at `http://localhost:8000`

## 📈 Performance Considerations

- **Latency:** Target < 2s per ranking query (with preloaded models)
- **Scalability:** Use worker threads or async processing for batch scoring
- **Caching:** Implement result caching for repeated queries
- **Monitoring:** Log query latencies and error rates

## ⚠️ Known Limitations

- `data/dataset_loader.py` is not included in this distribution; some training utilities may be unavailable
- CV parsing relies on CSV format; other formats require preprocessing
- Unbalanced classes in training data (mitigated with SMOTE)
- No semantic embeddings; keyword-based matching may miss contextual relevance

## 💡 Future Improvements

- Integrate SBERT or similar for semantic matching
- Implement role-based filtering and prioritization
- Add more robust section detection (PDF parsing)
- CI/CD pipeline for automated testing
- Advanced observability and monitoring
- Support for multiple languages

## 📄 Detailed Report

For a comprehensive technical report, see [REPORT.md](REPORT.md), which includes:
- Functional and non-functional specifications
- Architecture diagrams
- Evaluation metrics
- Deployment recommendations
- Glossary and appendices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License — see the LICENSE file for details.

## 👤 Authors

**Hamza El Mandouri** — Project Lead, Architecture & ML  
**Zakariya Kalakhy** — Development & Integration

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainer.

---

**Last Updated:** May 2026  
**Status:** Production-Ready
