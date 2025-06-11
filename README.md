Of course, here is your updated "readme" file with the images integrated to provide a more visual and engaging overview of your project.

-----

# Commercial Manager Assistant

A sophisticated, multi-module portfolio application built with Python and Streamlit, designed to showcase a suite of AI-powered tools that augment the capabilities of a Commercial Manager in the telecommunications industry.

This project demonstrates the ability to translate complex business requirements from a real-world job description into a functional, enterprise-grade web application. It integrates a robust PostgreSQL backend, advanced AI-driven analysis via the Anthropic API, and a professional, user-centric frontend based on UX research and B2B design principles.

-----

## 🖼️ Application Preview

Here's a sneak peek at the Commercial Manager Assistant in action:

**Main Dashboard providing a daily overview and quick actions.**
\<img width="1363" alt="Image" src="[https://github.com/user-attachments/assets/315bb006-bfb8-416f-873d-33d791063ab9](https://github.com/user-attachments/assets/315bb006-bfb8-416f-873d-33d791063ab9)" /\>

**AI-powered analysis of an uploaded contract, identifying risks and extracting key terms.**
\<img width="1360" alt="Image" src="[https://github.com/user-attachments/assets/8667e52f-8ae7-414f-ac99-35237371c631](https://github.com/user-attachments/assets/8667e52f-8ae7-414f-ac99-35237371c631)" /\>

**The TCO & Pricing Optimization module in action.**
\<img width="1179" alt="Image" src="[https://github.com/user-attachments/assets/18ac9e66-406a-4095-8a24-f0f410a69d85](https://github.com/user-attachments/assets/18ac9e66-406a-4095-8a24-f0f410a69d85)" /\>

**Partner performance dashboard tracking KPIs.**
\<img width="1348" alt="Image" src="[https://github.com/user-attachments/assets/a459f717-8c63-4280-a0a9-8f28dc5027e0](https://github.com/user-attachments/assets/a459f717-8c63-4280-a0a9-8f28dc5027e0)" /\>

**Preliminary risk assessment for an RFx document.**
\<img width="1117" alt="Image" src="[https://github.com/user-attachments/assets/f1ebe1dd-994d-411f-a378-9f358feb4ebd](https://github.com/user-attachments/assets/f1ebe1dd-994d-411f-a378-9f358feb4ebd)" /\>

\<img width="1366" alt="Image" src="[https://github.com/user-attachments/assets/ef96484c-e7fd-4ea4-aacc-ed7b0fe84ba2](https://github.com/user-attachments/assets/ef96484c-e7fd-4ea4-aacc-ed7b0fe84ba2)" /\>

\<img width="1363" alt="Image" src="[https://github.com/user-attachments/assets/c1edad96-5d6a-47b8-9bdc-4c1df968c28d](https://github.com/user-attachments/assets/c1edad96-5d6a-47b8-9bdc-4c1df968c28d)" /\>

-----

## ✨ Features

This application is composed of four distinct, integrated modules, each designed to address a core responsibility of a Commercial Manager:

### 📄 1. AI Contract Lifecycle Management (CLM)

  * **PDF Upload & Analysis**: Users can upload PDF contract documents directly for analysis.
  * **AI-Powered Risk Assessment**: Utilizes the Claude API to analyze contract text for telecom-specific risks, focusing on critical clauses like SLAs, Liability Caps, and IP Rights.
  * **Key Term Extraction**: Automatically extracts and displays key commercial terms (e.g., Renewal Dates, Payment Terms) from the contract.
  * **Dynamic Database Integration**: Saves all analyzed contracts and their key terms to a PostgreSQL database, with the main contract list updating in real-time.

### 📊 2. TCO & Pricing Optimization Tool

  * **Comprehensive TCO Calculator**: A detailed calculator for software-based mobile solutions, factoring in acquisition, operational, and personnel costs over a 5-year period.
  * **AI-Driven Strategy Recommendation**: Uses the calculated TCO and customer segment data to get strategic advice from an AI on the optimal commercial model (e.g., Tiered Subscription, Usage-Based).

### 🤝 3. Partner & Reseller Portal

  * **Performance Dashboard**: A real-time dashboard that pulls data from the database to track a partner's performance against their contractual KPIs (e.g., sales revenue, technical certifications).

### ⚙️ 4. RFx Response Automation System

  * **Preliminary Risk Assessment**: A dashboard that displays pre-assessed risks associated with a specific RFx document, demonstrating how data can inform bid/no-bid strategy.

-----

## 🔗 Seamless Integration

  * **Cross-Module Workflow**: The application demonstrates integrated workflows, such as a button in the contract list to initiate a TCO analysis for a specific client, passing the context between modules.

-----

## 🛠️ Tech Stack

  * **Backend & Frontend**: Python 3.10+, Streamlit
  * **Database**: PostgreSQL
  * **AI Integration**: Anthropic Claude API
  * **PDF Processing**: PyPDF2
  * **Environment Management**: python-dotenv, venv

-----

## 🚀 Setup and Installation

Follow these steps to run the project locally on macOS.

### Prerequisites

  * Python 3.9+
  * Homebrew
  * PostgreSQL
  * An Anthropic API Key stored in a `.env` file.

### 1\. Clone the Repository

```bash
git clone https://github.com/krmhstrk/commercial-manager-assistant.git
cd commercial-manager-assistant
```

### 2\. Set Up the Environment

Create and activate a Python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

Install all required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4\. Set Up the PostgreSQL Database

Make sure the PostgreSQL service is running and create the project database.

```bash
brew services start postgresql
createdb portfolio_db
```

**Note**: If you get an error that the database already exists, you can safely ignore it.

### 5\. Configure Environment Variables

Create a `.env` file in the root of the project directory. Add your Anthropic API key to this file. This file is not tracked by Git.

```
ANTHROPIC_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

-----

## ▶️ How to Run

With the virtual environment activated and the database running, start the Streamlit application:

```bash
streamlit run app.py
```

Open your web browser and navigate to `http://localhost:8501`. The application should be live. The database tables and sample data will be created automatically on the first run.