from langchain_huggingface import HuggingFaceEmbeddings

from utils.logging_config import exception_handling

model_kwargs = {"device": "cuda:0"}
encode_kwargs = {"normalize_embeddings": True}


@exception_handling
def mini_embedder():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                 model_kwargs=model_kwargs,
                                 encode_kwargs=encode_kwargs)


@exception_handling
def multi_lingual_embedder():
    return HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large",
                                 model_kwargs=model_kwargs,
                                 encode_kwargs=encode_kwargs)
