# Tools & ReAct Pattern

**Reasoning and Acting: Building Agentic LLMs with Tool Use**

This project demonstrates the ReAct (Reasoning + Acting) pattern, where an LLM can reason about problems and use tools to gather information or perform actions.

## Theme: "“Reason → Act → Observe → Decide. Give LLMs hands and feet" 

Build a Tool-Enabled Agent using the ReAct pattern, where the LLM:

- Reasons about a task
- Chooses a tool
- Executes the tool
- Observes the result
- Produces a final answer

Benefit Hypothesis

- The LLM is not just generating text
- It can invoke deterministic tools
- You can trace why an action happened

Why This Matters (Production Reality)

LLMs alone are:

- Non-deterministic
- Unverifiable
- Unsafe for direct action

Tools bring determinism.

Real systems require:

- Database queries
- API calls
- Calculations
- Configuration lookups

ReAct is the bridge between reasoning and execution.

The ReAct pattern enables LLMs to:
- **Reason** about complex problems step-by-step
- **Act** by using external tools (calculator, search, APIs, etc.)
- **Observe** the results of actions
- **Decide** what to do next based on observations

## Features

### 🧠 ReAct Agent
- **Structured Reasoning Loop**: Thought → Action → Observation → Final
- **Tool Selection**: Agent decides which tool to use based on the question
- **Multi-step Reasoning**: Can use multiple tools in sequence

### 🛠️ Tool System
- **Tool Registry**: Manages available tools and their descriptions
- **Calculator Tool**: Evaluates mathematical expressions
- **Knowledge Base Tool**: Looks up distributed systems concepts
- **Extensible**: Easy to add new tools

## Project Structure

```
06-ReAct-pattern/
├── src/
│   ├── agent/
│   │   └── react_agent.py      # ReAct agent implementation
│   ├── registry/
│   │   └── tool_registry.py    # Tool management
│   └── main.py                  # Demo application
├── tools/
│   ├── calculator.py            # Math evaluation tool
│   └── knowledge_base.py        # Concept lookup tool
└── README.md
```

## Installation

```bash
# From project root
poe install
```

## Usage

### Run the Demo

```bash
poe run-react
```

**Example Output:**
```
Thought: I need to evaluate the mathematical expression 2 + 2 * 5 first...

Action: calculator[2 + 2 * 5]
Observation: 12

Action: knowledge_base[CAP]
Observation: CAP stands for Consistency, Availability, and Partition Tolerance...

Final: The result of 2 + 2 * 5 is 12, and CAP refers to Consistency, 
Availability, and Partition Tolerance in distributed systems.
```

## How It Works

### 1. Agent Initialization

```python
from agent.react_agent import ReActAgent

agent = ReActAgent(client, tools.list_tools())
```

### 2. Tool Registration

```python
tools = ToolRegistry()

tools.register(
    name="calculator",
    description="Evaluate mathematical expressions",
    fn=calculate
)

tools.register(
    name="knowledge_base",
    description="Lookup basic distributed systems knowledge",
    fn=lookup
)
```

### 3. Agent Execution

```python
question = "What is 2 + 2 * 5 and what does CAP mean?"
output = agent.run(question)
```

## ReAct Format

The agent follows a strict format instructed in the system prompt:

```
Thought: [reasoning about the problem]
Action: tool_name[input]
Observation: [result from tool]
Final: [final answer]
```

This format helps the LLM:
- **Think** before acting
- **Use tools** when needed
- **Observe** results
- **Synthesize** a final answer

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `calculator` | Evaluate mathematical expressions | `calculator[2 + 2 * 5]` → `12` |
| `knowledge_base` | Lookup distributed systems concepts | `knowledge_base[CAP]` → `CAP theorem states...` |

## Adding New Tools

1. **Create tool function:**
```python
def my_tool(input_str: str) -> str:
    # Process input
    return result
```

2. **Register with registry:**
```python
tools.register(
    name="my_tool",
    description="Description for LLM to understand when to use this tool",
    fn=my_tool
)
```

3. **Agent automatically has access!**

## Why ReAct Matters

### Traditional LLMs:
- Limited to training data knowledge
- Can't perform computations
- Can't access real-time information
- Prone to hallucination on facts

### ReAct Pattern:
✅ Can use calculators for accurate math  
✅ Can search knowledge bases for facts  
✅ Can call APIs for real-time data  
✅ Can use databases for historical data  
✅ Reduces hallucination by grounding responses in tool outputs

## Production Considerations

### Current Implementation (Demo):
- **Simple regex parsing** to extract actions
- **No error recovery** if LLM doesn't follow format
- **Limited tools** (calculator + knowledge base)
- **Single-turn reasoning** (no multi-step loops)

### Production Enhancements:
- **Robust parsing**: Handle malformed LLM outputs
- **Error recovery**: Retry with feedback if tool fails
- **Multi-turn loops**: Allow agent to use multiple tools iteratively
- **Tool validation**: Validate inputs before execution
- **Safety checks**: Prevent dangerous tool usage
- **Observability**: Log all tool calls and reasoning steps

## Future Enhancements

- **Web Search Tool**: Real-time web search capability
- **Database Tool**: Query structured data
- **API Tools**: Call external APIs (weather, news, etc.)
- **File System Tools**: Read/write files
- **Multi-step Loops**: Allow agent to reason across multiple turns
- **Tool Chaining**: Automatically chain compatible tools
- **Guardrails**: Prevent unsafe tool usage

## Learn More

Related projects:
- **01-llm-playground**: Core LLM client used by the agent
- **05-guardrails**: Output validation (can validate tool inputs/outputs)

---

**Note**: This is a simplified ReAct implementation for learning. Production frameworks like LangChain, LlamaIndex, or Semantic Kernel provide more robust implementations with error handling, observability, and extensive tool libraries.

## References

- [ReAct Paper (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) - Original research
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/) - Production framework
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) - Native tool use
