# 🏗️ Ethos - AI Ethics Auditor for Supply Chain
## System Specification

## 1. System Architecture: "The Supervisor Pattern"
Ethos uses a hierarchical multi-agent system to ensure accuracy and separation of concerns.

- **The Supervisor (Orchestrator)**: Manages the user interaction and delegates work.
- **The Investigator (Worker A)**: Focused purely on information retrieval (Web/News).
- **The Auditor (Worker B)**: Focused purely on policy logic (RAG/Compliance).

## 2. Agent Definitions

### 🤖 Supervisor Agent
*   **Goal**: Coordinate the audit process.
*   **Input**: User query (e.g., "Audit Acme Corp").
*   **Logic**:
    1.  Call `Investigator` to get raw data.
    2.  Call `Auditor` with that data to get a score.
    3.  Format the final JSON for the UI.
*   **Output**: Final JSON Report.

### 🕵️ Investigator Agent
*   **Goal**: Gather external intelligence.
*   **Tools**: Mocked News Search / API.
*   **Behavior**:
    *   Search for: "Labor violations", "Environmental fines", "Strikes".
    *   Return: List of facts with sources and dates.

### ⚖️ Auditor Agent
*   **Goal**: Apply internal policy to facts.
*   **Tools**: Knowledge Base (`ethics_policy.txt`).
*   **Behavior**:
    *   Take the list of facts from the Investigator.
    *   Query the Knowledge Base: "Does [Fact X] violate our policy?"
    *   Assign a severity score (Minor/Major/Critical).

## 3. API Contracts (JSON)

### Interface: Investigator -> Supervisor
```json
{
  "supplier": "Acme Corp",
  "findings": [
    {
      "date": "2024-03-10",
      "source": "Global News",
      "snippet": "Fined $2M for river pollution."
    }
  ]
}