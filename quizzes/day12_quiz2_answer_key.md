# Day 12 — Quiz 2 answer key

1. An embedding maps text to a numeric vector intended to preserve useful similarity; cosine similarity compares vector direction.
2. `top-k` is the number of nearest candidates returned for the next stage or answer context.
3. Small chunks can lose context; large chunks add irrelevant text. Overlap can preserve boundary information but increases duplicate content and cost.
4. Source filename/document ID, page, chunk ID, section, timestamps/tenant where appropriate, and access-control metadata.
5. Usually sparse/lexical ranking such as BM25 with dense vector ranking; scores must be normalized or combined carefully.
6. It reorders candidates using a more focused relevance signal after a cheaper first pass.
7. Say that evidence is insufficient, avoid making up facts, and show what was retrieved when useful.
8. Documents can contain irrelevant or malicious instructions; retrieval gives evidence, not authority to change system behavior.
9. Context recall asks whether relevant evidence was retrieved; faithfulness asks whether the answer is supported by that evidence.
10. Examples: lexical overlap misses paraphrases, small labels are biased, rule-based outputs do not represent a live model, or a proxy is not equivalent to RAGAS.
