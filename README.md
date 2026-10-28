# ProjectMatch 🚀
> **Find Your First AI Project in 60 Minutes**

ProjectMatch is an AI-powered Streamlit web application designed for final-year engineering students. It uses a Groq-hosted LLM (`llama-3.3-70b-versatile`) to generate 3 personalized, practical, and resume-ready AI project ideas tailored to a student's branch, interests, and skill level. It also includes an integrated workshop registration flow and referral reward system.

---

## ✨ Features

- **Personalized Recommendations**: Suggests 3 tailored AI project ideas based on engineering discipline, interests, and coding proficiency.
- **Ultra-Fast Generation**: Powered by Groq's low-latency inference using Llama 3.3.
- **Smart Diversity Filter**: Built-in similarity guard ensures fresh, varied ideas across sessions.
- **Workshop Registration**: Seamless pre-filled registration integration with Google Forms.
- **Referral & Rewards Engine**: Unique referral code generation and milestone-based reward tiers (Starter Kit, Prompt Pack, Priority Certificate).
- **Responsive Modern UI**: Custom light-theme frosted glass interface with responsive layout.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **LLM Provider**: [Groq](https://console.groq.com/) (`llama-3.3-70b-versatile`)
- **Data & Utilities**: `pandas`, `Pillow`, `python-dotenv`

---

## 🚀 Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/naveen-111q/Prototype.git
cd Prototype
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory (refer to `.env.example`):
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
> Get your free Groq API key at [console.groq.com/keys](https://console.groq.com/keys).

### 5. Run the application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push your code to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
3. Click **"New app"** and select:
   - **Repository**: `naveen-111q/Prototype`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced Settings** → **Secrets**, and add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   ```
5. Click **Deploy!**

---

## 📄 License
MIT License
