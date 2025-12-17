
# Pattern: LLM Client Abstraction

### Intent
Decouple application logic from LLM providers.

### Benefits

**Multi-model routing**
**Easier testing & mocking**
**Centralized observability**
**Safer prompt handling**

### Anti-Pattern

**❌ Calling LLM APIs directly from business logic**
**❌ Hardcoding prompts inside functions**

### ⚠️ Known Limitations (By Design)

**No retry logic**
**No cost computation**
**No output schema validation**
**No error handling abstraction**

These are intentionally deferred to future days to keep each artifact focused.

# Implementation

This is a **clean, modular LLM client** that wraps the OpenAI API with metrics tracking. The codebase follows software engineering best practices with separation of concerns and clear abstractions.

---

## 🏗️ Architecture Overview

```
┌─────────────┐
│   main.py   │ ← Entry point / Example usage
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  LLMClient      │ ← Orchestrates requests
└────────┬────────┘
         │
         ├──→ ┌──────────────┐
         │    │  LLMRequest  │ ← Data model
         │    └──────────────┘
         │
         ├──→ ┌──────────────┐
         │    │   OpenAI     │ ← External API
         │    └──────────────┘
         │
         └──→ ┌──────────────┐
              │   Metrics    │ ← Latency tracking
              └──────────────┘
```

---

## 🚀 How to Run

### Setup (First Time)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API key

# Edit .env and add your OpenAI API key
```

### Run the Main Example
```bash
cd src
python main.py
```



## 📊 Data Flow

```
User Input
   ↓
LLMRequest (structured data)
   ↓
LLMClient.execute()
   ↓
┌─────────────────────┐
│ Start Metrics       │
│ Call OpenAI API     │
│ Stop Metrics        │
└─────────────────────┘
   ↓
Response Dict {
    output: str,
    usage: TokenUsage,
    latency_ms: float,
    model: str
}
```

---

## 🔐 Configuration

The `.env` file should contain:
```bash
OPENAI_API_KEY=sk-...your-key-here...
```
## 🎯 Key Takeaways

✅ **Well-structured**: Clear separation between models, clients, and utilities  
✅ **Type-safe**: Uses dataclasses and type hints  
✅ **Maintainable**: Small, focused modules (10-30 lines each)  
✅ **Observable**: Tracks latency and token usage  
✅ **Configurable**: Environment-based configuration  
✅ **Documented**: Comprehensive README and test suite  

This is a solid foundation for LLM experimentation! 🚀
