VIGIL: Neural Command for Civic Governance 🛡️
A Proactive Multimodal AI Agent for Smart Cities
VIGIL is a high-performance civic intelligence system that bridges the gap between urban infrastructure failures and administrative resolution. Built for the Gemini Live Agent Challenge, it leverages Gemini 1.5 Flash to transform citizen-reported evidence into legally-sound civic petitions and automated governance workflows.

🚀 Live Production Environment
Deployment URL: https://vigil-agent-691568831059.us-central1.run.app
Infrastructure: Fully containerized Docker environment running on Google Cloud Run.

🧠 Core Technical Architecture
VIGIL utilizes a sophisticated multimodal stack to ensure high accuracy and proactive resolution:
Multimodal Reasoning (Vision + Logic): Uses Gemini 1.5 Flash (via Vertex AI) to analyze image evidence, calculate "Risk Scores," and identify the responsible government department.
Live Voice Interface: Features a bilingual (English/Hindi/Telugu) voice agent powered by Google Cloud Speech-to-Text V2 and Text-to-Speech (Neural2) for hands-free reporting.
Proactive Lifecycle Management:
Automated Scheduling: Uses the Google Calendar API to inject resolution deadlines into the user's schedule based on the AI's predicted time-frame.
Communication Automation: Automatically generates Gmail Drafts addressed to the specific regional department head (e.g., District Collector or PWD Engineer).
Evidence Integrity: Implements SHA-256 hashing for every piece of uploaded evidence to ensure document integrity in legal escalations.

✨ Key Features 
Legal Awareness: The agent cites specific Indian Laws and handles tiered escalation logic, from initial reports to RTI (Right to Information) drafts and Lokayukta notices.
Geospatial Intelligence: Automatically extracts EXIF GPS coordinates from photos to pinpoint infrastructure failures on a real-time map.
Bilingual Support: Full support for regional Indian languages (Neural2 natural female voices) to ensure inclusivity for all residents.
Gamified Governance: Features a "Vigil Points (VP)" and "XP" system to reward active citizenship and successful resolutions.

🛠️ Tech Stack
Language: Python 3.9+
Framework: Streamlit
AI/ML: Google Generative AI (Gemini 1.5 Flash)
APIs: Google Maps, Google Calendar, Gmail, Google Cloud TTS/STT
Containerization: Docker & Google Artifact Registry