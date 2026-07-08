"""Build the seven AI-901 PowerPoint decks (original content) with python-pptx.

Run:  python build_pptx.py
"""
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.abspath(os.path.join(HERE, "..", "diagrams", "png"))

BLUE = RGBColor(0x0B, 0x5C, 0xAB)
INK = RGBColor(0x16, 0x32, 0x4F)
GREY = RGBColor(0x5B, 0x6B, 0x7B)
LIGHT = RGBColor(0xE8, 0xF1, 0xFB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Segoe UI"

SW, SH = Inches(13.333), Inches(7.5)  # 16:9


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = SW, SH
        self.blank = self.prs.slide_layouts[6]

    # ---- primitives ------------------------------------------------------
    def _slide(self, bg=WHITE):
        s = self.prs.slides.add_slide(self.blank)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = bg
        return s

    def _box(self, s, x, y, w, h):
        tb = s.shapes.add_textbox(x, y, w, h)
        tb.text_frame.word_wrap = True
        return tb.text_frame

    def _bar(self, s, y=Inches(1.28)):
        from pptx.enum.shapes import MSO_SHAPE
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), y,
                                 Inches(3.2), Pt(4))
        bar.fill.solid(); bar.fill.fore_color.rgb = BLUE
        bar.line.fill.background()

    def _title(self, s, text, size=32, color=INK):
        tf = self._box(s, Inches(0.55), Inches(0.45), SW - Inches(1.1), Inches(0.9))
        p = tf.paragraphs[0]; r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.bold = True
        r.font.color.rgb = color; r.font.name = FONT
        self._bar(s)

    # ---- slide types -----------------------------------------------------
    def title_slide(self, kicker, title, subtitle):
        s = self._slide(bg=RGBColor(0x0E, 0x22, 0x3B))
        tf = self._box(s, Inches(0.9), Inches(2.1), SW - Inches(1.8), Inches(3.4))
        for text, size, bold, col in [(kicker, 16, False, RGBColor(0x9F, 0xC4, 0xE8)),
                                      (title, 44, True, WHITE),
                                      (subtitle, 18, False, RGBColor(0xC9, 0xDC, 0xF0))]:
            p = tf.add_paragraph(); r = p.add_run(); r.text = text
            r.font.size = Pt(size); r.font.bold = bold
            r.font.color.rgb = col; r.font.name = FONT
            p.space_after = Pt(14)
        note = self._box(s, Inches(0.9), Inches(6.6), SW - Inches(1.8), Inches(0.6))
        p = note.paragraphs[0]; r = p.add_run()
        r.text = "AI-901 Faculty Study Kit · original content from public Microsoft Learn documentation"
        r.font.size = Pt(11); r.font.color.rgb = RGBColor(0x7E, 0x9A, 0xB8); r.font.name = FONT
        return s

    def bullets(self, title, items, size=19):
        s = self._slide()
        self._title(s, title)
        tf = self._box(s, Inches(0.75), Inches(1.65), SW - Inches(1.5), SH - Inches(2.2))
        first = True
        for it in items:
            lvl, text = (it if isinstance(it, tuple) else (0, it))
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.level = lvl
            r = p.add_run(); r.text = ("• " if lvl == 0 else "– ") + text
            r.font.size = Pt(size if lvl == 0 else size - 3)
            r.font.color.rgb = INK if lvl == 0 else GREY
            r.font.name = FONT
            p.space_after = Pt(10 if lvl == 0 else 5)
        return s

    def image(self, title, png_name, caption=None):
        s = self._slide()
        self._title(s, title)
        path = os.path.join(PNG, png_name)
        from PIL import Image  # pillow ships with python-pptx installs commonly; fallback below
        try:
            iw, ih = Image.open(path).size
        except Exception:
            iw, ih = 1800, 880
        max_w, max_h = SW - Inches(1.2), SH - Inches(2.4)
        scale = min(max_w / iw, max_h / ih)
        w, h = int(iw * scale), int(ih * scale)
        s.shapes.add_picture(path, int((SW - w) / 2), Inches(1.55) + int((max_h - h) / 2), w, h)
        if caption:
            tf = self._box(s, Inches(0.75), SH - Inches(0.75), SW - Inches(1.5), Inches(0.5))
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = caption
            r.font.size = Pt(13); r.font.italic = True
            r.font.color.rgb = GREY; r.font.name = FONT
        return s

    def closing(self, points, next_step):
        s = self.bullets("Summary & exam pointers", points)
        tf = self._box(s, Inches(0.75), SH - Inches(0.85), SW - Inches(1.5), Inches(0.6))
        p = tf.paragraphs[0]; r = p.add_run(); r.text = "➜ " + next_step
        r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = BLUE; r.font.name = FONT
        return s

    def save(self, name):
        out = os.path.join(HERE, name)
        self.prs.save(out)
        print("wrote", name)


