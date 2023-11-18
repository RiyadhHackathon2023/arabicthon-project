from langchain.utilities.wikipedia import WikipediaAPIWrapper

class WikipediaSource():
    def __init__(self, domain, n_docs):
        self.wikipediaAPI = WikipediaAPIWrapper()
        self.wikipediaAPI.doc_content_chars_max = 1000000000
        self.values = {"lang": "ar"}
        self.wikipediaAPI.validate_environment(self.values)
        self.domain = domain
        self.n_docs = n_docs
        self.docs = self.wikipediaAPI.load(self.domain)
    
    def get_title(self):
        return self.docs[0].metadata["title"]

    def get_summary(self):
        return self.docs[0].metadata["summary"]
    
    def get_content(self):
        return self.docs[0].page_content