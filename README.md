# 👻 GhostTrace  
### AI-Powered Local Privacy Auditor

GhostTrace is a desktop privacy auditing tool that scans local files for exposed sensitive information and helps users identify potential privacy risks before attackers do.

Built with Python, PyQt6, AI-based detection, and automated reporting.

---

## 🚀 Features

### 🔍 Local File Scanning
- Scan folders directly from your system
- Detect sensitive information inside documents
- Supports multiple file formats

### 🛡 Sensitive Data Detection
GhostTrace can identify:

- Password leaks
- API keys
- Email addresses
- Phone numbers
- Personal information patterns
- Other exposed secrets

---

## 🤖 AI Detection

Includes AI-powered entity detection to find sensitive information beyond simple pattern matching.

Detects possible:
- Names
- Personal identifiers
- Sensitive entities

---

## 📊 Privacy Risk Engine

GhostTrace calculates a privacy risk score based on detected exposure.

Includes:

- Files scanned
- Number of threats
- Risky files
- Overall security score

Risk levels:

🟢 LOW  
🟠 HIGH  
🔴 CRITICAL  

---

## 📈 Analytics Dashboard

Modern cybersecurity-style dashboard built using PyQt6.

Includes:

- Real-time scan statistics
- Risk overview charts
- Threat distribution graphs
- Separate advanced risk analysis window

---

## 📄 PDF Security Reports

Generate professional audit reports containing:

- Scan summary
- Risk score
- Threat analysis
- Security recommendations
- Graph visualizations

---

## ⚙ Custom Settings

GhostTrace includes a configurable settings system:

- Scan modes
  - Quick Scan
  - Deep Scan
  - Smart Detection

- File type filters

- AI detection toggle

- Report customization

- Risk sensitivity controls

---

## 🖥 Tech Stack

- Python
- PyQt6
- Matplotlib
- ReportLab
- Regex Detection
- NLP / AI Entity Detection
- JSON Configuration

---

## 📂 Project Structure

```text
GhostTrace
│
├── scanner/
│   ├── file_scanner.py
│   ├── regex_detector.py
│   ├── ai_detector.py
│   └── pdf_reader.py
│
├── reports/
│   └── report_generator.py
│
├── ui/
│   └── dashboard.py
│
├── settings.json
├── main.py
└── README.md
```

---

## ⚡ Installation

Clone the repository:

```bash
git clone https://github.com/mnemosyne-dev/GhostTrace.git
```

Move into project:

```bash
cd GhostTrace
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

## 📸 Screenshots

(Add dashboard screenshots here)

---

## 🎯 Goal

Modern systems store thousands of files containing forgotten credentials, documents, and private information.

GhostTrace helps users discover these risks locally before they become security incidents.

---

## 🔮 Future Improvements

- Encrypted privacy vault
- Background monitoring
- Real-time alerts
- More AI models
- Secure file quarantine
- Scan history

---

## Developer

Created by **Sunny Nayak**

GitHub:  
https://github.com/mnemosyne-dev

---

⭐ If you like this project, consider starring the repository.