# ===========================================================================
# Deck 0 — course overview
d = Deck()
d.title_slide("AI-901 · INTRODUCTION TO AI IN AZURE", "Course Overview",
              "What we cover, how the exam works, and how to use this kit")
d.bullets("About this course", [
    "Builds awareness of common AI workloads and how Microsoft Foundry supports them in Azure",
    "Aimed at everyone — not just data scientists or professional developers",
    "Six modules: AI in Azure · Generative AI & agents · Text analysis · Speech · Computer vision · Information extraction",
    "Each module pairs concepts (how it works) with implementation (how to build it in Foundry)",
    "Official learning content: https://aka.ms/mslearn-ai-901"])
d.bullets("Exam AI-901 at a glance", [
    "Two skill areas measured:",
    (1, "Identify AI concepts and capabilities — ~40% of questions"),
    (1, "Implement AI solutions with Microsoft Foundry — ~60% of questions"),
    "Prepare with: study guide, exam prep videos, the exam sandbox, and practice assessments",
    "Fundamentals certifications do not expire",
    "This kit adds 12 section quizzes + 2 full timed mock exams (see index.html)"])
d.bullets("How to use this kit", [
    "Read the module notes (modules/ folder) — every diagram is in the deck and the PDF too",
    "Present decks 1–6 in order; each ends with exam pointers",
    "After each module, run the matching 30-question quiz (portal, timed, explanations included)",
    "Finish with the two 45-question mixed mock exams under real-exam timing",
    "Complete course PDF: pdf/AI-901-Complete-Course.pdf for offline study"])
d.closing([
    "AI-901 replaces the retired AI-900 focus with a Microsoft Foundry-centric syllabus",
    "60% of the exam is implementation — hands-on Foundry familiarity matters",
    "Every module in this kit maps 1:1 to an official Microsoft Learn path"],
    "Start with Module 1 — AI concepts & getting started with AI in Azure")
d.save("AI901-00-Course-Overview.pptx")

# Deck 1 — AI concepts & Azure
d = Deck()
d.title_slide("MODULE 1", "AI Concepts & Getting Started with AI in Azure",
              "Workloads · Responsible AI · Azure · Microsoft Foundry · Endpoints")
d.bullets("What is artificial intelligence?", [
    "Software that imitates human capabilities:",
    (1, "predict outcomes and recognize patterns from historic data"),
    (1, "evaluate content, make decisions, take appropriate action"),
    (1, "understand language and hold conversations"),
    (1, "interpret visual input"),
    (1, "extract information from sources to gain knowledge"),
    "Machine learning — models mapping input to output, f(x) = y — underpins all of it"])
d.image("Five common AI workloads", "ai-workloads.png",
        "Generative AI & agents · text & language · speech · vision · information extraction")
d.image("Responsible AI — six principles", "responsible-ai.png",
        "Fairness · Reliability & safety · Privacy & security · Inclusiveness · Transparency · Accountability")
d.bullets("Responsible AI — scenario keywords", [
    "Bias against a group of people → Fairness",
    "Rigorous testing; safe operation within limits → Reliability & safety",
    "Personal / sensitive data protection → Privacy & security",
    "Serving people of all abilities → Inclusiveness",
    "Users understand purpose, behavior, limitations → Transparency",
    "Humans remain answerable; governance & override → Accountability"])
d.image("Microsoft Azure — organizational hierarchy", "azure-hierarchy.png",
        "Tenant (security, Entra ID) → Subscription (billing) → Resource group → Resources")
d.image("Microsoft Foundry — resource, project & assets", "foundry-structure.png",
        "Projects are isolated work environments containing Models, Agents, Tools and Knowledge")
d.bullets("Foundry is built on Azure", [
    "Foundry uses Azure compute, networking, identity and security to host AI applications",
    "It does not run independently of Azure, and it does not replace Azure services",
    "A Foundry resource provides compute, storage and model delivery",
    "Projects isolate development work; assets = models, agents, tools, knowledge"])
d.image("Endpoints, keys and SDKs", "foundry-endpoint.png",
        "Endpoint = URL to call a deployed model · key or Entra ID token authenticates the request")
