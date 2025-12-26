# Multi-Agent Study Planner (Google ADK + LM Studio)

## Overview

This project implements a **multi-agent study assistant** using **Google Agent Development Kit (ADK)** and **LM Studio–hosted LLMs** (e.g. Qwen 2.5).

The system decomposes a user’s study request into multiple sequential stages:

1. **Planning & Research**
2. **Content Generation**
3. **Quiz Generation**
4. **Review & Quality Assurance**

Agents are orchestrated using `SequentialAgent`, with explicit context passing between agents to ensure deterministic and web-safe execution.

---

## Architecture

### High-Level Flow

```text
User Request
   ↓
Planner & Research Agent
   ↓
Content Creation Agent
   ↓
Quiz Generation Agent
   ↓
Reviewer Agent
   ↓
Final Output
```

Each agent:

* Has a single responsibility
* Consumes outputs from previous agents
* Produces a structured artifact for the next stage

---

## Key Design Decisions

### 1. No Implicit Context Variables

* The system **does not rely on `root_input`**
* All context is passed explicitly via agent outputs
* This guarantees compatibility with:

  * `adk web`
  * CLI execution
  * API-based execution

### 2. Sequential Deterministic Execution

* Uses `SequentialAgent`
* Ensures predictable ordering and reproducibility
* Avoids race conditions common in parallel agent graphs

### 3. Model-Agnostic Design

* Uses `LiteLlm` for compatibility with:

  * LM Studio
  * Local OpenAI-compatible servers
* Avoids Gemini-only assumptions in agent logic

---

## Agents Description

### 1. Planner & Research Agent

**Purpose**

* Breaks down the study task
* Performs research using available tools
* Produces a structured study plan

**Output**

* `research_output`

---

### 2. Content Agent

**Purpose**

* Converts the research plan into comprehensive study material
* Organizes content into logical sections

**Input**

* `planner_research_agent.research_output`

**Output**

* `content_output`

---

### 3. Quiz Agent

**Purpose**

* Generates assessment questions
* Covers key concepts from the study material

**Input**

* `content_agent.content_output`

**Output**

* `quiz_output`

---

### 4. Reviewer Agent

**Purpose**

* Evaluates coverage and completeness
* Identifies gaps and suggests improvements

**Inputs**

* Research plan
* Study content
* Quiz output

**Output**

* `review_output`

---

## Technology Stack

* **Python 3.10+**
* **Google ADK**
* **LM Studio**
* **LiteLLM**
* **Qwen 2.5 (recommended)**

---

## Prerequisites

* Python 3.10 or newer
* LM Studio running locally
* An OpenAI-compatible inference server exposed by LM Studio

---

## Environment Variables

Create a `.env` file or set environment variables:

```env
MODEL_NAME=qwen2.5:7b-instruct
BASE_URL=http://localhost:1234/v1
API_KEY=lm-studio
```

> `API_KEY` can be any non-empty value for LM Studio.

---

## Running the Application

### Start the ADK Web Server

```bash
adk web
```

Then open the localhost page:

```
http://127.0.0.1:8000/
```

Select the app and submit a study request.

---

## Known Limitations

* `GoogleSearchAgentTool` is **Gemini-oriented**
* Tool invocation may be inconsistent with non-Gemini models
* For production use, replace with:

  * Local search tools
  * Tavily / SerpAPI
  * Vector database retrieval

---

## Recommended Improvements

* Replace Google search with deterministic `FunctionTool`
* Add JSON or schema-based outputs
* Parallelize research sub-tasks
* Introduce caching for repeated study topics
* Add formal input/output contracts per agent

---

## Status

**Stable for development and experimentation**
**Production hardening recommended for tooling and output schemas**

---

## License

MIT License (or your preferred license)
