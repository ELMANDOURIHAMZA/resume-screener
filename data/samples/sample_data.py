"""
Sample resume and job description dataset generator.
Simulates realistic CV-job matching data for testing and demonstration.
"""

SAMPLE_JOB_DESCRIPTIONS = {
    "senior_python_engineer": """
Senior Python Engineer — FinTech Platform

We are looking for an experienced Python engineer to join our backend infrastructure team.

Requirements:
- 5+ years of Python development experience
- Deep knowledge of FastAPI, Django, or Flask
- Experience with PostgreSQL and Redis
- Strong understanding of OOP and design patterns
- Experience with Docker and Kubernetes
- Familiarity with AWS or GCP cloud services
- CI/CD pipeline management (Jenkins, GitHub Actions)
- Understanding of REST API design and microservices
- Experience with machine learning frameworks (scikit-learn, TensorFlow) is a plus
- Git proficiency and code review experience

Responsibilities:
- Design and implement scalable backend services
- Lead architecture decisions for new features
- Mentor junior developers
- Write comprehensive unit and integration tests
- Collaborate with data science team on ML model deployment

Nice to have:
- MLOps experience
- Kafka or RabbitMQ message queues
- Golang or Rust knowledge
""",
    "data_scientist": """
Data Scientist — NLP & Recommendation Systems

Join our AI team to build next-generation recommendation and personalization systems.

Requirements:
- 3+ years of data science experience
- Expert Python skills (pandas, numpy, scikit-learn)
- Strong NLP background (spaCy, Hugging Face, BERT, transformers)
- Experience with deep learning (PyTorch or TensorFlow)
- Machine learning model deployment (MLOps, model serving)
- SQL proficiency
- Statistical analysis and hypothesis testing
- Experience with Jupyter notebooks and experiment tracking (MLflow)

Responsibilities:
- Research and implement recommendation algorithms
- Build NLP pipelines for text classification and sentiment analysis
- Deploy models to production using Docker and REST APIs
- Collaborate with engineering on feature development
- Present findings to stakeholders

Nice to have:
- Experience with A/B testing frameworks
- Spark / distributed computing
- Knowledge of LLMs and prompt engineering
""",
    "frontend_developer": """
Frontend Developer — React & TypeScript

We're building a world-class web application and need a talented frontend engineer.

Requirements:
- 3+ years of frontend development
- Expert React and TypeScript skills
- Strong CSS3 and HTML5 knowledge
- Experience with state management (Redux, Zustand, or MobX)
- REST API integration and GraphQL
- Git, code review, and agile workflows
- Unit testing with Jest and React Testing Library
- Responsive design and cross-browser compatibility

Nice to have:
- Next.js or Remix experience
- CI/CD with GitHub Actions
- Node.js backend experience
- UX/UI design sensibility
- Performance optimization techniques
""",
}