d.closing([
    "Tenant = security boundary; subscription = billing boundary",
    "Generative AI = language model creating original content from a prompt",
    "AI agent = an application that performs tasks on behalf of a user",
    "Endpoint answers 'where'; key/token answers 'may I' — keys never store data"],
    "Next: Module 2 — Generative AI and agents")
d.save("AI901-01-AI-Concepts-and-Azure.pptx")

# Deck 2 — GenAI & agents
d = Deck()
d.title_slide("MODULE 2", "Generative AI and Agents",
              "LLMs · transformers · model catalog · playgrounds · Foundry Agent Service")
d.bullets("What is generative AI?", [
    "Generates responses from natural-language prompts",
    "Output types: natural language (text/speech), images & video, code (Python, C#, SQL, …)",
    "Applications: smart chatbots, creative assistants, and the foundation for agentic AI",
    "Powered by large language models (LLMs); small language models (SLMs) fit devices and constrained environments"])
d.image("How language models work", "transformer-embeddings.png",
        "Transformer architecture: tokens → embeddings → attention → next-token prediction")
d.bullets("Transformer vocabulary — exam anchors", [
    "Token — unit of text (word / word-part) the model processes",
    "Embedding — vector representation of a token capturing semantic meaning",
    "Attention — weighs relationships between each token and the tokens around it",
    "Semantically similar tokens have similar vector directions (dog + young ≈ puppy)",
    "The model repeatedly predicts the most probable next token"])
d.image("What are agents?", "agent-anatomy.png",
        "Model + instructions + tools — tools provide knowledge (grounding) and actions (automation)")
d.bullets("Foundry Models — the catalog", [
    "Central hub to discover, filter, compare and deploy models from multiple providers",
    "Sold directly by Microsoft (billed via your Azure subscription) — includes Azure OpenAI models",
    "Partner & community models from trusted third-party providers",
    "Deployment considerations:",
    (1, "Deployment type — where data is processed and how you pay"),
    (1, "Version — model version and auto-update policy"),
    (1, "Rate limits — maximum tokens-per-minute (TPM)"),
    (1, "Guardrails — responsible-AI content policies")])
d.bullets("Using a generative model", [
    "Model playground — test prompts, compare models, capture working settings before coding",
    "OpenAI-compatible APIs / SDKs — consume the model from application code",
    "Shape behavior with three levers:",
    (1, "Instructions (system prompt) — context and guidelines"),
    (1, "Input (user prompt) — explicit, detailed requests"),
    (1, "Parameters — temperature ('creativity'), response length"),
    "Pattern: OpenAI(base_url=endpoint, api_key=key) → client.responses.create(model=deployment, input=prompt)"])
d.bullets("Creating agents — Foundry Agent Service", [
    "Save a model configuration as a named agent, or build one directly",
    "Add tools — knowledge (file search, web, data) and actions (connected services, code)",
    "Experiment and test in the agent playground",
    "Connect from code with the Foundry Project API:",
    (1, "AIProjectClient(endpoint, DefaultAzureCredential()) — project connection"),
    (1, "project.agents.get('name') — fetch the agent definition"),
    (1, "openai_client.responses.create(input=…, extra_body={'agent': …}) — THIS submits the prompt")])
d.closing([
    "LLM = model designed to generate human-like text; embeddings = semantic vectors",
    "Playground helps you experiment — it does not replace deployment or the API",
    "Know all four deployment considerations: type, version, rate limits, guardrails",
    "responses.create() is the line that actually sends a prompt to a model or agent"],
    "Next: Module 3 — NLP & text analysis")
d.save("AI901-02-Generative-AI-and-Agents.pptx")

# Deck 3 — NLP
d = Deck()
d.title_slide("MODULE 3", "Natural Language Processing & Text Analysis",
              "NLP tasks · pre-processing · statistical vs semantic · Azure Language")
d.bullets("What is NLP?", [
    "Inferring meaning from text",
    "Core tasks: key-term extraction, named entity recognition, text classification (incl. sentiment), summarization",
    "Azure Language adds: PII extraction & redaction, language detection, Text Analytics for Health",
    "Use cases: search indexing, PII redaction, chatbot intent prediction, spam filtering, social media analysis"])
d.image("Text pre-processing pipeline", "nlp-pipeline.png",
        "Tokenization → normalization → stop-word removal → stemming/lemmatization → POS tagging")
