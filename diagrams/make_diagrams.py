"""Generate the original SVG diagram set for the AI-901 study kit.

Run:  python make_diagrams.py
All diagrams are original works created for this kit.
"""
import html
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- palette -------------------------------------------------------------
BLUE = "#0b5cab"; BLUE_L = "#e8f1fb"; INK = "#16324f"; GREY = "#5b6b7b"
PURPLE = "#7a3ee8"; PURPLE_L = "#f3ecfe"; GREEN = "#107c10"; GREEN_L = "#e6f4e6"
ORANGE = "#c74e0c"; ORANGE_L = "#fdeee3"; TEAL = "#038387"; TEAL_L = "#e3f5f5"
FONT = "Segoe UI, Arial, sans-serif"


def esc(s):
    return html.escape(str(s), quote=True)


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}" role="img" aria-label="{esc(title)}">',
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GREY}"/></marker></defs>',
            f'<text x="{w/2}" y="34" text-anchor="middle" font-size="22" '
            f'font-weight="600" fill="{INK}">{esc(title)}</text>',
        ]

    def rect(self, x, y, w, h, fill=BLUE_L, stroke=BLUE, rx=10, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=15, fill=INK, anchor="middle", weight="normal"):
        self.parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{esc(s)}</text>')

    def lines(self, x, y, items, size=13, fill=GREY, lh=19, anchor="middle"):
        for i, s in enumerate(items):
            self.text(x, y + i * lh, s, size=size, fill=fill, anchor=anchor)

    def arrow(self, x1, y1, x2, y2, label=None):
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREY}" '
            'stroke-width="2.2" marker-end="url(#arr)"/>')
        if label:
            self.text((x1 + x2) / 2, min(y1, y2) - 8, label, size=12, fill=GREY)

    def save(self, name):
        self.parts.append("</svg>")
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write("\n".join(self.parts))
        print("wrote", name)


def step_flow(svg, y, steps, x0=40, gap=28, box_h=110, colors=None):
    """Row of numbered step boxes with arrows."""
    n = len(steps)
    total_gap = gap * (n - 1)
    bw = (svg.w - 2 * x0 - total_gap) / n
    for i, (title, subs) in enumerate(steps):
        x = x0 + i * (bw + gap)
        c_fill, c_stroke = (colors[i] if colors else (BLUE_L, BLUE))
        svg.rect(x, y, bw, box_h, fill=c_fill, stroke=c_stroke)
        svg.parts.append(
            f'<circle cx="{x+21}" cy="{y+23}" r="12" fill="{c_stroke}"/>')
        svg.text(x + 21, y + 28, str(i + 1), size=13, fill="#fff", weight="600")
        svg.text(x + 40, y + 28, title, size=14, weight="600", anchor="start")
        svg.lines(x + bw / 2, y + 54, subs, size=12)
        if i < n - 1:
            svg.arrow(x + bw + 3, y + box_h / 2, x + bw + gap - 3, y + box_h / 2)


# ===========================================================================
# 1. Azure hierarchy
s = SVG(900, 460, "Microsoft Azure: organizational hierarchy")
s.rect(60, 60, 780, 370, fill="#f4f8fd")
s.text(140, 90, "Tenant", 17, BLUE, weight="600")
s.text(640, 90, "Security boundary — identities via Microsoft Entra ID", 13, GREY)
s.rect(100, 110, 700, 290, fill="#eef5fc")
s.text(200, 140, "Subscription", 16, BLUE, weight="600")
s.text(620, 140, "Billing boundary", 13, GREY)
s.rect(140, 160, 620, 210, fill="#e8f1fb")
s.text(265, 190, "Resource group", 15, BLUE, weight="600")
s.text(600, 190, "Organization & management", 13, GREY)
for i, (nm, sub) in enumerate([("Microsoft Foundry", "AI apps & agents"),
                               ("App Service", "Web apps"),
                               ("Storage / SQL", "Data services")]):
    x = 180 + i * 190
    s.rect(x, 215, 170, 120, fill="#ffffff")
    s.text(x + 85, 265, nm, 14, INK, weight="600")
    s.text(x + 85, 290, sub, 12, GREY)
