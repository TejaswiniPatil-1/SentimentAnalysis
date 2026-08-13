<div align="center">

# 🧠 SentimentIQ

### Intelligent Sentiment Analysis Through Machine Learning & NLP

**A Web-Based Multi-Model Framework for Real-Time Sentiment Analysis and Comparative Evaluation**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=for-the-badge\&logo=scikitlearn\&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
![NLP](https://img.shields.io/badge/NLP-Sentiment%20Analysis-8A2BE2?style=for-the-badge)

<br>

[![Live Demo](https://img.shields.io/badge/🚀_LIVE_DEMO-Launch_SentimentIQ-00C853?style=for-the-badge)](https://sentimentiq-tejaswini.streamlit.app/)

<br>

### Analyze • Predict • Compare • Visualize

</div>

---

## 🚀 About SentimentIQ

**SentimentIQ** is a web-based sentiment analysis system that combines **Natural Language Processing (NLP)** and **Machine Learning** to analyze textual data and predict sentiment in real time.

Rather than relying on a single classification technique, the system provides a **multi-model framework** that allows different machine learning algorithms to be evaluated within a unified application.

The project integrates the complete machine learning workflow — from text preprocessing and feature extraction to classification, comparative analysis, and interactive visualization.

> 💡 **Goal:** Transform unstructured textual data into meaningful sentiment insights through an accessible and interactive machine learning application.

---

## 🌐 Live Application

<div align="center">

### Experience SentimentIQ directly in your browser

[![Open Application](https://img.shields.io/badge/OPEN_SENTIMENTIQ-LIVE_APPLICATION-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://sentimentiq-tejaswini.streamlit.app/)

**No installation required — launch and analyze text directly online.**

</div>

---

## ✨ Key Features

<table>
<tr>

<td width="50%">

### ⚡ Real-Time Prediction

Analyze user-provided textual content and generate sentiment predictions through an interactive interface.

</td>

<td width="50%">

### 🤖 Multi-Model Analysis

Compare multiple machine learning algorithms within a unified sentiment analysis framework.

</td>

</tr>

<tr>

<td width="50%">

### 🧠 NLP Pipeline

Processes textual data using cleaning, normalization, transformation, and feature extraction techniques.

</td>

<td width="50%">

### 📊 Interactive Analytics

Visualizes analytical results to make model predictions and performance easier to understand.

</td>

</tr>

<tr>

<td width="50%">

### 🧩 Modular Architecture

Separates machine learning, visualization, authentication, interface, and styling components.

</td>

<td width="50%">

### 🔐 Authentication

Provides authentication functionality for controlled application access.

</td>

</tr>
</table>

---

## 🤖 Machine Learning Models

SentimentIQ implements multiple supervised machine learning algorithms for sentiment classification.

| Algorithm                         | Description                                                                |
| :-------------------------------- | :------------------------------------------------------------------------- |
| **Logistic Regression**           | Efficient linear classifier suitable for high-dimensional textual features |
| **Multinomial Naive Bayes**       | Probabilistic classifier widely used for text classification               |
| **Linear Support Vector Machine** | Margin-based classifier effective for sparse and high-dimensional NLP data |

The multi-model architecture enables comparative analysis of different approaches to text classification.

---

## 🔄 System Workflow

```text
                         ┌────────────────────────┐
                         │       USER INPUT       │
                         │    Text / Statement    │
                         └───────────┬────────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │    TEXT PREPROCESSING  │
                         │ Cleaning • Normalizing │
                         └───────────┬────────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │   FEATURE EXTRACTION   │
                         │   Text → Numerical     │
                         └───────────┬────────────┘
                                     │
                                     ▼
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ▼                    ▼                    ▼
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
        │   Logistic   │     │ Multinomial  │     │  Linear SVM  │
        │  Regression  │     │ Naive Bayes  │     │              │
        └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
               │                    │                    │
               └────────────────────┼────────────────────┘
                                    │
                                    ▼
                         ┌────────────────────────┐
                         │  SENTIMENT PREDICTION  │
                         └───────────┬────────────┘
                                     │
                                     ▼
                         ┌────────────────────────┐
                         │ RESULTS & VISUALIZATION│
                         └────────────────────────┘
```

---

## 🛠️ Technology Stack

<div align="center">

| Category                | Technology                              |
| :---------------------- | :-------------------------------------- |
| 🐍 **Programming**      | Python                                  |
| 🤖 **Machine Learning** | Scikit-learn                            |
| 🧠 **Domain**           | Natural Language Processing             |
| 🔤 **Text Processing**  | Feature Extraction & Text Vectorization |
| 📊 **Data Processing**  | Pandas, NumPy                           |
| 📈 **Visualization**    | Matplotlib                              |
| 🌐 **Web Application**  | Streamlit                               |
| 🔧 **Version Control**  | Git & GitHub                            |
| ☁️ **Deployment**       | Streamlit Community Cloud               |

</div>

---

## 📁 Project Architecture

```text
SentimentAnalysis/
│
├── 📂 sentimentiq/
│   │
│   ├── 📂 core/
│   │   ├── charts.py
│   │   └── pipeline.py
│   │
│   ├── 📂 ui/
│   │   ├── styles.py
│   │   └── tabs.py
│   │
│   ├── 🚀 app.py
│   ├── 🔐 auth.py
│   ├── 🧪 demo.py
│   ├── 📦 requirements.txt
│   └── .gitignore
│
├── 📂 assets/
│   ├── dashboard.png
│   ├── prediction.png
│   └── analytics.png
│
├── .gitignore
└── README.md
```

---

## 🧩 Core Components

### 🚀 `app.py`

The main application entry point responsible for integrating the user interface with the sentiment analysis functionality.

### 🧠 `core/pipeline.py`

Contains the primary text-processing and machine learning prediction pipeline.

### 📊 `core/charts.py`

Handles analytical charts and visualization components.

### 🔐 `auth.py`

Provides application authentication functionality.

### 🎨 `ui/styles.py`

Manages visual styling and interface presentation.

### 🗂️ `ui/tabs.py`

Organizes application features into structured interface sections.

---

## 📸 Application Preview

<div align="center">

### 🏠 Application Dashboard

<img src="assets/dashboard.png" width="850" alt="SentimentIQ Dashboard">

<br><br>

### 🧠 Real-Time Sentiment Prediction

<img src="assets/prediction.png" width="850" alt="SentimentIQ Prediction">

<br><br>

### 📊 Model Analysis & Visualization

<img src="assets/analytics.png" width="850" alt="SentimentIQ Analytics">

</div>

> **Note:** Add the corresponding application screenshots to the `assets` directory using the exact filenames shown above.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/TejaswiniPatil-1/SentimentAnalysis.git
```

### 2. Navigate to the Repository

```bash
cd SentimentAnalysis
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r sentimentiq/requirements.txt
```

---

## ▶️ Run Locally

Run the Streamlit application from the repository root:

```bash
streamlit run sentimentiq/app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

---

## 🎯 Potential Applications

SentimentIQ can be adapted for:

* 💬 Social media sentiment monitoring
* ⭐ Product review analysis
* 🛒 Customer feedback analysis
* 📢 Brand perception monitoring
* 📋 Survey response analysis
* 📰 Public opinion analysis
* 🎯 Marketing and customer-experience analytics

---

## 🔮 Future Enhancements

* Transformer-based NLP models
* Real-time social media integration
* Multilingual sentiment analysis
* Explainable AI (XAI)
* Advanced analytical dashboards
* REST API integration
* Cloud-based database support
* Enhanced authentication
* Automated model retraining
* Large-scale sentiment monitoring

---

## 🔒 Security & Privacy

Sensitive runtime information and authentication records are excluded from version control.

```text
.venv/
SentimentEnv/
users.json
__pycache__/
*.pyc
.env
```

> **Security Notice:** API keys, passwords, credentials, authentication records, and environment secrets should never be committed to a public GitHub repository.

---

## 🚀 Deployment

The application is deployed using **Streamlit Community Cloud** and connected directly to this GitHub repository.

Any production-ready updates pushed to the configured deployment branch can be reflected in the deployed application.

<div align="center">

[![Launch App](https://img.shields.io/badge/🚀_LAUNCH-SentimentIQ-FF4B4B?style=for-the-badge\&logo=streamlit)](https://sentimentiq-tejaswini.streamlit.app/)

</div>

---

## 👩‍💻 Developer

<div align="center">

### Tejaswini Patil

**Machine Learning • NLP • Python • Software Development**

[![GitHub](https://img.shields.io/badge/GitHub-TejaswiniPatil--1-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/TejaswiniPatil-1)

<br>

*Building intelligent applications through Machine Learning and Natural Language Processing.*

</div>

---

## ⭐ Support

<div align="center">

If you find **SentimentIQ** useful, consider giving this repository a **⭐ Star**.

### 🧠 SentimentIQ

**Analyze • Predict • Compare • Visualize**

</div>
