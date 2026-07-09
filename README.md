# AI-901: Introduction to AI in Azure — Faculty Study Kit

A complete, self-contained study and teaching kit for **Exam AI-901 (Introduction to AI in Azure)**.
All content in this repository is **original material** authored from publicly available
[Microsoft Learn documentation](https://aka.ms/mslearn-ai-901). It contains **no Microsoft
courseware content**, so it can be freely shared with faculty and students.

> **Exam skill areas** (per the official study guide)
>
> | Study area | Weight |
> |---|---|
> | Identify AI concepts and capabilities | ~40% |
> | Implement AI solutions with Microsoft Foundry | ~60% |

---

## 🚀 Quick start

| I want to… | Go to |
|---|---|
| Take the interactive quizzes & mock exams | **[index.html](index.html)** (open locally or via GitHub Pages) |
| Read the study notes | [`modules/`](modules/) — 6 chapters below |
| Teach with slides | [`pptx/`](pptx/) — 7 ready-to-present PowerPoint decks |
| Print / distribute the full course | [`pdf/AI-901-Complete-Course.pdf`](pdf/AI-901-Complete-Course.pdf) |
| Prep participants for mock tests (term glossary) | [`pdf/AI-901-Exam-Terminology-Reference.pdf`](pdf/AI-901-Exam-Terminology-Reference.pdf) |
| Reuse the diagrams | [`diagrams/`](diagrams/) — original SVG diagrams |

### Hosting the quiz portal on GitHub Pages
1. Push this repository to GitHub.
2. **Settings → Pages → Source: Deploy from a branch → `main` / root**.
3. The portal is served at `https://<user>.github.io/<repo>/`.

---

## 📚 Course index

| # | Module (study notes) | Slides | Quizzes (30 Q each, timed) |
|---|---|---|---|
| 0 | Course overview & exam guide *(this page + intro deck)* | [Deck 0](pptx/AI901-00-Course-Overview.pptx) | — |
| 1 | [AI concepts & getting started with AI in Azure](modules/01-ai-concepts-and-azure.md) | [Deck 1](pptx/AI901-01-AI-Concepts-and-Azure.pptx) | Quiz 1A · Quiz 1B |
| 2 | [Generative AI and agents](modules/02-generative-ai-and-agents.md) | [Deck 2](pptx/AI901-02-Generative-AI-and-Agents.pptx) | Quiz 2A · Quiz 2B |
| 3 | [Natural language processing & text analysis](modules/03-nlp-and-text-analysis.md) | [Deck 3](pptx/AI901-03-NLP-and-Text-Analysis.pptx) | Quiz 3A · Quiz 3B |
| 4 | [AI speech](modules/04-ai-speech.md) | [Deck 4](pptx/AI901-04-AI-Speech.pptx) | Quiz 4A · Quiz 4B |
| 5 | [Computer vision](modules/05-computer-vision.md) | [Deck 5](pptx/AI901-05-Computer-Vision.pptx) | Quiz 5A · Quiz 5B |
| 6 | [Information extraction](modules/06-information-extraction.md) | [Deck 6](pptx/AI901-06-Information-Extraction.pptx) | Quiz 6A · Quiz 6B |
| — | **Final mock exam 1** (45 Q, mixed, timed) | — | via [index.html](index.html) |
| — | **Final mock exam 2** (45 Q, mixed, timed) | — | via [index.html](index.html) |

All quizzes are launched from **[index.html](index.html)** — light-themed, timed, one correct
answer per question, with a full **review mode** that explains why each option is right or wrong
(just like the real exam experience). Difficulty mix per quiz: ~25% easy, ~25% moderate, ~50% hard.

---

## 🗂 Repository layout

```
├── index.html              ← Quiz & mock-exam portal (GitHub Pages entry point)
├── assets/                 ← Portal CSS + exam engine JS
├── quizzes/                ← Question banks (12 section quizzes + 2 final exams)
├── modules/                ← Study notes, one markdown chapter per module
├── diagrams/               ← Original SVG diagrams (+ PNG exports for slides)
├── pptx/                   ← PowerPoint decks (0–6)
├── pdf/                    ← Complete course PDF (all modules + diagrams)
│   └── src/                ← HTML source used to render the PDF
└── _archive/               ← Earlier drafts (not part of the kit; safe to delete)
```

---

## 🧭 Suggested delivery plan (1-day faculty session)

| Slot | Topic | Material |
|---|---|---|
| 09:00 | Course overview + exam structure | Deck 0 |
| 09:30 | AI concepts & AI in Azure (Foundry, endpoints) | Deck 1 → Quiz 1A |
| 10:45 | Generative AI & agents | Deck 2 → Quiz 2A |
| 12:00 | *Lunch* | |
| 13:00 | NLP & text analysis | Deck 3 → Quiz 3A |
| 14:00 | Speech | Deck 4 → Quiz 4A |
| 15:00 | Computer vision | Deck 5 → Quiz 5A |
| 16:00 | Information extraction | Deck 6 → Quiz 6A |
| 17:00 | Final mock exam 1 (timed) + review | Portal |

Use the **B quizzes** and **mock exam 2** as homework / next-day reinforcement.

---

## 🔗 Official references (public Microsoft Learn)

- Course collection: <https://aka.ms/mslearn-ai-901>
- AI concepts: <https://aka.ms/mslearn-ai-concepts> · Get started with AI in Azure: <https://aka.ms/mslearn-get-started-azure-ai>
- Generative AI & agents: <https://aka.ms/mslearn-intro-gen-ai> · <https://aka.ms/mslearn-get-started-gen-ai-agents>
- NLP: <https://aka.ms/mslearn-nlp-concepts> · <https://aka.ms/mslearn-get-started-ai-text>
- Speech: <https://aka.ms/mslearn-ai-speech-concepts> · <https://aka.ms/mslearn-get-started-ai-speech>
- Vision: <https://aka.ms/mslearn-ai-vision-concepts> · <https://aka.ms/mslearn-get-started-ai-vision>
- Information extraction: <https://aka.ms/mslearn-ai-info-concepts> · <https://aka.ms/mslearn-get-started-information-extraction>
- Certifications home: <https://learn.microsoft.com/certifications>

---

*Maintained by Aryan Tripathi (MCT). Original educational content — no Microsoft courseware
material is included in this repository.*
