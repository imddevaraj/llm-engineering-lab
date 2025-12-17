# 🛠️ Common Utilities

Shared utilities and tools used across all LLM Engineering Lab projects.

## 📦 What's Inside

### `env_loader.py`
Environment variable loader with **cascading override support**:
- Loads parent `.env` (repository root) for shared defaults
- Loads project-specific `.env` for overrides
- Eliminates hardcoded credentials across projects

## 🚀 Installation

### As Editable Package (Recommended)

From the repository root:

```bash
pip install -e common/
```

This makes the utilities importable from any project without `sys.path` hacks.

### Via requirements.txt

Add to your `requirements.txt`:

```
-e common/
```

Then:
```bash
pip install -r requirements.txt
```

## 💡 Usage

### Environment Loading

**In any project's `main.py`:**

```python
from common.env_loader import load_project_env

# Load both parent and project-specific .env files
PROJECT_ROOT = load_project_env(__file__)

# Now use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")
```

**What it does:**
1. Finds repository root (goes up `project_levels_up` levels)
2. Loads `llm-engineering-lab/.env` (shared defaults)
3. Searches for project-specific `.env` (overrides)
4. Returns path to project root for other path operations

## 🎯 Environment Cascading Pattern

### Structure
```
llm-engineering-lab/
├── .env                          # 🌍 Parent (shared defaults)
├── common/
│   └── env_loader.py
├── 01-llm-playground/
│   └── .env                      # 🔧 Project-specific overrides
├── 02-prompt-registry/
│   └── .env                      # 🔧 Project-specific overrides  
└── 03-prompt-evaluation/
    └── .env                      # 🔧 Project-specific overrides
```

### Priority

**Parent `.env` (repository root):**
```bash
OPENAI_API_KEY=sk-shared-key
DEFAULT_MODEL=gpt-4o-mini
TEMPERATURE=0.2
```

**Project `.env` (e.g., `03-prompt-evaluation/.env`):**
```bash
TEMPERATURE=0.7          # Overrides parent
EVALUATION_RUNS=100      # Project-specific
```

**Result:**
- `OPENAI_API_KEY` → from parent (shared)
- `DEFAULT_MODEL` → from parent (shared)
- `TEMPERATURE` → `0.7` (overridden by project)
- `EVALUATION_RUNS` → `100` (project-specific)

## 📚 API Reference

### `load_project_env(script_file, project_levels_up=2)`

Loads environment variables with cascading priority.

**Parameters:**
- `script_file` (str): Usually `__file__` from calling script
- `project_levels_up` (int): Levels to traverse up to find repo root
  - Default: `2` (for scripts in `project/src/main.py`)
  - Use `1` if script is in `project/main.py`

**Returns:**
- `Path`: Absolute path to project root

**Example:**
```python
from common.env_loader import load_project_env

# For script at: 03-prompt-evaluation/src/main.py
PROJECT_ROOT = load_project_env(__file__)
# Returns: /path/to/llm-engineering-lab/

# For script at: my-project/main.py  
PROJECT_ROOT = load_project_env(__file__, project_levels_up=1)
```

**Output:**
```
✓ Loaded parent env: /path/to/llm-engineering-lab/.env
✓ Loaded project env: /path/to/llm-engineering-lab/03-prompt-evaluation/.env
```

## 🔧 Development

### Adding New Utilities

1. Create new module in `common/`
2. Export in `common/__init__.py`:
   ```python
   from .env_loader import load_project_env
   from .new_module import new_function
   
   __all__ = ['load_project_env', 'new_function']
   ```
3. Changes are immediately available (editable install)

### Testing

```bash
# Test import
python -c "from common.env_loader import load_project_env; print('✓ Success')"

# Test functionality
cd 03-prompt-evaluation
python src/main.py
```

## ✅ Benefits

| Before | After |
|--------|-------|
| ❌ `sys.path` manipulation in every file | ✅ Clean imports |
| ❌ Hardcoded credentials | ✅ Centralized `.env` |
| ❌ Copy-paste utility functions | ✅ Shared package |
| ❌ No override mechanism | ✅ Project-specific customization |
| ❌ Poor IDE support | ✅ Full autocomplete |

## 📦 Package Info

- **Name**: `llm-engineering-common`
- **Version**: `0.1.0`
- **Dependencies**: `python-dotenv>=1.0.0`

## 🤝 Contributing

When adding utilities:
1. Keep them generic and reusable
2. Document parameters and return values
3. Add usage examples
4. Update this README

---

**Part of**: [LLM Engineering Lab](../README.md)
