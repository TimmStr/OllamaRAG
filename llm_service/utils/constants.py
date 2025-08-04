MAIL_HOST = "MAIL_HOST"
MAIL_PORT = "MAIL_PORT"
MAIL_USER = "MAIL_USER"
MAIL_PASSWORD = "MAIL_PASSWORD"
OLLAMA_TEST_SERVER_URL = "OLLAMA_TEST_SERVER_URL"

CONFLUENCE_EXAMPLE_QUERY = "Can you explain the design decisions behind our customer churn prediction model, and point me to the relevant Confluence pages where this is documented?"


def paper_prompt(user_question, retrieved_documents):
    return f"""You are a knowledgeable research assistant specialized in deep learning, machine learning, and related scientific papers.
            You will be given one or more user questions along with retrieved text passages from relevant research papers, technical reports, or documentation provided by a RAG system.
            Your task:
                Answer the question as accurately and precisely as possible, using only the information found in the retrieved passages.
                If the answer depends on specific papers or models, clearly mention the relevant paper names or authors if available.
                If the information in the retrieved passages is insufficient, say so honestly (e.g., "The retrieved documents do not provide enough information to answer this question conclusively.").
                Avoid adding extra assumptions or external knowledge not grounded in the retrieved text.
                Keep the explanation clear, concise, and technically correct.
            
            Question:
            {user_question}
            
            Retrieved passages:
            {retrieved_documents}"""


def document_retrieval_prompt(result, image_documents):
    return f"""
            You are an expert document retrieval assistant.  
            Given the following text and a list of available documents (with their paths), identify which documents are most relevant to the text.

            Please return **only** the file paths of the relevant documents as a JSON array, for example:
            ["/path/to/doc1", "/path/to/doc2"]

            Do not include any explanation or extra text.

            Text to match:
            {result}

            Available documents:
            {image_documents}"""

def email_prompt(email_content):
    return f"""
    You are a professional business writing assistant.
    I will provide you with the content of an email I received.
    Your task is to write an appropriate, professional, and polite reply in English.
    Please keep your reply:
        Clear and concise
        Matching the tone and context of the original email
        Grammatically correct and natural sounding
    If necessary, include greetings and sign-off.
    
    
    Return your answer in the following format:
    Mail: [your reply message]
    Subject: [the subject line of your reply]
    
    Here is the email you should reply to:
    
    {email_content}
    """