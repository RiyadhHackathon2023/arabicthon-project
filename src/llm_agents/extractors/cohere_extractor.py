import cohere

class cohereExtractor():
    def __init__(self):
        self.api_key = 'p9jFscVEhxLVDMI8sqCU4JX2STAVMAFUUja2SgXg'
        self.co = cohere.Client(self.api_key)
        self.labels = []
        self.examples = []
        self.example_labels = []
        self.example_prompt = ""
        self.task_desciption = ""

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join( [examples[i] + "\n" +
                                self.example_prompt + 
                                 labels[i] for i in range(len(examples))]))

    def extract(self, example):
      extraction = self.co.generate(
          prompt=self.make_prompt(example),
          temperature=0.1,
          stop_sequences=["\n"])
      return(extraction.generations[0].text)