d.bullets("Statistical text analysis", [
    "Term Frequency (TF) — the most common tokens indicate key topics",
    "TF-IDF — importance of a word in one document relative to the whole collection",
    "Bag-of-Words — word-set frequencies drive classification (happy/great/fantastic → positive)",
    "TextRank — sentence relevance scoring (PageRank idea); powers extractive summarization",
    "Semantic models vectorize tokens as embeddings — the basis of modern LLMs"])
d.image("Choosing the right method in Foundry", "text-analysis-methods.png",
        "Flexible prompting vs deterministic structured output with confidence scores")
d.bullets("Azure Language SDK — the pattern", [
    "TextAnalyticsClient(endpoint, AzureKeyCredential(key)) — the client object lets code talk to the service",
    "Submit a collection of documents for analysis",
    "detect_language() → language name + ISO 639-1 code + confidence score",
    "recognize_pii_entities() → redacted text + entities + confidence per entity",
    "recognize_entities(), extract_key_phrases(), analyze_sentiment()",
    "Deterministic: the same input returns the same structured result"])
d.bullets("Azure Language in an agent (MCP)", [
    "Model Context Protocol (MCP) exposes Azure Language capabilities to agents as tools",
    "Connect the MCP server to your agent — specify the Foundry resource and credentials",
    "Approve tool access: one-time, always for this tool, or always for all tools",
    "The MCP server complements the agent's model — it does not replace it"])
d.closing([
    "TF-IDF = importance of a word in a document vs the collection",
    "Deterministic structured output + confidence scores → Azure Language, not an LLM prompt",
    "PII redaction for regulated data is an Azure Language strength",
    "MCP = the bridge that lets agents call Azure Language"],
    "Next: Module 4 — AI speech")
d.save("AI901-03-NLP-and-Text-Analysis.pptx")

# Deck 4 — Speech
d = Deck()
d.title_slide("MODULE 4", "AI Speech",
              "Speech-to-text · text-to-speech · Speech SDK · Voice Live agents")
d.bullets("Speech-enabled solutions", [
    "Speech recognition = speech-to-text (STT): audio file / stream / microphone → transcription",
    (1, "Customer support, voice assistants, automatic subtitles, meeting transcription, clinical notes"),
    "Speech synthesis = text-to-speech (TTS): text → audio waveform",
    (1, "Conversational AI, screen readers, notifications, e-learning, game character voices"),
    "Accessibility appears on both sides: captions = STT, screen readers = TTS"])
d.image("Speech recognition pipeline", "speech-recognition.png",
        "Capture → feature extraction → acoustic model (phonemes) → language model (words) → post-processing")
d.image("Speech synthesis pipeline", "speech-synthesis.png",
        "Text → normalization → phonemes → prosody (natural cadence) → waveform encoding")
d.bullets("Pipeline vocabulary — exam anchors", [
    "Pre-processing extracts feature vectors from the waveform (noise removed, never added)",
    "Phoneme — the smallest unit of sound in speech",
    "Acoustic model maps features → phonemes; language model picks the most probable words",
    "Normalization (TTS) expands 'Dr.' → 'doctor', '3:00pm' → 'three o'clock P M'",
    "Prosody = pitch, rhythm, timbre → natural pronunciation and cadence (not volume, not translation)"])
d.bullets("Azure Speech in Foundry Tools", [
    "Portal playground — real-time transcription, language ID, speaker diarization; voice tuning for TTS",
    "Azure Speech SDK — put speech recognition/synthesis directly into application code",
    (1, "STT: SpeechConfig(key, endpoint) + AudioConfig(file) → SpeechRecognizer → recognize_once_async()"),
    (1, "TTS: set speech_synthesis_voice_name → SpeechSynthesizer → speak_text_async()"),
    (1, "No AudioConfig needed for default speaker output (use one for file output)"),
    "SDK handles authentication, network communication and audio generation",
    "MCP server exposes speech capabilities to agents"])
d.bullets("Voice Live — speech-capable agents", [
    "Real-time spoken conversation with a generative model that has instructions and tools",
    "Continuous conversation flow with interruption handling and background-noise reduction",
    "Experiment in the Foundry portal playground",
    "Build clients with the Voice Live SDK (azure-ai-voicelive): opens a real-time connection, streams audio, handles spoken responses & interruptions"])
d.closing([
    "STT pipeline order: capture → features → acoustic → language → post-processing",
    "Phonemes = smallest units of sound; prosody = natural cadence",
    "SDK vs playground: the SDK is how speech gets into your application code",
    "Voice Live = real-time voice agents with interruption support"],
    "Next: Module 5 — Computer vision")
