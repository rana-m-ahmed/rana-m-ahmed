<p align="center">
  <img src="./assets/rma-signal.svg" alt="Rana Muhammad Ahmed — Applied AI and Software Engineer" width="100%" />
</p>

<p align="center">
  <strong>I build AI-powered products end to end — from models, RAG and agent workflows to secure APIs, web/mobile interfaces and deployable runtimes.</strong>
</p>

<p align="center">
  I like owning the whole path from idea to working system. My research background is the layer underneath: it shapes how I evaluate, test and harden what I ship.
</p>

<p align="center">
  <a href="mailto:ranamuhammadahmed6@gmail.com">Email</a>
  &nbsp;·&nbsp;
  <a href="https://linkedin.com/in/rana-muhammad-ahmed-571057295">LinkedIn</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/rana-m-ahmed">GitHub</a>
</p>

<p align="center">
  <code>AI Engineer</code>&nbsp;&nbsp;<code>Applied ML</code>&nbsp;&nbsp;<code>Python / Backend</code>&nbsp;&nbsp;<code>Full-Stack AI</code>&nbsp;&nbsp;<code>Computer Vision / Edge</code>
</p>

<p align="center">
  <img src="./assets/evidence-strip.svg" alt="Engineering delivery stack across applied AI, backend systems, web and mobile product engineering, and deployment" width="100%" />
</p>

## What I can ship

- **AI features and systems** — RAG, agents, computer vision, inference pipelines, evaluation, prompt-injection defenses and edge ML.
- **Backend infrastructure** — FastAPI services, PostgreSQL/Supabase, authentication, vector search, streaming APIs and model-serving workflows.
- **Web and mobile products** — Next.js/React dashboards, Flutter applications, analytics surfaces and embedded AI experiences.
- **Production engineering** — Docker, CI/CD, automated QA, Playwright/Vitest/pytest, deployment hardening and direct runtime validation.

---

## Selected engineering

### 01 / [Synapse](https://github.com/rana-m-ahmed/Synapse)

**A multi-tenant RAG platform built as a complete AI product, not a notebook demo.**

Synapse takes private documents from ingestion to deployed agent experience: chunking and embeddings feed **PostgreSQL + pgvector/HNSW** retrieval, **Supabase Auth** protects tenant data, **FastAPI** orchestrates inference, SSE streams responses, and a **Next.js** control plane manages agents, analytics and a one-line embeddable web component.

<code>FastAPI</code> <code>Next.js</code> <code>Supabase</code> <code>PostgreSQL</code> <code>pgvector</code> <code>RAG</code> <code>SSE</code>