s.text(450, 425, "Resources = infrastructure & application services — the building blocks of solutions", 13, GREY)
s.save("azure-hierarchy.svg")

# 2. Foundry structure
s = SVG(900, 460, "Microsoft Foundry: resource, project, and assets")
s.rect(70, 60, 760, 360, fill=PURPLE_L, stroke=PURPLE)
s.text(230, 92, "Microsoft Foundry resource", 16, PURPLE, weight="600")
s.text(640, 92, "Compute · storage · model delivery", 13, GREY)
s.rect(110, 110, 680, 290, fill="#ffffff", stroke=PURPLE, dash="6 5")
s.text(260, 140, "Microsoft Foundry project", 15, PURPLE, weight="600")
s.text(620, 140, "Isolated work environment", 13, GREY)
tiles = [("Models", "Choose & deploy from the model catalog"),
         ("Agents", "Create & manage agents that use models"),
         ("Tools", "Actions & information access for agents"),
         ("Knowledge", "Data sources that ground agent responses")]
for i, (nm, sub) in enumerate(tiles):
    x = 145 + (i % 2) * 310; y = 165 + (i // 2) * 110
    s.rect(x, y, 290, 95, fill=BLUE_L)
    s.text(x + 145, y + 38, nm, 15, BLUE, weight="600")
    s.lines(x + 145, y + 62, [sub], size=12)
s.save("foundry-structure.svg")

# 3. Foundry endpoint
s = SVG(900, 430, "Foundry endpoints: how applications call models and services")
s.rect(50, 90, 230, 260, fill=GREEN_L, stroke=GREEN)
s.text(165, 125, "Client application", 15, GREEN, weight="600")
s.lines(165, 152, ["Uses an SDK (Python, C#, …)", "that wraps the REST API"], size=12.5)
s.rect(90, 210, 150, 110, fill="#ffffff", stroke=GREEN)
s.text(165, 250, "< SDK >", 15, GREEN, weight="600")
s.lines(165, 275, ["OpenAI / Azure", "client libraries"], size=12)
s.rect(620, 90, 230, 260, fill=BLUE_L)
s.text(735, 125, "Foundry endpoint", 15, BLUE, weight="600")
s.lines(735, 152, ["HTTPS address of a", "deployed model or service"], size=12.5)
s.rect(660, 210, 150, 110, fill="#ffffff")
s.text(735, 245, "Auth", 14, BLUE, weight="600")
s.lines(735, 268, ["API key, or", "Microsoft Entra ID token"], size=12)
s.arrow(285, 170, 615, 170, "Request — JSON body + headers")
s.arrow(615, 285, 285, 285, "Response — JSON results + headers")
s.text(450, 395, "Endpoint = where to call  ·  Key/token = proof you may call it", 14, GREY)
s.save("foundry-endpoint.svg")

# 4. AI workloads
s = SVG(900, 430, "Common AI workloads")
tiles = [("Generative AI & agents", "Create content; act on a user's behalf", BLUE_L, BLUE),
         ("Text & language", "Infer meaning from written language", TEAL_L, TEAL),
         ("Computer speech", "Recognize & synthesize spoken language", PURPLE_L, PURPLE),
         ("Computer vision", "Interpret images and video", GREEN_L, GREEN),
         ("Information extraction", "Turn documents & media into data", ORANGE_L, ORANGE)]
for i, (nm, sub, f, st) in enumerate(tiles):
    x = 40 + i * 168
    s.rect(x, 75, 152, 190, fill=f, stroke=st)
    words = nm.split(" ")
    mid = (len(words) + 1) // 2
    s.text(x + 76, 115, " ".join(words[:mid]), 14, st, weight="600")
    s.text(x + 76, 135, " ".join(words[mid:]), 14, st, weight="600")
    line1, line2 = sub[:24], sub[24:]
    import textwrap
    wrapped = textwrap.wrap(sub, 20)
    s.lines(x + 76, 170, wrapped, size=11.5)
s.rect(40, 295, 820, 95, fill="#10324f", stroke="#10324f")
s.text(450, 335, "Machine learning   —   f(x) = y", 17, "#ffffff", weight="600")
s.text(450, 362, "Models trained on historic data underpin every AI workload", 13, "#cfe0f0")
s.save("ai-workloads.svg")

# 5. Responsible AI
s = SVG(900, 400, "Microsoft's six principles of responsible AI")
pr = [("Fairness", "Treat all people equitably; avoid bias in data & predictions"),
      ("Reliability & safety", "Operate within defined limits; test rigorously"),
      ("Privacy & security", "Protect data used for training and inference"),
      ("Inclusiveness", "Empower everyone, including all abilities"),
      ("Transparency", "Make purpose, behavior & limits understandable"),
      ("Accountability", "People remain answerable for AI systems")]
for i, (nm, sub) in enumerate(pr):
    x = 55 + (i % 3) * 275; y = 70 + (i // 3) * 155
    s.rect(x, y, 250, 135, fill=BLUE_L)
    s.text(x + 125, y + 35, nm, 15.5, BLUE, weight="600")
    import textwrap
    s.lines(x + 125, y + 62, textwrap.wrap(sub, 30), size=12)
s.save("responsible-ai.svg")

# 6. Transformer / embeddings
s = SVG(900, 440, "How language models work: tokens, embeddings, attention")
step_flow(s, 90, [
    ("Tokenization", ["Text is split into", "tokens (words /", "word-parts)"]),
    ("Embeddings", ["Each token becomes a", "vector that captures", "semantic meaning"]),
    ("Attention", ["Weights relate every", "token to the tokens", "around it in context"]),
    ("Prediction", ["Model computes the", "most probable", "next token"]),
], box_h=130)
s.rect(60, 260, 780, 150, fill="#f7f9fc", stroke=GREY, dash="5 5")
s.text(450, 292, "Vector space intuition", 14.5, INK, weight="600")
s.lines(450, 318, [
    'Semantically similar tokens point in similar directions:  "dog" ≈ "puppy",  "cat" ≈ "kitten"',
    'Vector arithmetic captures relationships:  dog + young ≈ puppy',
    "LLMs use the transformer architecture; SLMs are compact versions for constrained devices"], size=13, lh=24)
s.save("transformer-embeddings.svg")

# 7. Agent anatomy
s = SVG(900, 450, "Anatomy of an AI agent")
s.rect(60, 100, 240, 280, fill=BLUE_L)
s.text(180, 140, "Agent", 18, BLUE, weight="600")
s.lines(180, 170, ["Autonomous, action-capable", "AI assistant that works with", "users and with other agents"], size=12.5)
comps = [("Model", "Language understanding & reasoning", PURPLE_L, PURPLE),
         ("Instructions", "Define behavior, scope & tone", TEAL_L, TEAL),
         ("Tools", "Capabilities the agent can invoke", ORANGE_L, ORANGE)]
for i, (nm, sub, f, st) in enumerate(comps):
    y = 95 + i * 100
    s.rect(400, y, 260, 82, fill=f, stroke=st)
    s.text(530, y + 32, nm, 14.5, st, weight="600")
    import textwrap
    s.lines(530, y + 54, textwrap.wrap(sub, 30), size=11.5)
    s.arrow(305, 240, 395, y + 41)
s.rect(710, 150, 160, 90, fill="#ffffff", stroke=ORANGE)
s.text(790, 185, "Knowledge", 13.5, ORANGE, weight="600")
s.lines(790, 206, ["Ground answers", "in data sources"], size=11.5)
s.rect(710, 260, 160, 90, fill="#ffffff", stroke=ORANGE)
s.text(790, 295, "Actions", 13.5, ORANGE, weight="600")
s.lines(790, 316, ["Automate tasks via", "connected services"], size=11.5)
s.arrow(665, 305, 705, 220)
s.arrow(665, 320, 705, 300)
s.save("agent-anatomy.svg")

# 8. NLP pre-processing pipeline
s = SVG(900, 330, "Text pre-processing pipeline")
step_flow(s, 80, [
    ("Tokenization", ["Split text", "into words"]),
    ("Normalization", ["Lower-case;", "strip punctuation"]),
    ("Stop-word removal", ['Drop noise words', '("the", "a", "and")']),
    ("Stemming /", ["lemmatization —", "consolidate roots"]),
    ("POS tagging", ["Label verbs,", "nouns, adjectives"]),
], box_h=115)
s.text(450, 250, 'Example: "We choose to go to the Moon!"  →  choose (V) · go (V) · moon (N)', 14, GREY)
s.text(450, 285, "Prepared tokens feed statistical analysis or are vectorized for semantic models", 13, GREY)
s.save("nlp-pipeline.svg")

# 9. Text analysis — choosing the right method
s = SVG(900, 460, "Text analysis in Foundry: choosing the right method")
s.rect(60, 70, 370, 320, fill=BLUE_L)
s.text(245, 105, "General-purpose AI models", 15.5, BLUE, weight="600")
s.text(245, 128, "(prompt an LLM, e.g. gpt-4.1-mini)", 12.5, GREY)
s.lines(245, 158, ["✓ Flexible, conversational analysis", "✓ Multiple tasks in one call",
                   "✓ Natural-language responses", "✓ Exploratory workflows", "",
                   "✗ Probabilistic — results can vary", "   between identical calls"], size=13, lh=24)
s.rect(470, 70, 370, 320, fill=GREEN_L, stroke=GREEN)
s.text(655, 105, "Azure Language (Foundry Tools)", 15.5, GREEN, weight="600")
s.text(655, 128, "(dedicated prebuilt service + SDK)", 12.5, GREY)
s.lines(655, 158, ["✓ Deterministic, structured output", "✓ Confidence scores per result",
                   "✓ Production pipelines at scale", "✓ PII detection for regulated data",
                   "✓ Language detection, NER, health", "", "Strength: reproducible results"],
        size=13, lh=24)
s.text(450, 425, "Same input → same output needed?  Pick Azure Language.  Flexibility needed?  Prompt a model.", 13.5, GREY)
s.save("text-analysis-methods.svg")

# 10. Speech recognition
s = SVG(900, 330, "Speech recognition (speech-to-text) pipeline")
step_flow(s, 80, [
    ("Audio capture", ["Analog signal →", "digital waveform"]),
    ("Pre-processing", ["Extract feature", "vectors (frequency", "intensities)"]),
    ("Acoustic model", ["Map features to", "phonemes (smallest", "units of sound)"]),
    ("Language model", ["Most probable word", 'sequence: "nice to', 'be here" not "nights…"']),
    ("Post-processing", ["Normalize &", "format the text"]),
], box_h=120)
s.text(450, 255, 'Output: transcribed text — used for captions, transcription, voice assistants', 13.5, GREY)
s.save("speech-recognition.svg")

# 11. Speech synthesis
s = SVG(900, 330, "Speech synthesis (text-to-speech) pipeline")
step_flow(s, 80, [
    ("Source text", ["Document content", "or app/model", "output"]),
    ("Normalization", ["Expand Dr. → doctor,", "3:00pm → three", "o'clock P M"]),
    ("Linguistic model", ["Map normalized", "text to phonemes"]),
    ("Prosody", ["Pitch, rhythm &", "timbre for natural", "pronunciation"]),
    ("Waveform", ["Encode digital", "audio output"]),
], box_h=120, colors=[(PURPLE_L, PURPLE)] * 5)
s.text(450, 255, "Output: spoken audio — used by assistants, screen readers, alerts, e-learning", 13.5, GREY)
s.save("speech-synthesis.svg")

# 12. Vision tasks
s = SVG(900, 440, "Computer vision tasks")
t = [("Image classification", ["Assign a single label to the", 'whole image: "apple"']),
     ("Object detection", ["Locate each object with a", "bounding box + class label"]),
     ("Semantic segmentation", ["Classify every pixel —", "exact object outlines"]),
     ("Contextual image analysis", ["Describe the scene:", '"a person eating an apple"'])]
for i, (nm, sub) in enumerate(t):
    x = 70 + (i % 2) * 390; y = 70 + (i // 2) * 170
    s.rect(x, y, 360, 150, fill=GREEN_L, stroke=GREEN)
    s.text(x + 180, y + 40, nm, 15.5, GREEN, weight="600")
    s.lines(x + 180, y + 70, sub, size=13, lh=22)
s.text(450, 420, "All manipulate and analyze pixel values, increasingly via multimodal models", 13.5, GREY)
s.save("vision-tasks.svg")

# 13. CNN vs ViT
s = SVG(900, 470, "Computer vision models: CNN vs Vision Transformer")
s.rect(55, 70, 385, 330, fill=BLUE_L)
s.text(247, 103, "Convolutional Neural Network (CNN)", 15, BLUE, weight="600")
s.lines(247, 135, ["1. Train on labeled images", "2. Filters extract numeric features",
                   "3. Feature maps are flattened", "4. Fully-connected layers predict class",
                   "5. Output = probability per class"], size=13, lh=26, anchor="middle")
s.text(247, 300, "Classic approach for image", 12.5, GREY)
s.text(247, 320, "classification tasks", 12.5, GREY)
s.rect(460, 70, 385, 330, fill=PURPLE_L, stroke=PURPLE)
s.text(652, 103, "Vision Transformer (ViT)", 15, PURPLE, weight="600")
s.lines(652, 135, ["1. Image split into patches", "2. Patches → embedding vectors",
                   "3. Attention encodes visual relationships", "4. Cross-modal attention combines vision",
                   "    + language vector spaces"], size=13, lh=26)
s.text(652, 300, "Foundation of multimodal models that", 12.5, GREY)
s.text(652, 320, "accept both images and text", 12.5, GREY)
s.text(450, 440, "Multimodal models let you prompt with an image + a question in a single request", 13.5, GREY)
s.save("cnn-vit.svg")

# 14. Diffusion
s = SVG(900, 330, "Diffusion models: how images are generated")
step_flow(s, 80, [
    ("Training", ["Add visual noise to", "labeled images,", "step by step"]),
    ("Learning", ["Model learns how", "noise changes an", "image + its label"]),
    ("Generation", ["Start from random", "pixels (pure noise)"]),
    ("Denoising", ["Iteratively remove", "noise guided by", "the text prompt"]),
    ("Output", ["Novel image that", "matches the", "description"]),
], box_h=120, colors=[(GREEN_L, GREEN)] * 5)
s.text(450, 255, "Video generation (e.g. sora models) runs as an asynchronous job — poll until complete", 13.5, GREY)
s.save("diffusion.svg")

# 15. OCR pipeline
s = SVG(900, 330, "Optical Character Recognition (OCR) pipeline")
step_flow(s, 80, [
    ("Acquisition", ["Scan / photo /", "PDF input"]),
    ("Pre-processing", ["Enhance image;", "deskew, denoise"]),
    ("Region detection", ["Find areas that", "contain text"]),
    ("Recognition", ["Classify individual", "characters & words"]),
    ("Output", ["Machine-readable", "text + positions"]),
], box_h=120, colors=[(ORANGE_L, ORANGE)] * 5)
s.text(450, 255, "OCR reads the text; field extraction gives that text business meaning", 13.5, GREY)
s.save("ocr-pipeline.svg")

# 16. Field extraction
s = SVG(900, 330, "Field extraction & mapping (Azure Content Understanding)")
step_flow(s, 80, [
    ("Ingest OCR", ["Raw recognized", "text + layout"]),
    ("Detect fields", ["Find candidate", "values (dates,", "totals, names)"]),
    ("Map to schema", ["Associate values", "with defined fields", "(analyzer schema)"]),
    ("Normalize", ["Standardize formats:", "$20 → 20.00,", "01/01 → 2025-01-01"]),
    ("Integrate", ["JSON results feed", "business systems", "via REST API"]),
], box_h=120, colors=[(TEAL_L, TEAL)] * 5)
s.text(450, 255, "Predefined analyzers for invoices/receipts; custom analyzers from your own sample schema", 13.5, GREY)
s.save("field-extraction.svg")

print("done")