d.save("AI901-04-AI-Speech.pptx")

# Deck 5 — Vision
d = Deck()
d.title_slide("MODULE 5", "Computer Vision",
              "Vision tasks · CNNs & ViTs · multimodal analysis · image & video generation")
d.image("Computer vision tasks", "vision-tasks.png",
        "Classification (one label) · detection (boxes) · segmentation (pixels) · contextual analysis (description)")
d.bullets("Vision fundamentals", [
    "Computer vision manipulates and analyzes pixel values — not metadata or file names",
    "Classification: one label for the whole image",
    "Object detection: bounding box + class for each object",
    "Semantic segmentation: classify every pixel — exact outlines",
    "Contextual analysis: natural-language description of the scene"])
d.image("Vision models — CNN vs Vision Transformer", "cnn-vit.png",
        "CNN filters extract numeric features; ViTs apply attention to image patches")
d.bullets("Multimodal models", [
    "Understand and work with more than one data type — e.g. an image plus a text question",
    "ViTs use cross-modal attention to combine visual and language vector spaces",
    "Analyze images through the OpenAI API multi-part content structure:",
    (1, "content = [{type: input_text, …}, {type: input_image, image_url: …}]"),
    (1, "images can be URLs or base64-encoded data")])
d.image("Image generation — diffusion models", "diffusion.png",
        "Train by adding noise to labeled images; generate by denoising random pixels toward the prompt")
d.bullets("Image & video generation in Foundry", [
    "Image generation: search the catalog for 'text to image' inference-task models (e.g. gpt-image family)",
    "Generate programmatically by sending prompts through the OpenAI Responses API to your deployed model",
    "Video generation: 'video generation' task models (e.g. sora family)",
    "Video runs as an asynchronous job — resource-intensive and slow, so you submit then poll for completion"])
d.closing([
    "Task discriminators: locate → detection; per-pixel → segmentation; describe → contextual",
    "CNN filters extract numeric features (not visual effects)",
    "Multimodal = multiple input types in one prompt; images via URL or base64",
    "sora video jobs are asynchronous because generation takes time and resources"],
    "Next: Module 6 — Information extraction")
d.save("AI901-05-Computer-Vision.pptx")

# Deck 6 — Information extraction
d = Deck()
d.title_slide("MODULE 6", "Information Extraction",
              "OCR · field mapping · Azure Content Understanding · audio & video analysis")
d.bullets("What is information extraction?", [
    "Analyzing unstructured content to identify and extract relevant fields and values",
    "Sources: documents & emails, business cards & receipts, invoices & contracts, images, audio, video",
    "Example: photo of a receipt → vendor, date and amount pre-filled into an expense claim",
    "Not the same as querying a database or copying files — the content starts unstructured"])
d.image("OCR pipeline", "ocr-pipeline.png",
        "Acquisition → pre-processing → text-region detection → character recognition → text output")
d.image("Field extraction & mapping", "field-extraction.png",
        "OCR ingestion → field detection → schema mapping → normalization → business integration")
d.bullets("Generative AI in extraction", [
    "Semantic language models match extracted values to data fields accurately",
    "Replaces hand-coded extraction rules per document type",
    "Normalization standardizes values: $20 → 20.00, 01/01/2025 → 2025-01-01"])
d.bullets("Azure Content Understanding in Foundry Tools", [
    "Key advantage over plain OCR: understands document structure and maps data to a defined schema",
    "Analyzer = defines how content is processed and what structured data is returned",
    (1, "Predefined analyzers — invoices, receipts, contracts, post-call recordings"),
    (1, "Custom analyzers — define your own schema from sample documents"),
    "Results returned as JSON via the REST API",
    "Python SDK flow is asynchronous: submit content → poll a URL until the job completes"])
d.bullets("Audio & video scenarios", [
    "Post-call analysis for contact centers (topics, sentiment, speakers)",
    "Voice-message automation",
    "Video call transcription and summary",
    "Video recording analysis",
    "Same analyzer concept — predefined or custom — applied to media"])
d.closing([
    "OCR = images of text → machine-readable text; Content Understanding adds schema & structure",
    "Analyzer defines processing + output schema; confidence scores per field",
    "SDK results are polled, not returned inline",
    "You have now covered 100% of the AI-901 syllabus — go take the mock exams!"],
    "Finish: run Quiz 6A/6B, then Final Mock Exams 1 & 2 in the portal")
d.save("AI901-06-Information-Extraction.pptx")

print("done")
