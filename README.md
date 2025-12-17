# LLM Engineering Lab

Modern Python workspace for learning production LLM systems, featuring prompt management, evaluation frameworks, and shared utilities.

## 🚀 Quick Start

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Install dependencies
poe install

# 3. Run a project
poe run-playground
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup.

## 📦 Projects

### [common/](common/) - Shared Utilities
Reusable utilities across all projects:
- Environment variable loading with cascading (parent → project)
- Shared configurations

### [01-llm-playground/](01-llm-playground/) - Core LLM Client
Foundation for LLM interactions:
- `LLMClient`: OpenAI API wrapper
- `LLMRequest`: Request data model
- `Metrics`: Latency and cost tracking

### [02-prompt-registry/](02-prompt-registry/) - Prompt Management
Centralized prompt versioning and templating:
- YAML-based prompt storage
- Variable substitution (`{{format}}`)
- Version control for prompts

### [03-prompt-evaluation/](03-prompt-evaluation/) - A/B Testing
Compare prompt versions systematically:
- Multi-version testing
- Performance metrics
- Regression detection

## 🛠️ Development

### Available Tasks

```bash
poe list                # Show all tasks
poe run-playground      # Run LLM Playground
poe run-registry        # Run Prompt Registry  
poe run-evaluation      # Run evaluation suite
poe format              # Format code with Black
poe lint                # Lint code with Ruff
```

### Project Structure

```
llm-engineering-lab/
├── pyproject.toml           # Workspace config
├── common/                  # Shared package
├── 01-llm-playground/       # Core LLM client
├── 02-prompt-registry/      # Prompt management
└── 03-prompt-evaluation/    # Evaluation framework
```

## 🎯 Key Features

- **⚡ Fast**: Uses `uv` for 10-100x faster package installs
- **🎭 Automated**: `poe` tasks for common workflows
- **📦 Modern**: `pyproject.toml` standard packaging
- **🔒 Reproducible**: Consistent environments across machines

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Common Utils README](common/README.md)
- [Prompt Registry Guide](02-prompt-registry/README.md)
- [Evaluation Framework](03-prompt-evaluation/README.md)


## 📝 Requirements

- Python 3.12+
- UV package manager
- Poe task runner

## 🔧 Environment Setup

1. Create `.env` in repository root with shared credentials:
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

2. Optional: Create project-specific `.env` files to override defaults

---

**Author**: Devaraj  
**Email**: imddevaraj@gmail.com
