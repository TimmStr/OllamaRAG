from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitterSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return cls._instance