[Repository](https://github.com/rana-m-ahmed/Synapse)

---

### 02 / [ReadOut](https://github.com/rana-m-ahmed/ReadOut-B2B-Analytics-SaaS)

**Conversational analytics that turns uploaded business data into grounded visual answers.**

ReadOut combines a **Next.js 16 / React 19** product surface with a **Python API** and Supabase-backed workflow. Users ask natural-language questions against their own datasets and receive schema-grounded analysis, visualisations and follow-up insight. The engineering stack includes static checks, **Vitest**, **Playwright** and **axe-core** accessibility validation.

<code>Next.js</code> <code>React</code> <code>Python</code> <code>Supabase</code> <code>Analytics</code> <code>Playwright</code> <code>Accessibility</code>

[Repository](https://github.com/rana-m-ahmed/ReadOut-B2B-Analytics-SaaS) · [Live demo](https://readoutanalytics.vercel.app/)

---

### 03 / [Anti-LLM Injection Gateway](https://github.com/rana-m-ahmed/Anti-LLM-Injection-Gateway)

**A security layer for LLM applications that turns adversarial and sensitive-input signals into explicit runtime policy.**

The gateway combines **50+ weighted prompt-injection patterns**, encoding and structural checks, Microsoft Presidio plus custom secret recognizers, and an explainable **Block / Warn / Mask / Allow** policy engine behind FastAPI. Its QA path covers detector, policy, API and responsive browser behavior.

<code>FastAPI</code> <code>Presidio</code> <code>LLM Security</code> <code>PII</code> <code>Policy Enforcement</code> <code>Playwright</code>

[Repository](https://github.com/rana-m-ahmed/Anti-LLM-Injection-Gateway) · [Related research](https://arxiv.org/abs/2608.12880)

---

### 04 / [CropCop](https://github.com/rana-m-ahmed/ResearchWork-CropCop)

**A 120-class computer-vision pipeline carried from data engineering and model evaluation into an executed edge runtime.**

CropCop moves through the full ML delivery chain: **117,546 source images audited**, a **109,107-image / 120-class** frozen benchmark, a compact MobileNetV4 lineage, validation-only post-training quantisation, and direct execution as a **22.60 MiB ExecuTorch/XNNPACK PTE** with **98.46% internal-test accuracy**.

<code>PyTorch</code> <code>Computer Vision</code> <code>MobileNetV4</code> <code>PTQ</code> <code>ExecuTorch</code> <code>XNNPACK</code> <code>Edge AI</code>

[Repository](https://github.com/rana-m-ahmed/ResearchWork-CropCop) · [Paper](https://arxiv.org/abs/2608.25539) · [Evidence chain](https://github.com/rana-m-ahmed/ResearchWork-CropCop#evidence-chain)

---

## More things I've built

<details>
  <summary><strong>OrthoLens</strong> — explainable medical-imaging prototype · <code>DenseNet121</code> <code>Grad-CAM</code> <code>Docker</code> <code>Next.js</code></summary>

  DenseNet121 inference with structured probabilities and Grad-CAM visual explanations behind a thread-safe backend and a separate Next.js review interface. Development reference metrics include **0.9813 test AUC**; the project explicitly does not claim clinical validity.

  [Backend](https://github.com/rana-m-ahmed/ortholens-backend) · [Frontend](https://github.com/rana-m-ahmed/ortholens-frontend) · [Live demo](https://ortholens-ai.vercel.app/)
</details>

<details>
  <summary><strong>Haul</strong> — mobile commerce with visual search · <code>Flutter</code> <code>FastAPI</code> <code>Firebase</code> <code>Stripe</code></summary>

  Android-first marketplace work spanning product discovery, recommendation and visual-search flows, resilient client state, backend services and server-authoritative Stripe test checkout.

  [Repository](https://github.com/rana-m-ahmed/Haul-Ecommerce-Marketplace)
</details>

<details>
  <summary><strong>AIDRA</strong> — hybrid AI disaster-response system · <code>A*</code> <code>CSP</code> <code>ML</code> <code>Socket.IO</code></summary>

  A real-time rescue simulation combining risk-aware A*, constraint allocation with MRV/forward checking, survival prediction, fuzzy urgency scoring and a Flask + Socket.IO command surface.

  [Repository](https://github.com/rana-m-ahmed/Intelligent-Disaster-Response-Agent)
</details>

<details>
  <summary><strong>Compresso</strong> — multithreaded lossless compression utility · <code>C++17</code> <code>Qt</code> <code>CMake</code></summary>

  Folder-oriented archival using Canonical Huffman Coding, custom binary metadata, directory reconstruction and asynchronous desktop processing.

  [Repository](https://github.com/rana-m-ahmed/Compresso)
</details>

<details>
  <summary><strong>TPU Systolic Array Visualizer</strong> — cycle-by-cycle architecture simulation · <code>React</code> <code>TypeScript</code> <code>Vite</code></summary>

  An interactive browser-side simulator for TPU-style systolic matrix multiplication, with architecture references, timeline controls, reduced-motion support and automated validation.

  [Repository](https://github.com/rana-m-ahmed/TPU-Systolic-Array-Visualizer)
</details>

---

## Industry experience

**2026 — now · Pakistan Telecommunication Authority (PTA), Headquarters**  
**ICT Intern — Enterprise ICT, AI, Governance & DevOps**  
Working around reliability, auditability, data handling, AI governance and the DevOps/change-management practices required to move enterprise and public-sector systems into resilient production environments.

**2026 · EaseZen Solutions**  
**AI/ML Intern**  
Worked across dataset preparation, model training and evaluation, error analysis, and the conversion of experimental workflows into reusable engineering pipelines.

---

## Engineering toolkit

| Area | Stack |
|---|---|
| **Applied AI / ML** | Python · PyTorch · TensorFlow/Keras · Hugging Face · OpenCV · scikit-learn · RAG · agents · embeddings · computer vision · PTQ · ExecuTorch |
| **Backend / data** | FastAPI · PostgreSQL · Supabase · Firebase · REST APIs · Auth · SSE · pgvector/HNSW · vector search |
| **Web / mobile** | TypeScript/JavaScript · Next.js · React · Flutter · Dart · Tailwind CSS |
| **Engineering / systems** | C++ · Docker · Linux · Git/GitHub · CI/CD · pytest · Playwright · Vitest · algorithms · data structures |

---

## Research depth

Research is not the destination of this profile; it is an engineering advantage. I use it to make stronger decisions around evaluation, reproducibility, failure analysis, security and model/runtime evidence.

**[Labels Are Not Endpoints: Treatment Leakage and Construct Validity in MCP Agent Security Evaluation](https://arxiv.org/abs/2608.12880)**  
Rana Muhammad Ahmed, Sabahat Abbas · arXiv preprint · 2026  
Audits treatment-contaminated behavioral endpoints in a closed MCP-style agent-security campaign and reconstructs treatment-blind outcomes from preserved execution evidence.

**[CropCop: An Auditable 120-Class Plant-Health Model from Benchmark Reconstruction to a Quantised Runtime Artifact](https://arxiv.org/abs/2608.25539)**  
Rana Muhammad Ahmed, Sabahat Abbas · arXiv preprint · 2026  
Connects leakage-aware dataset reconstruction, compact-model evaluation, post-training quantisation and direct execution of the serialized runtime artifact.

---

## Education, problem solving & leadership

**B.S. Computer Science — Bahria University Islamabad**  
Expected Dec 2027 · **CGPA 3.89 / 4.00** · ranked **#1 in the Spring 2024 cohort** · Rector's Honour List · University Merit Scholar · Orange Tree Foundation Scholar

**Founder & Captain — The Pull Pirates**  
Competitive-programming team representing Bahria University at ICPC and national contests; represented the university at **ICPC Asia Topi Regional 2025**.

**BU GlobalX Student Ambassador**  
Selected among the university's student ambassadors supporting international academic, STEM and professional engagement.

---

## Available for engineering work

**Open to paid remote part-time, contract and high-impact internship opportunities.**

I am most useful where a team needs someone who can move across the stack rather than stop at a model or mockup:

<code>AI Engineer</code> · <code>Applied AI / ML</code> · <code>Full-Stack AI</code> · <code>Python / Backend</code> · <code>Computer Vision / Edge AI</code>

**Availability:** ~15–20 hours/week · **Location:** Islamabad, Pakistan · **Timezone:** UTC+05

**Reach me:** [ranamuhammadahmed6@gmail.com](mailto:ranamuhammadahmed6@gmail.com) · [LinkedIn](https://linkedin.com/in/rana-muhammad-ahmed-571057295)

---

<p align="center">
  <sub>RMA / MODEL → API → PRODUCT → SHIP</sub>
</p>
