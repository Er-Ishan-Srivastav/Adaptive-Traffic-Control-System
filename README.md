<div align="center">

<!-- HERO BANNER -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=220&section=header&text=CAMAF&fontSize=90&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Context-Aware%20Multi-Agent%20Federated%20Learning%20for%20Adaptive%20Traffic%20Signal%20Control&descAlignY=60&descSize=16&descColor=a78bfa"/>

<!-- BADGES ROW 1 -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/YOLOv11-Object%20Detection-FF6B35?style=for-the-badge&logo=opencv&logoColor=white"/>
  <img src="https://img.shields.io/badge/Federated%20Learning-FedProx-7C3AED?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/SUMO-Simulation-00C49A?style=for-the-badge&logo=googlemaps&logoColor=white"/>
</p>

<!-- BADGES ROW 2 -->
<p>
  <img src="https://img.shields.io/badge/Chandigarh%20University-2026-DC2626?style=for-the-badge&logo=graduation-cap&logoColor=white"/>
  <img src="https://img.shields.io/badge/BE%20CSE%20(BDA)-8th%20Semester-1D4ED8?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/mAP%400.5-0.432-22C55E?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Bandwidth%20Reduction-~90%25-F59E0B?style=for-the-badge"/>
</p>

<br/>

> **"Transforming passive urban surveillance into an intelligent, privacy-preserving nervous system for the city."**

<br/>

</div>

---

## 🧠 What is CAMAF?

**CAMAF** *(Context-Aware Multi-Agent Federated Learning)* is a next-generation adaptive traffic signal control framework that redefines how intersections think, communicate, and learn — without ever compromising citizen privacy.

Traditional traffic systems are **blind**. They follow pre-programmed timers that ignore what's actually happening on the road. CAMAF transforms every intersection into an **intelligent agent** that:

