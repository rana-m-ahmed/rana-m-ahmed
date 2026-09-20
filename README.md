<p align="center">
  <img src="./assets/rma-signal.svg" alt="Rana Muhammad Ahmed — Applied AI and Software Engineer" width="100%" />
</p>

<p align="justify">
  <strong>I build AI-powered products end to end — from models, RAG and agent workflows to secure APIs, production-minded backends, polished web/mobile interfaces and deployable runtimes.</strong> I enjoy owning the difficult middle between an idea and a working system: turning ambiguous requirements into architecture, wiring the data and inference layers together, validating failure paths, and shipping something people can actually use.
</p>

<p align="justify">
  My research work sits underneath that engineering rather than replacing it. It has trained me to question benchmarks, trace evidence, test assumptions and make claims that survive scrutiny — habits I carry directly into product development, AI security, model evaluation and deployment.
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

### Pakistan Telecommunication Authority (PTA), Headquarters
**ICT Intern — Enterprise ICT, AI, Governance & DevOps** · *Aug–Sep 2026 · Islamabad, Pakistan*

Worked under senior PTA officers to understand how national-scale telecom and public-sector ICT services are kept reliable, secure and governable in regulated environments.

- Examined enterprise-AI and agentic-system requirements around **data handling, auditability, human oversight and operational governance**.
- Reviewed **DevOps, CI/CD, change-management and reliability practices** used to move systems from development into controlled production environments.
- Built practical exposure to the engineering constraints that appear at **government and enterprise scale**, where resilience, accountability and traceability matter alongside functionality.

### EaseZen Solutions
**AI/ML Intern** · *Jan–Mar 2026*  
<code>Applied ML</code> <code>Model Evaluation</code> <code>Error Analysis</code> <code>Workflow Engineering</code>

Worked across the model-development loop rather than a single isolated task, with a focus on making ML experiments easier to evaluate, reproduce and hand off.

- Prepared and cleaned datasets for training/evaluation workflows, helping turn raw inputs into consistent model-ready data.
- Supported **model training, validation and comparative evaluation**, then used error analysis to identify failure patterns and guide the next iteration.
- Helped move work beyond one-off notebooks by separating repeatable preprocessing, training and evaluation steps into **clearer reusable workflows**.
- Strengthened **reproducibility and engineering handoff** through documented experiment structure, consistent evaluation practice and reusable pipeline components.

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

Research is an engineering advantage for me: a way to make better decisions about evaluation, reproducibility, failure analysis, security and the evidence behind a system.

**[Labels Are Not Endpoints: Treatment Leakage and Construct Validity in MCP Agent Security Evaluation](https://arxiv.org/abs/2608.12880)**  
Rana Muhammad Ahmed, Sabahat Abbas · arXiv preprint · 2026  
Audits treatment-contaminated behavioral endpoints in a closed MCP-style agent-security campaign and reconstructs treatment-blind outcomes from preserved execution evidence.

**[CropCop: An Auditable 120-Class Plant-Health Model from Benchmark Reconstruction to a Quantised Runtime Artifact](https://arxiv.org/abs/2608.25539)**  
Rana Muhammad Ahmed, Sabahat Abbas · arXiv preprint · 2026  
Connects leakage-aware dataset reconstruction, compact-model evaluation, post-training quantisation and direct execution of the serialized runtime artifact.

**[HiSPA Robotics v3.1 — Mamba-based Robotic Controller Security](https://github.com/rana-m-ahmed/Research-Work-Adversarial-Amnesia-Hidden-State-Poisoning-in-Mamba-Based-Robotic-Controllers)**  
Ongoing research infrastructure · 2026  
An isolated, fail-closed clean reimplementation for studying adversarial-amnesia / hidden-state-poisoning questions around Mamba-based robotic controllers. The current public repository intentionally contains **no scientific results yet** and keeps later experimental workflows unauthorized by default until the repository and dataset-lineage gates are satisfied.

---

## Education & recognition

### B.S. Computer Science — Bahria University Islamabad Campus
*Spring 2024 — Expected Dec 2027*

**CGPA: 3.89 / 4.00** · **Ranked #1 in the Spring 2024 BSCS cohort**

- **Rector's Honour List**
- **University Merit Scholar**
- Coursework spanning **Artificial Intelligence, Data Structures & Algorithms, Database Systems, Computer Networks, Software Engineering and Linear Algebra**

### Academic signal

<code>3.89 / 4.00 CGPA</code> · <code>#1 cohort rank</code> · <code>Merit scholarship</code> · <code>Honour List</code>

---

## Leadership, competition & community

### The Pull Pirates — Founder & Captain
*Sep 2024 — Present*

Founded and lead a competitive-programming team representing Bahria University across ICPC and national contests. Cleared internal selection/preliminary stages and represented the university at the **ICPC Asia Topi Regional 2025**.

<code>C++</code> <code>Algorithms</code> <code>Problem Solving</code> <code>Team Leadership</code>

### BU GlobalX Student Ambassador
*Feb 2026 — Present*

Selected as **one of 14 university ambassadors**, supporting STEM outreach, international engagement and student participation in global academic and professional opportunities, including peer-facing workshops and campus initiatives.

### Community, accessibility & sport

- Contributed to university **community-service and Iftar-drive initiatives**, including work with **Noreen Zindagi Welfare Trust**.
- Built a **text-to-speech accessibility tool** aimed at improving access for users with visual impairments and reading difficulties.
- Participated in **badminton and cricket** at inter-university events including **NUST Olympiad** and **NESCON**.

---

## Available for engineering work

**Open to paid remote contract, part-time and high-impact internship opportunities.**

I am most useful where a team needs someone who can move across the stack rather than stop at a model or mockup:

<code>AI Engineer</code> · <code>Applied AI / ML</code> · <code>Full-Stack AI</code> · <code>Python / Backend</code> · <code>Computer Vision / Edge AI</code>

**Availability:** 30+ hours/week · **Location:** Islamabad, Pakistan · **Timezone:** UTC+05

**Reach me:** [ranamuhammadahmed6@gmail.com](mailto:ranamuhammadahmed6@gmail.com) · [LinkedIn](https://linkedin.com/in/rana-muhammad-ahmed-571057295)

---

<p align="center">
  <sub>MODEL → API → PRODUCT → SHIP</sub>
</p>
