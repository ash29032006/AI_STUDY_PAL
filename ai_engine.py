import json
import re
from bytez import Bytez

KEY = "1dadba3ffb4218718ba81252a6589b2a"
sdk = Bytez(KEY)
model = sdk.model("meta-llama/Llama-3.1-8B-Instruct")

def _run_llama(prompt, system_message="You are a helpful AI study assistant. Answer ONLY in valid JSON format."):
    results = model.run([
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ])
    
    if results.error:
        print(f"[Error from LLM]: {results.error}")
        return None
        
    text = results.output.get('content', '').strip()
    
    # Extract JSON if the model wrapped it in markdown code blocks
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        text = match.group(1)
        
    try:
        return json.loads(text)
    except Exception as e:
        print(f"[Error parsing JSON]: {e}")
        print(f"Raw output: {text}")
        return None

def generate_study_plan(subjects_list):
    # subjects_list is like [{"subject": "Math", "hours": 5}, {"subject": "Physics", "hours": 4}]
    subjects_str = ", ".join([f"'{s['subject']}' ({s['hours']} hours/week)" for s in subjects_list])
    prompt = f"""Create a weekly study plan for the following subjects: {subjects_str}.
Distribute the hours across 7 days (Monday to Sunday) appropriately.
Return ONLY valid JSON like this:
{{
  "plan": [
    {{"day": "Monday", "subject": "Math", "hours": 2, "activity": "Read chapter 1"}},
    ...
  ]
}}"""
    res = _run_llama(prompt)
    if not res:
        # Fallback
        plan = []
        for s in subjects_list:
            daily = round(s['hours']/7.0, 1)
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                plan.append({"day": day, "subject": s['subject'], "hours": daily, "activity": "Study"})
        return {"plan": plan}
    return res

def generate_quiz(text):
    prompt = f"""Generate a university-level 5-question multiple choice quiz based on the following text.
Text: "{text}"
Make sure each question has exactly 4 options and 1 correct answer. The difficulty should be university level.
Return ONLY valid JSON like this:
{{
  "questions": [
    {{
      "question": "What is...?",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "difficulty": "university"
    }},
    ...
  ]
}}"""
    res = _run_llama(prompt)
    if not res:
        return {"questions": []}
    return res

def summarize_text(text):
    prompt = f"""Summarize the following text clearly and concisely for a student.
Text: "{text}"
Return ONLY valid JSON like this:
{{
  "summary": "The main point is..."
}}"""
    res = _run_llama(prompt)
    if not res:
        return {"summary": "Could not generate summary."}
    return res

def generate_tips(topic):
    prompt = f"""Extract 3-5 main keywords from this topic, and give 3-5 actionable study tips.
Topic: "{topic}"
Return ONLY valid JSON like this:
{{
  "keywords": ["word1", "word2"],
  "tips": ["Tip 1", "Tip 2"]
}}"""
    res = _run_llama(prompt)
    if not res:
        return {"keywords": [], "tips": []}
    return res

def generate_feedback(subject):
    prompt = f"""Give a short, very inspiring 1-sentence motivational quote or message for a student studying '{subject}'.
Return ONLY valid JSON like this:
{{
  "message": "Keep studying..."
}}"""
    res = _run_llama(prompt)
    if not res:
        return {"message": "You are doing great! Keep going!"}
    return res
