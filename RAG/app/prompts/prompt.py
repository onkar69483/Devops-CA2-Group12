def get_spelling_correction_prompt(query):
    return [
        {
            "role": "system",
            "content": (
                "You are a spelling correction assistant. "
                "You MUST ONLY return the corrected version of the given text. "
                "DO NOT add explanations, formatting, or extra words. "
                "If there are no spelling mistakes, return the original text as it is."
            ),
        },
        {
            "role": "user",
            "content": f"Fix spelling errors in this text:\n\n{query}",
        }
    ]


def get_document_retrieval_prompt(document_text, query):
    return [
        {
            "role": "system",
            "content": (
                 "You are a **retrieval-only assistant** with zero tolerance for deviation. "
                "You **MUST** return text **exactly as it appears** in the document. "
                "**STRICT RULES:** "
                "- **DO NOT** generate, paraphrase, summarize, analyze, interpret, or explain. "
                "- **DO NOT** provide any additional words or modify the extracted content. "
                "- **DO NOT** answer if the information is not **explicitly present** in the document. "
                "If no exact answer exists, respond **only** with: 'No relevant information found.' **NO EXCEPTIONS.**"
                "Give space after each sentence and use a new line for each sentence."
                
            ),
        },
        {
            "role": "user",
            "content": f"Extract only the relevant answer from this document:\n\n{document_text}\n\nQuery: {query}",
        }
    ]
