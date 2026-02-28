# AI Study Pal 📚

Hey! Welcome to **AI Study Pal**, a project I built to make studying less of a headache. I realized that as students, we waste so much time manually scheduling revisions, trying to find practice questions, and staring at giant textbook PDFs without actually retaining anything. So, I decided to build a tool that does the heavy lifting for us.

At its core, AI Study Pal is a full-stack web app that acts like your personal tutor, powered directly by **Meta's Llama-3.1-8B** model under the hood. 

---

## 🚀 What it actually does

* **Study Planner:** You just punch in what subjects you need to study and how many hours you have. It spits out a balanced 7-day schedule for you. You can even download it as a CSV.
* **PDF Quiz Generator:** *This is my favorite part.* You upload any lecture or textbook PDF, and the app reads it and generates a legit 5-question multiple-choice quiz based *only* on the text you uploaded.
* **Text Summarizer:** Paste in a massive wall of text, and get a quick, easy-to-digest summary back.
* **Study Tips & Keywords:** If you're stuck on a topic, type it in. It pulls out the main keywords you need to memorize and gives you actionable tips.
* **Motivation:** Just a fun little feature that gives you a customized motivational quote when you're feeling burned out.

---

## 🛠️ How I Built It (The Stack)

* **Backend:** Built entirely in **Python** using the **Flask** framework. Why Flask? Because I needed a secure way to talk to the AI without exposing my API keys to the frontend, and Flask made it super easy to set up the API endpoints.
* **The "Brain":** The real magic happens using the Bytez API to connect to the **Llama-3.1-8B-Instruct** model. I spent a lot of time doing strict "prompt engineering" to force the AI to return data purely as JSON format so my frontend could parse it without crashing.
* **Frontend UI Engine:** The interface is built with premium **dark-mode glassmorphism** layered over a dynamic, isometric 3D grid powered by **Anime.js**. The entire UI uses 3D perspective transforms (`translateZ`, `rotateX`) that track mouse movement in real time and trigger complex stagger ripple-animations when you interact with the app.

*(Note: There are a few older files in the repo like `ml_quiz.py` and `dl_summarizer.py`. Those were my early attempts at building this using classic Machine Learning tools like TensorFlow, Scikit-Learn, and NLTK before I realized that pivoting to an LLM made the app 100x smarter.)*

---

## ⚙️ How to run it yourself

Want to run this on your own machine? It's pretty straightforward:

1. **Clone the repo**
   ```bash
   git clone https://github.com/ash29032006/AI_STUDY_PAL.git
   cd AI_STUDY_PAL
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` if you're on Windows
   ```

3. **Install the dependencies**
   ```bash
   pip install flask flask-cors PyPDF2 bytez pandas matplotlib scikit-learn tensorflow nltk
   ```

4. **Fire it up!**
   ```bash
   python app.py
   ```
   Then just open up `http://localhost:5000` in your browser.

---

## 🤝 Let's Connect

Feel free to fork this, mess around with the code, or let me know if you build something cool on top of it. Happy studying!
