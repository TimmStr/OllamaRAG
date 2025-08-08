from utils.constants import paper_prompt, document_retrieval_prompt, email_prompt, rag_prompt


def test_paper_prompt():
    user_question = "How is the weather in Frankfurt"
    documents = ["My favourite color is blue",
                 "Today will be sunny"]
    result = paper_prompt(user_question, documents)

    assert user_question in result
    assert all([doc in result for doc in documents])


def test_document_retrieval_prompt():
    query = "Frankfurt is a city in germany."
    image_desc_documents = ["Image of the Maintower in Frankfurt",
                            "Hamburg is beautiful."]
    result = document_retrieval_prompt(query, image_desc_documents)

    assert query in result
    assert all([doc in result for doc in image_desc_documents])


def test_email_prompt():
    content = "Hi how are you"
    result = email_prompt(content)
    assert content in result


def test_rag_prompt():
    question = "Who is the president of the USA?"
    documents = ["Barrack Obama is the president of the USA.",
                 "Merkel is the chancellor of germany"]
    result = document_retrieval_prompt(question, documents)

    assert question in result
    assert all([doc in result for doc in documents])
    rag_prompt(question, documents)
