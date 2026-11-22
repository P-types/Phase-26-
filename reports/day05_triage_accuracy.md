# Day 5 triage sample run

- Synthetic complaints: 20
- Outputs parsed and Pydantic-validated in offline mock mode: 20/20
- Equipment labels matching the hand-written expected labels: 20/20
- Urgency labels matching the hand-written expected labels: 15/20

This measures only the deterministic offline rule baseline against its synthetic labels. It is not an LLM accuracy score. The CSV is the accuracy sheet template to complete again with a live model after an approved API key is configured. No real device or clinical data was used.
