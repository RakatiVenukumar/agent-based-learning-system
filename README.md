# AI Agent-Based Educational Content System

## 📘 Overview
This project implements a simple agent-based system with two AI agents:
- Generator Agent
- Reviewer Agent

The system generates educational content and evaluates it using a structured pipeline.

---

## ⚙️ Features
- Structured content generation (explanation + MCQs)
- Automated review for:
  - Age appropriateness
  - Concept correctness
  - Clarity
- One-pass refinement based on feedback
- UI to visualize full agent pipeline

---

## 🧠 Agent Architecture
---

## 🧩 Agents

### 1. Generator Agent
- Generates explanation and MCQs
- Output is structured JSON

### 2. Reviewer Agent
- Evaluates generated content
- Returns:
  - status (pass/fail)
  - feedback

---

## 🔁 Refinement Logic
If the Reviewer returns **fail**, the Generator is re-run once with feedback.

---

## 🖥️ UI
The UI allows users to:
- Enter grade and topic
- View:
  - Generated content
  - Reviewer feedback
  - Refined output (if applicable)

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
python app.py