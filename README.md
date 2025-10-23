## 🛍️ FeedbackPulse AI: E-commerce Review Analyst

This project is now live! View the fully interactive dashboard here:

### 🔗 **Live Application Link**

**[[Live Streamlit App URL Here](https://feedback-pulse-bl3gepcrgy4b2axjaxaoaz.streamlit.app/)]** 

***

## Project Overview

This project, **FeedbackPulse AI**, is a robust demonstration of **Generative AI (Gemini LLM)** and **Natural Language Processing (NLP)** transforming unstructured customer reviews into structured, actionable business intelligence.

It addresses the critical business need of rapidly analyzing large volumes of customer feedback to inform product development, marketing, and support prioritization.

### Key Features:

* **Generative Analysis:** Uses the Gemini LLM for structured output to automatically generate three key insights for every review:
    1.  **Sentiment:** (Positive, Negative, Neutral)
    2.  **Topic Tagging:** (e.g., `Sizing_Fit`, `Quality`, `Shipping_Delivery`)
    3.  **Action Item:** A concise, direct suggestion for the business.
* **Interactive Dashboard (Streamlit):** Presents the analysis with real-time charts (Sentiment Distribution, Top Topics) and filters for quick decision-making.
* **Python Stack:** Built using **Python**, **Pandas**, **Streamlit**, and the **Google GenAI SDK**.

***

## Project Files

| File | Description |
| :--- | :--- |
| `streamlit_app.py` | The main file that runs the interactive web dashboard and renders the charts. |
| `main.py` | The pipeline script that calls the LLM for batch analysis (executed once locally). |
| `llm_analyzer.py` | Contains the core Generative AI logic, JSON Schema, and prompt engineering. |
| `data_utils.py` | Handles data loading, cleaning, and sampling of raw reviews. |
| `master_analysis_data.csv` | **(Pre-Analyzed Data)** The final LLM-processed dataset, committed for fast, reliable cloud deployment. |
| `requirements.txt` | Lists all necessary Python dependencies (`streamlit`, `pandas`, `google-genai`, `plotly`). |

***

## 🚀 Getting Started (Local Setup)

To replicate and extend this project locally, follow these steps:

### 1. Prerequisites

* Python 3.8+
* A **Gemini API Key** (obtainable from the Google AI Studio).

### 2. Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/syedmoaz14/FEEDBACK-PULSE.git]
    cd feedback_pulse_ai
    ```
2.  **Activate Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate    # Mac/Linux
    .\venv\Scripts\activate     # Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. API Key Configuration

The project requires the `GEMINI_API_KEY` to be accessible as an environment variable for the LLM scripts.

* **Set Key:** Configure the environment variable in your terminal or your IDE's Run Configuration (recommended for PyCharm).
    ```bash
    export GEMINI_API_KEY="YOUR_KEY_HERE"
    ```

### 4. Run Locally

Since the analysis CSV is pre-committed, you can run the dashboard immediately:

```bash
streamlit run streamlit_app.py
