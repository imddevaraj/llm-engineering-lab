"""
LLM Playground - Core client and models

Provides:
- calculate: Calculator tool
"""

from .tools.calculator import calculate
from .tools.knowledge_base import lookup

__all__ = ["calculate","lookup"]
