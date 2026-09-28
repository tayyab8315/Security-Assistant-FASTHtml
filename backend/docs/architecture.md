# Updated Intent Router

Flow:
User -> Conversation Manager -> Intent + Task Understanding LLM
-> Clarification OR Planner
-> Schema Retrieval
-> SQL Generator
-> Validator
-> Repair
-> Execute
-> Result Understanding

Important fixes:
1. Intent is not considered complete without task understanding.
2. Low confidence requests require clarification.
3. Ambiguous business terms are detected.
4. Conversation clarification is preserved.