SAMPLE_RESUMES = [
    {
        "id": "alice_chen",
        "name": "Alice Chen",
        "text": """
ALICE CHEN
alice.chen@email.com | LinkedIn: linkedin.com/in/alicechen | GitHub: github.com/alicechen

SUMMARY
Senior Software Engineer with 7 years of Python development experience specializing in backend systems,
API design, and cloud infrastructure. Passionate about clean code, scalability, and mentoring.

EXPERIENCE

Senior Python Engineer — DataFlow Inc (2020–Present)
- Designed and deployed FastAPI-based microservices handling 10M+ requests/day
- Built ML model serving infrastructure using Docker and Kubernetes on AWS
- Led a team of 5 engineers, conducted code reviews and architecture sessions
- Implemented CI/CD pipelines using GitHub Actions and Jenkins
- Optimized PostgreSQL queries resulting in 40% performance improvement
- Integrated Redis caching layer reducing latency by 60%

Backend Engineer — TechCorp (2017–2020)
- Built REST APIs using Django and Flask for e-commerce platform
- Managed AWS deployments (EC2, S3, RDS, Lambda)
- Implemented message queues with Kafka for async event processing
- Wrote unit and integration tests achieving 90% code coverage

SKILLS
Python, FastAPI, Django, Flask, PostgreSQL, Redis, Docker, Kubernetes, AWS, GCP,
Git, CI/CD, Jenkins, GitHub Actions, Kafka, REST APIs, Microservices, OOP, Design Patterns,
Machine Learning, scikit-learn, TensorFlow, MLOps

EDUCATION
B.Sc. Computer Science — MIT (2017)

CERTIFICATIONS
AWS Certified Solutions Architect, Google Cloud Professional
""",
    },
    {
        "id": "bob_martinez",
        "name": "Bob Martinez",
        "text": """
BOB MARTINEZ
bob.m@gmail.com | Portfolio: bobdev.io

SUMMARY
Full-stack developer with 4 years of experience. Comfortable with Python, JavaScript and cloud services.

EXPERIENCE

Software Developer — StartupXYZ (2021–Present)
- Built backend APIs using Python and Flask
- Worked with PostgreSQL databases
- Used Docker for containerization
- Deployed applications to AWS EC2

Junior Developer — WebAgency (2019–2021)
- Frontend development with React and JavaScript
- REST API integration

SKILLS
Python, Flask, JavaScript, React, PostgreSQL, Docker, AWS, Git

EDUCATION
B.Sc. Information Technology — State University (2019)
""",
    },
    {
        "id": "carol_nguyen",
        "name": "Carol Nguyen",
        "text": """
CAROL NGUYEN
carol.nguyen@proton.me | GitHub: github.com/carolng

SUMMARY
Data Scientist and ML Engineer with 5 years of experience building NLP systems and recommendation engines.
Expertise in deep learning, transformer models, and production ML deployment.

EXPERIENCE

Senior Data Scientist — AILabs (2021–Present)
- Built NLP text classification pipeline using spaCy and Hugging Face BERT, achieving 94% accuracy
- Designed recommendation system serving 2M+ daily active users
- Deployed ML models using FastAPI + Docker with MLflow experiment tracking
- Led A/B testing framework for model evaluation
- Used PyTorch for custom transformer fine-tuning

Data Scientist — AnalyticsHub (2019–2021)
- Developed predictive models using scikit-learn and XGBoost
- Built data pipelines with pandas and numpy
- Created dashboards with SQL and visualization tools
- Conducted statistical analysis and hypothesis testing

SKILLS
Python, PyTorch, TensorFlow, scikit-learn, pandas, numpy, spaCy, Hugging Face,
NLP, BERT, transformers, MLOps, MLflow, Docker, FastAPI, SQL, PostgreSQL,
Machine Learning, Deep Learning, Recommendation Systems, A/B Testing

EDUCATION
M.Sc. Machine Learning — Stanford University (2019)
B.Sc. Statistics — UC Berkeley (2017)

PUBLICATIONS
"Efficient BERT Fine-tuning for Domain-Specific NLP" — NeurIPS Workshop 2022
""",
    },
    {
        "id": "david_kim",
        "name": "David Kim",
        "text": """
DAVID KIM
david.kim@outlook.com

EXPERIENCE

Cashier — Supermart (2020–2022)
- Managed customer transactions
- Operated point-of-sale systems

Customer Service Representative — CallCenter Inc (2018–2020)
- Resolved customer complaints
- Used Microsoft Excel for reporting

EDUCATION
High School Diploma (2018)

SKILLS
Microsoft Office, Customer Service, Communication
""",
    },
    {
        "id": "emma_wilson",
        "name": "Emma Wilson",
        "text": """
EMMA WILSON
emma.wilson@gmail.com | GitHub: github.com/emmaw

SUMMARY
Backend Python engineer with 6 years of experience building distributed systems and APIs.
Strong background in OOP, design patterns, functional programming, and test-driven development.

EXPERIENCE

Principal Engineer — CloudSystems Ltd (2020–Present)
- Architected FastAPI microservices platform processing 50M events/day
- Implemented async concurrency patterns (asyncio, thread pools) for CPU-bound ML tasks
- Designed PostgreSQL schemas and Redis caching strategies
- Built Kubernetes deployments on GCP with Terraform infrastructure-as-code
- Introduced MLOps practices: model versioning, automated retraining pipelines
- Mentored 8 junior/mid-level engineers

Senior Engineer — DevHouse (2018–2020)
- Python backend development with Django REST Framework
- AWS infrastructure management (EC2, RDS, S3, Lambda)
- Kafka event streaming for real-time data pipelines
- Achieved 95%+ test coverage with pytest

SKILLS
Python, FastAPI, Django, Flask, OOP, Design Patterns, Functional Programming,
Asyncio, PostgreSQL, Redis, MongoDB, Docker, Kubernetes, GCP, AWS, Terraform,
Kafka, CI/CD, GitHub Actions, Jenkins, MLOps, scikit-learn, TensorFlow, Git

EDUCATION
M.Sc. Computer Science — Carnegie Mellon University (2018)

CERTIFICATIONS
Certified Kubernetes Administrator (CKA), AWS Solutions Architect Professional
""",
    },
]


def get_sample_jobs():
    return SAMPLE_JOB_DESCRIPTIONS


def get_sample_resumes():
    return SAMPLE_RESUMES


def get_demo_payload(job_key: str = "senior_python_engineer"):
    job = SAMPLE_JOB_DESCRIPTIONS.get(job_key, list(SAMPLE_JOB_DESCRIPTIONS.values())[0])
    return {
        "job_description": job,
        "resumes": [
            {"id": r["id"], "text": r["text"], "candidate_name": r["name"]}
            for r in SAMPLE_RESUMES
        ],
    }