- 🔍 **Sees** — using YOLOv11 real-time vehicle detection on edge hardware
- 🧩 **Coordinates** — via Spatio-Temporal Graph (STGCN) communication between intersections
- 🔒 **Learns privately** — through Federated Learning that never shares raw video data
- ⚡ **Acts** — dynamically adjusting green phase durations to prevent gridlock *before it forms*

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CAMAF THREE-LAYER PIPELINE                     │
├───────────────────┬──────────────────────┬──────────────────────────┤
│  LAYER I          │  LAYER II            │  LAYER III               │
│  Edge Processing  │  Coordination        │  Federated Learning      │
│  (Perception)     │  (Network Control)   │  (Global Optimization)   │
├───────────────────┼──────────────────────┼──────────────────────────┤
│                   │                      │                          │
│  CCTV Video ──►   │  Graph G = (V, E)    │  Local Model Weights     │
│  YOLOv11n         │  ┌─────────────────┐ │  ──► FedProx Aggregation │
│  Detection        │  │ Node A ──► Node B│ │  ──► Global Model Bcast │
│  BoT-SORT Track   │  └─────────────────┘ │                          │
│                   │                      │  w(t+1) = 1/K Σ wk(t+1) │
│  Outputs:         │  Look-Ahead:         │                          │
│  • Density D      │  If P_down > 0.80:   │  ~5–10 MB / node         │
│  • Max Wait Wmax  │  Cap green phase Tg  │  vs. raw video streaming │
│  • Emergency E    │                      │                          │
└───────────────────┴──────────────────────┴──────────────────────────┘
```

**Dynamic Green Time Formula:**
```
Tg = α·D  +  β·ΣWl  +  γ·E
```
Where `D` = vehicle density, `Wl` = cumulative lane wait time, `E` = emergency priority flag,
and `α`, `β`, `γ` are federated-learned scalar weights.

---

## 🚀 Key Innovations

<table>
<tr>
<td width="33%" valign="top">

### 👁️ Perceptual Layer
- **YOLOv11n** — nano variant for real-time inference on edge devices (NVIDIA Jetson)
- **BoT-SORT** tracking — persistent vehicle identity across frames
- **12 vehicle classes** — from cars to big buses
- **640×640px** input resolution
- **6 GB VRAM** constrained training

</td>
<td width="33%" valign="top">

### 🕸️ Coordination Layer
- Intersection graph: **G = (V, E)**
- Downstream pressure metric:  
  `P_down = N_current / C_road`
- **80% occupancy threshold** triggers look-ahead suppression
- Prevents **cascade gridlock** propagation
- Orthogonal flows continue unimpeded

</td>
<td width="33%" valign="top">

### 🔐 Privacy Layer
- **Flower (flwr)** federated framework
- **FedProx** optimization — handles non-IID traffic distributions
- Only **model weights** transmitted (~5–10 MB/node)
- **~90% bandwidth reduction** vs. centralized streaming
- Raw video **never leaves** the edge device

</td>
</tr>
</table>

---

## 📊 Detection Performance

<div align="center">

### YOLOv11n — Model Metrics at a Glance

| Metric | Value | Notes |
|:---|:---:|:---|
| **mAP@0.5** | `0.432` | Across all 12 vehicle classes |
| **mAP@0.5:0.95** | `0.29` | Stricter localization threshold |
| **Best F1 Score** | `0.47` | At confidence threshold = 0.418 |
| **Peak Precision** | `0.82` | At confidence = 1.0 |
| **Peak Recall** | `0.82` | At confidence = 0.0 |
| **Training Epochs** | `50` | Early stopping @ patience = 10 |

</div>

### Per-Class AP@0.5 Performance

```
car          ██████████████████████████████████████████  0.817  ✅ Dominant class
big truck    ████████████████████████████████            0.650
truck-xl     ████████████████████████████               0.553
truck-l      █████████████████████████                  0.502
big bus      ████████████████████████████████           0.632
small truck  █████████████████████████████              0.596
truck-m      ████████████████████                       0.411
mid truck    ████████████████████                       0.408
bus-s        ███████████                                0.222
truck-s      █████████████                              0.283
small bus    ██                                         0.060  ⚠️ Class imbalance
bus-l        █                                          0.048  ⚠️ Class imbalance
```

> **Design Note:** The car class dominates the training set with **19,083 instances** vs. bus-l with just **120 instances** (>100:1 ratio). Future work includes focal loss tuning and synthetic augmentation.

---

## 🔬 Simulation Results (Eclipse SUMO)

> Validated via **TraCI interface** on a two-node signalized network (Node A → Node B, 3 lanes/approach)

<table>
<tr>
<th>Condition</th>
<th>Isolated Adaptive Control</th>
<th>CAMAF Coordination</th>
</tr>
<tr>
<td><b>Congestion Propagation</b></td>
<td>❌ Spillback from Node B → Node A</td>
<td>✅ Suppressed by look-ahead gate</td>
</tr>
<tr>
<td><b>Gridlock</b></td>
<td>❌ Full network gridlock occurs</td>
<td>✅ Gridlock prevented entirely</td>
</tr>
<tr>
<td><b>Orthogonal Flow</b></td>
<td>⚠️ Partially blocked</td>
<td>✅ Continues unimpeded</td>
</tr>
<tr>
<td><b>Trigger Mechanism</b></td>
<td>None — purely local</td>
<td>P_down > 0.80 → green phase capped</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Detection** | `YOLOv11n` + `BoT-SORT` | Real-time vehicle detection & tracking |
| **Vision** | `OpenCV` | Video stream processing |
| **Training** | `PyTorch` | Deep learning framework |
| **Coordination** | `STGCN` | Spatio-temporal graph for inter-intersection logic |
| **Federated Learning** | `Flower (flwr)` + `FedProx` | Privacy-preserving distributed training |
| **Simulation** | `Eclipse SUMO` + `TraCI` | Urban traffic digital twin |
| **Security** | `AES-256` | Encrypted metadata transmission |
| **Hardware Target** | `NVIDIA Jetson` | Edge inference deployment |

</div>

---

## 📁 Repository Structure

```
📦 CAMAF-Traffic-Signal-Control
 ┣ 📂 detection/
 ┃ ┣ 📜 train.py              # YOLOv11n training pipeline
 ┃ ┣ 📜 inference.py          # Edge inference engine
 ┃ ┗ 📜 tracker.py            # BoT-SORT integration
 ┣ 📂 coordination/
 ┃ ┣ 📜 graph_model.py        # Spatio-temporal graph G=(V,E)
 ┃ ┗ 📜 signal_logic.py       # Dynamic green-time formula
 ┣ 📂 federated/
 ┃ ┣ 📜 server.py             # FedProx aggregation server
 ┃ ┗ 📜 client.py             # Edge node training client
 ┣ 📂 simulation/
 ┃ ┣ 📜 sumo_env/             # SUMO network configuration
 ┃ ┗ 📜 traci_control.py      # TraCI Python interface
 ┣ 📂 results/
 ┃ ┣ 📊 confusion_matrices/
 ┃ ┣ 📊 pr_curves/
 ┃ ┗ 📊 training_curves/
 ┣ 📜 requirements.txt
 ┣ 📜 config.yaml
 ┗ 📜 README.md
```

---

## ⚙️ Getting Started

### Prerequisites
```bash
Python >= 3.10
CUDA-compatible GPU (6GB+ VRAM recommended)
Eclipse SUMO >= 1.26.0
```

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/CAMAF-Traffic-Signal-Control.git
cd CAMAF-Traffic-Signal-Control

# Install dependencies
pip install -r requirements.txt

# Install SUMO (Ubuntu)
sudo apt-get install sumo sumo-tools sumo-doc
```

### Training the Detection Model
```bash
python detection/train.py \
  --epochs 50 \
  --imgsz 640 \
  --batch 8 \
  --conf 0.45 \
  --tracker botsort \
  --patience 10
```

