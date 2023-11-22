from src.llm_agents.extractors.examples.terms_examples import terms_examples
from src.llm_agents.extractors.cohere_extractor import cohereExtractor

class cohereTermsExtractor(cohereExtractor):
    def __init__(self):
        super().__init__()
        self.examples = [e[1] for e in terms_examples]
        self.example_labels = [e[0] for e in terms_examples]
        self.example_prompt = "Extract in Arabic all the domain-specific terms from the text: "
    
    def extract(self, example):
        extracted = super().extract(example)
        return extracted.split(',')