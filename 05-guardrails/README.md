#  Guardrails & Output Validation

Theme: “Never trust raw LLM output.”

**Output Validation and Safety Guards for LLM Applications**

This project demonstrates how to add guardrails to LLM outputs through safety checking and schema validation.

Build a Guardrails layer that enforces:

- Structured outputs (JSON schema)
- Safe refusal patterns
- “I don’t know” behavior for uncertainty
- Post-generation validation

Benefit Hypothesis

- LLM outputs are validated, not assumed
- Unsafe responses are caught before use
- Your system behaves predictably under failure

Why This Matters (Production Reality)

In real systems:

- LLM output feeds APIs, workflows, agents
- One hallucinated field can:
    - Trigger wrong actions
    - Corrupt data
    - Cause incidents

Guardrails are non-negotiable for production AI.

## Features

### 🛡️ Safety Guards
- **Instruction Leak Detection**: Prevents exposure of system prompts
- **Pattern-Based Filtering**: Detects unsafe response patterns
- **Safe Refusal Recognition**: Identifies when the LLM appropriately refuses

### ✅ JSON Schema Validation
- **Structured Output Validation**: Ensures LLM output matches expected schema
- **Type Checking**: Validates data types (string, number, boolean)
- **Required Field Enforcement**: Ensures all required fields are present

### ⚙️ Pydantic Configuration
- Type-safe settings with automatic `.env` loading
- Configurable schema paths and file names
- Hierarchical environment variable search

**Output:**
```
Safety check: True ok
Schema valid: True
{
  "summary": "The CAP theorem states...",
  "confidence": 0.9,
  "sources_used": false
}
```
## Schema Definition

**explanation_schema.json:**
```json
{
  "type": "object",
  "properties": {
    "summary": { "type": "string" },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
    "sources_used": { "type": "boolean" }
  },
  "required": ["summary", "confidence", "sources_used"]
}
```

## Safety Patterns

The `SafetyGuard` currently detects:

| Pattern | Detection | Action |
|---------|-----------|--------|
| Instruction leak | `"as an ai model i was instructed"` | Block (unsafe) |
| System prompt | `"system prompt"` | Block (unsafe) |
| Ignore instructions | `"ignore previous instructions"` | Block (unsafe) |
| Safe refusal | `"i don't know"`, `"cannot determine"` | Allow (safe) |

## Future Enhancements

- **ML-based guards**: Use embeddings for semantic safety detection
- **PII detection**: Identify and redact personally identifiable information
- **Toxicity scoring**: Detect harmful or inappropriate content
- **Custom validators**: User-defined validation rules
- **Retry logic**: Auto-retry with corrected prompts on validation failure

## Learn More

Related projects:
- **01-llm-playground**: Core LLM client implementation
- **04-hallucination-lab**: Failure classification and detection
- **03-prompt-evaluation**: Prompt version evaluation

---

**Note**: This project uses simple heuristic-based guards on purpose. In production, consider ML-based guardrails like LlamaGuard, NeMo Guardrails, or Guardrails AI.
