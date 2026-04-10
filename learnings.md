Q1)What was wrong with my RAG and why?
Ans) My RAG was only answering on unstructured data and not calculated ones, so I used Pandas Agent. I created it by using LangChain function called create_csv_agent.
RAG uses semantic similarity search which cannot perform aggregations, counts, or date comparisons. It finds rows that look similar to the question — not rows that answer it mathematically.

Q2)What is the ReAct pattern?
Ans) Think- Act- Response loop

Q3)Why does the Pandas agent write Python code?
It writes the python code to make calculations, LangChain cannot do calculations its a large language model so it can actually write python code to do the calculation

Q4)What is the difference between a chain and an agent?
chain is like an assembly line, it follows the same steps everytime, no decision making of its own. agent is like a human analyst who chooses the approach based on the question, it thinks and understands the situation, which tool to use, reads the result.