<div align="center">

# Hi there, I'm Prince Baah-Mensah 👋

### **Electrical & Electronic Engineering Researcher @ Ashesi University**
*Bridging Machine Learning Inference Acceleration, FPGA Hardware Co-Design, and Control Engineering*

[![Website](https://img.shields.io/badge/Website-princebaah.vercel.app-005cb9?style=for-the-badge&logo=vercel&logoColor=white)](https://princebaah.vercel.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Prince_Baah--Mensah-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prince-baah-mensah)
[![GitHub](https://img.shields.io/badge/GitHub-Baah134-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Baah134)
[![IEEE IMS Scholarship](https://img.shields.io/badge/IEEE_IMS-Scholarship_Recipient-10b981?style=for-the-badge&logo=ieee&logoColor=white)](#honors--leadership)

---

</div>

## 📌 About Me

I am an Electrical and Electronic Engineering undergraduate researcher at **Ashesi University**. My work operates at the intersection of **machine learning inference**, **embedded hardware acceleration**, and **control systems**. I design hardware-software co-design pipelines that make intelligent systems faster, more energy-efficient, and physically robust—from **ASIC/FPGA sparse compute units** to **constraint-aware Bayesian Optimization** and **TinyML edge microcontrollers**.

- 🔭 **Current Focus:** Hardware acceleration of sparse GEMV operations on FPGAs & TinyML edge deployment vs. cloud LLM reasoning.
- 🏆 **Recognitions:** IEEE IMS Undergraduate Scholarship Recipient | IEEE MYOSA 4.0 Global Finalist | IEEE Ashesi Branch Co-founder & Chair.
- 🎓 **Leadership:** President, Ashesi Engineering Student Association (AESA) | President, Effective Altruism Ashesi.
- 🌐 **Portfolio Website:** Explore interactive demos, papers, and projects at [princebaah.vercel.app](https://princebaah.vercel.app).

---

## 🔬 Core Research Interests

### 1. ⚡ FPGA Hardware Co-Design & ML Inference Acceleration
- **Activation Sparsity Compute Engines:** Designing ASIC/FPGA-targeted hardware in Verilog that dynamically detects and bypasses zero-valued activations (e.g., produced by ReLU), conserving clock cycles and dynamic switching power on edge devices.
- **Autonomous Vivado RTL Loops (`FPGA Autoresearch`):** Developing autonomous agentic loops that execute overnight Vivado Tcl synthesis batch runs, extracting timing/area/power metrics and committing hardware optimizations using free NVIDIA NIM LLM endpoints.

### 2. 🎛️ Constraint-Aware Machine Learning for Control Engineering
- **Constrained Black-Box PID Tuning:** Reformulating classic PID controller tuning as a strictly constrained black-box optimization problem solved via constraint-aware Bayesian Optimization (BO).
- **Robustness & Sample Efficiency:** Proving that BO maintains **75–100% specification compliance** under severe parametric uncertainty (compared to **1–38%** for classical MATLAB `pidtune`) while achieving **4–20× sample efficiency** over population-based evolutionary algorithms (Genetic Algorithms & CMA-ES).

### 3. 🧠 TinyML Edge Intelligence vs. Cloud LLM Inference
- **On-Device Ambient Assisted Living (AAL):** Training 1D Convolutional Neural Networks (1D-CNN) compressed to **75.6 KB** via one-shot magnitude pruning and INT8 quantization for real-time deployment on ESP32 microcontrollers via TensorFlow Lite Micro.
- **Benchmarking & Failure Mode Analysis:** Benchmarking edge TinyML against cloud-hosted LLMs (Google Gemma 4, Meta Llama 3.1, Mistral Medium 3.5 via NVIDIA Build API). Demonstrating **1.00 Macro F1** and **100% inference availability** for TinyML vs. **0.84 F1** and **60% availability** for cloud LLMs, identifying critical reasoning deficits in general-purpose LLMs during daytime inactivity detection.

### 4. 🎙️ Speaker-Strict Speech Emotion Recognition (SER)
- **Generalization Across Unseen Speakers:** Engineering self-supervised learning (SSL) representations, Librosa signal processing pipelines, and hybrid CNN-Transformers in PyTorch to close the 30%+ generalization gap on unseen speakers.

---

## 📚 Publications & Accepted Research

| Title | Venue / Conference | Status | Links |
| :--- | :--- | :---: | :---: |
| **Constraint-Aware Bayesian Optimization for PID Tuning: Discovering Plant-Specific Control Strategies** | 52nd Annual Conference of the IEEE Industrial Electronics Society (**IEEE IECON 2026**) | 🟢 **Accepted** | [![GitHub](https://img.shields.io/badge/Code-Repo-181717?style=flat&logo=github)](https://github.com/Baah134/iecon-2026-pid-bo-tuning) \| [Details](https://princebaah.vercel.app/research/bayesian-pid) |
| **AI-Powered Adaptive Learning System for Education in the Metaverse Classroom** | IEEE International Conference on Smart Sustainable Systems for Computer and Engineering Applications (**IEEE 3SCEA 2026**) | 🟢 **Accepted** | [![IEEE Xplore](https://img.shields.io/badge/IEEE_Xplore-11602834-00629B?style=flat&logo=ieee)](https://ieeexplore.ieee.org/document/11602834) \| [Details](https://princebaah.vercel.app/research/metaverse-education) |
| **Multi-Label Health State Classification in Ambient Assisted Living: Comparing TinyML Edge Deployment and Cloud LLM Inference** | Target: IEEE Conference Submission (July 2026) | 🟡 **Manuscript Under Prep** | [Details](https://princebaah.vercel.app/research/tinyml-aal) |
| **Speaker-Strict Comparative Analysis of SER Architectures** | Target: IEEE Publication Submission | 🟡 **Ongoing Research** | [Details](https://princebaah.vercel.app/research/speech-emotion) |

---

## 💻 Featured Projects & Repositories

### 🛠️ [`sparse-gemv-fpga`](https://github.com/Baah134/sparse-gemv-fpga) — Sparse-Compute AI Hardware Accelerator
> **Verilog RTL · Vivado Simulator · Block RAM · FSM Controller**  
> Custom ASIC/FPGA compute engine designed in Verilog that dynamically detects null activations before the execution stage, skipping zero-valued operands to conserve dynamic switching power and speed up edge inference times.  
> 🔗 [View Repository](https://github.com/Baah134/sparse-gemv-fpga) · [Project Case Study](https://princebaah.vercel.app/projects/sparse-compute-accelerator)

### 🤖 [`fpga-autoresearch`](https://github.com/Baah134) — Autonomous Vivado RTL Loop
> **Python · Verilog · Vivado Tcl · NVIDIA NIM API · Git**  
> An autonomous agentic loop applying the 'autoresearch' paradigm to FPGA hardware design. Runs unattended overnight batch Vivado synthesis runs, parses timing/power/area reports, and executes keep-or-revert git commits via NVIDIA NIM LLMs.  
> 🔗 [Project Case Study](https://princebaah.vercel.app/projects/fpga-autoresearch)

### 📚 [`llm-wiki`](https://github.com/Baah134/llm-wiki) — Personal AI Knowledge Base
> **Python · Flask · LLM Agents · NVIDIA NIM API · Markdown Processing**  
> A self-compounding personal knowledge base agent inspired by Andrej Karpathy's LLM Wiki pattern. Automatically compiles research papers and PDFs into an index-first, interlinked wiki network with conflict resolution.  
> 🔗 [View Repository](https://github.com/Baah134/llm-wiki) · [Project Case Study](https://princebaah.vercel.app/projects/llm-wiki)

### 🎙️ `fine-tuning-whisper` — Fine-tuning Whisper for African Accents
> **PyTorch · LoRA / PEFT · Hugging Face · ASR**  
> Systematic evaluation and LoRA-based parameter-efficient fine-tuning of OpenAI's Whisper model on African-accented English, achieving a **64% reduction in Word Error Rate** (from 0.50 to 0.18).  
> 🔗 [Project Case Study](https://princebaah.vercel.app/projects/whisper)

### 💡 `lumina-ambient-ai` — Lumina Ambient Intelligence System
> **ESP32 · Sensors · SQL · Nvidia Nemotron LLM · MQTT**  
> Non-intrusive ambient monitoring system for assisted living that translates raw PIR motion and DHT environmental sensor data into human-readable safety insights. **IEEE MYOSA 2025 Global Finalist**.  
> 🔗 [Project Case Study](https://princebaah.vercel.app/projects/lumina)

---

## 🛠️ Technical Skill Matrix

```
  Hardware & Embedded Systems  │ Verilog HDL, Xilinx Vivado (Tcl Batch, ILA), ESP32, Block RAM, FSM Controllers, PCB Design, Arduino
  AI / ML & Optimization       │ PyTorch, TensorFlow, TensorFlow Lite Micro, Optuna, LoRA/PEFT, Bayesian Optimization, Librosa, GA/CMA-ES
  Languages & Tools            │ Python, C/C++, MATLAB (ode45, Control System Toolbox), SQL, Git, Linux, Flask, NVIDIA Build API
```

<div align="center">

![Verilog](https://img.shields.io/badge/Verilog-005cb9?style=flat-square&logo=microchip&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-E0123C?style=flat-square&logo=espressif&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![MATLAB](https://img.shields.io/badge/MATLAB-CC3333?style=flat-square&logo=mathworks&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA_NIM-76B900?style=flat-square&logo=nvidia&logoColor=white)

</div>

---

## 🏅 Honors & Leadership

- 🏆 **IEEE IMS Undergraduate Scholarship** — Granted by the IEEE Instrumentation and Measurement Society for academic excellence and technical potential.
- ⚡ **Co-founder & Chair, IEEE Ashesi Student Branch** (Nov 2024 – Present) — Scaled Ashesi's first IEEE chapter from 0 to 75+ active members, the largest student branch in Ghana.
- 🎓 **President, Ashesi Engineering Student Association (AESA)** (Jan 2026 – Present) — Leading academic, technical, and industry-facing initiatives for the primary engineering student body.
- 💡 **President, Effective Altruism Ashesi** (Jan 2026 – Present) — Facilitating discussions on AI Safety, Biosecurity, and evidence-based technical inquiry.
- 🌐 **Global Finalist, IEEE MYOSA 4.0** — Selected as a global finalist for IEEE APSCON 2026 for ambient assisted living intelligence.

---

## 📬 Connect With Me

<div align="center">

🌐 **Website:** [princebaah.vercel.app](https://princebaah.vercel.app) &nbsp;|&nbsp;
💼 **LinkedIn:** [linkedin.com/in/prince-baah-mensah](https://www.linkedin.com/in/prince-baah-mensah) &nbsp;|&nbsp;
🐙 **GitHub:** [@Baah134](https://github.com/Baah134)

</div>
