# DodoAi - Codiverse Telegram Chatbot

DodoAi is a smart support specialist bot for Codiverse on Telegram. It helps users start new projects, check project status, and answers general queries using AI.

## Features

- **🎯 Intelligent AI Routing**: Tier-based query classification system that automatically selects the most appropriate AI model based on query complexity (Simple/Medium/Complex)
- **🚀 Multi-Model Support**: Seamlessly integrates multiple AI providers (Groq, OpenRouter, Gemini) with automatic failover
- **💡 Cost Optimization**: Smart routing uses lightweight models for simple queries and premium models only for complex reasoning
- **⚡ Speed Optimization**: Fast responses (<1s) for simple queries using optimized 3B parameter models
- **🛡️ High Reliability**: Multi-tier fallback system ensures 99%+ uptime with automatic rate limit management
- **Lead Generation**: Collects user project details and saves them directly to Google Sheets
- **Project Tracking**: Generates a unique Codiverse Member ID (CMID) for users to track their project status

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/SpicychieF05/DodoAi_Codiverse.git
    cd DodoAi_Codiverse
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file with the following keys:
    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    
    # Multi-model configuration
    GROQ_API_KEY=your_groq_api_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    OPENROUTER_MODELS=model1:free,model2:free,model3:free
    GOOGLE_API_KEY=your_gemini_api_key
    
    # Google Sheets integration
    GOOGLE_SHEETS_CREDENTIALS=your_base64_encoded_service_account_json
    LEADS_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
    ```

## 🎯 Tier-Based Routing System

The bot uses an intelligent query classification system to route requests efficiently:

### Query Complexity Tiers

| Tier | Characteristics | Priority Models | Response Time |
|------|----------------|-----------------|---------------|
| 🟢 **Simple** | <15 words, basic questions, greetings | Llama 3.2 3B → WizardLM → DeepSeek | 0.5-1.5s |
| 🟡 **Medium** | 15-50 words, explanations, comparisons | DeepSeek → Gemini → Llama 3.2 | 1-3s |
| 🔴 **Complex** | >50 words, detailed reasoning, planning | Groq (70B) → Gemini → DeepSeek | 2-5s |

### Examples

```python
# Simple query → Routes to Llama 3.2 3B
"What is Python?"

# Medium query → Routes to DeepSeek
"Explain how async/await works in Python"

# Complex query → Routes to Groq Llama 3.3 70B
"Provide a comprehensive analysis with step-by-step reasoning..."
```

**📚 Full Documentation**: See [TIER_ROUTING_GUIDE.md](TIER_ROUTING_GUIDE.md) for complete details

**🧪 Testing**: Run `python test_tier_routing.py` or `python simulate_routing.py`

## Usage

Run the bot:

```bash
python agent.py
```
