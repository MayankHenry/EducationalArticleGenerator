# 📚 Educational Article Generator (EAG)

A clean, production-ready backend service built with FastAPI that uses Large Language Models (LLMs) to automatically create structured, high-quality educational articles on any given topic.

## 🌟 Features

- **Automated Content Generation:** Uses an LLM (OpenRouter/DeepSeek) to generate articles on any topic.
- **Structured Output:** Articles are generated in a consistent Markdown format, including a title, introduction, main sections, summary, and further reading.
- **Customization:** Accepts optional parameters for **difficulty** (beginner, intermediate, advanced) and **target audience** (students, professionals).
- **File Downloads:** Download generated articles as **PDF** or **DOCX** files.
- **History Tracking:** A simple in-memory history of generated articles.
- **Modular Design:** Code is organized into `routes/`, `services/`, and `utils/` for easy maintenance and scalability.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A virtual environment is highly recommended.

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-username/educational-article-generator.git](https://github.com/your-username/educational-article-generator.git)
    cd educational-article-generator
    ```

2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Create a `.env` file in the root directory and add your OpenRouter API key:
    ```
    OPENROUTER_API_KEY="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"
    ```
    (Note: Replace with your actual key if different.)

### ▶️ Running the Application

Run the server with Uvicorn from the root directory:
```bash
uvicorn app.main:app --reload