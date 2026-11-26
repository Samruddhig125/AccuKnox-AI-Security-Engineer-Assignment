# Assignment 3

**Project Link:** https://github.com/Samruddhig125/enterprise-rag-intelligence

### Why Building This Was Hard

1. **Enforcing permissions before the LLM sees anything:** Role-based access control (RBAC) had to happen directly inside the vector search filter if a restricted document chunk ever makes it into the prompt context, trying to scrub it out after the model generates an answer is already too late.
2. **Routing mixed file formats reliably:** One user question might pull facts from policy PDFs, tabular CSVs, and structured JSON logs all at once, meaning the query router had to figure out which ingestion and lookup path to trigger so the model wouldn't hallucinate a confident but wrong answer.
3. **Measuring quality without a built-in accuracy score:** Unlike standard ML models where you can just check an F1 score or loss curve, RAG doesn't give you an obvious metric out of the box ,so I had to put together my own evaluation set of test questions just to verify whether changing chunk sizes or retrieval rules actually helped or only looked good on one or two examples.
