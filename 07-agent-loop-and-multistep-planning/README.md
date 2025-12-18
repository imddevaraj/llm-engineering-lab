#  Agent Loop & Multi-Step Planning

##  Objective

Transform a ReAct-style prompt into a **true autonomous agent**
by implementing an execution loop that reasons, acts, observes,
and repeats until completion.

---

##  Problem Statement

Single-shot ReAct prompts do not execute actions.
Without a loop:
- Tools are never invoked
- State is lost
- Agents are not autonomous

---

##  Solution Overview

This module introduces:
- A deterministic agent loop
- Action parsing
- Tool execution
- Observation feedback
- Step limits for safety

---

##  Agent Loop Flow