### Running the Federated Simulation
```bash
# Terminal 1: Start aggregation server
python federated/server.py --rounds 10 --min-clients 3

# Terminal 2+: Launch edge node clients
python federated/client.py --node-id A --intersection-data data/nodeA/
python federated/client.py --node-id B --intersection-data data/nodeB/
```

### SUMO Traffic Simulation
```bash
python simulation/traci_control.py \
  --config simulation/sumo_env/demo.sumocfg \
  --mode camaf \
  --threshold 0.80
```

---

## 📈 Training Configuration

```yaml
# config.yaml
model:
  variant: yolov11n
  classes: 12
  imgsz: 640

training:
  epochs: 50
  batch_size: 8
  patience: 10
  conf_threshold: 0.45
  agnostic_nms: true
  tracker: botsort

federated:
  algorithm: FedProx
  framework: flower
  rounds: 10
  mu: 0.1           # FedProx proximal term
  bandwidth_per_node: "5-10MB"

coordination:
  downstream_threshold: 0.80
  alpha: 1.0         # density weight
  beta: 0.5          # wait-time weight
  gamma: 1.0         # emergency override weight
```

---

## 📚 Literature Context

This project builds on and extends:

| Year | Work | Contribution to CAMAF |
|:---|:---|:---|
| 1958 | Webster (Fixed-Time Model) | Baseline benchmark |
| 1995 | SCOOT | Network-level adaptive control reference |
| 2016 | YOLO (Redmon et al.) | Foundation of detection pipeline |
| 2020 | YOLOv4 (Bochkovskiy et al.) | Architecture evolution |
| 2020 | DRLE (Zhou et al.) | Decentralized RL inspiration |
| 2020 | FedProx (Li et al.) | Federated optimization strategy |
| 2023 | Shams et al. Taxonomy | Adaptive control classification |
| 2026 | **CAMAF (This Work)** | **End-to-end federated edge framework** |

---

## 👥 Team

<div align="center">

<table>
<tr>
<td align="center" width="220">
<b>Ishan Srivastav</b><br/>
<code>22BDA70073</code><br/>
<br/>
🔐 <b>Secure Systems & Integration Developer</b><br/>
<sub>AES-256 encryption · API integration · Hardware-software bridge · Key management system</sub>
</td>
<td align="center" width="220">
<b>Priyanshu Kumar Singh</b><br/>
<code>22BDA70093</code><br/>
<br/>
🚦 <b>Traffic Systems & Simulation Specialist</b><br/>
<sub>SUMO digital twin · Dynamic signal timing · Fixed vs. Adaptive comparative analysis</sub>
</td>
<td align="center" width="220">
<b>Aditya Jaswal</b><br/>
<code>22BDA70117</code><br/>
<br/>
🤖 <b>Computer Vision & AI Engineer</b><br/>
<sub>YOLOv11 fine-tuning · Edge inference optimization · BoT-SORT integration</sub>
</td>
</tr>
</table>

**Supervisor:** Ms. Sakshi &nbsp;|&nbsp; **HOD:** Mr. Aman Kaushik  
**Department:** AIT – CSE, Chandigarh University  
**Program:** BE Computer Science (Big Data Analytics) · 8th Semester · Jan–Apr 2026

</div>

---

## 🔭 Future Roadmap

- [ ] **Class Imbalance** — Focal loss tuning + synthetic augmentation for bus-l, bus-s classes
- [ ] **Emergency Detection** — Dedicated dataset collection for ambulance/fire engine detection
- [ ] **Multi-City Scaling** — Hierarchical cluster-based coordination for 100+ intersections
- [ ] **Federated RL** — Combine federated learning with reinforcement learning agents
- [ ] **Multi-modal Fusion** — GPS, IoT sensor, and weather data integration
- [ ] **Personalized Federation** — Adaptive models per intersection type (school zone, highway, commercial)
- [ ] **Explainability** — XAI layer for transparent signal decisions
- [ ] **AV Integration** — V2I communication interface for autonomous vehicle ecosystems

---

## 📄 Citation

If you use this work, please cite:
```bibtex
@project{camaf2026,
  title   = {Adaptive Traffic Signal Control System Using Real-Time Object Detection: The CAMAF Framework},
  author  = {Srivastav, Ishan and Singh, Priyanshu Kumar and Jaswal, Aditya},
  school  = {Chandigarh University, AIT -- CSE},
  year    = {2026},
  note    = {BE Computer Science (Big Data Analytics), 8th Semester Project}
}
```

---

<div align="center">

**Keywords:** `Adaptive Traffic Signal Control` · `Federated Learning` · `YOLOv11` · `BoT-SORT` · `Spatio-Temporal Graph` · `FedProx` · `Edge Computing` · `SUMO Simulation` · `Privacy Preservation` · `Multi-Agent Systems`

<br/>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer"/>

</div>
