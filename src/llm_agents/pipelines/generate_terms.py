from src.llm_agents.scrapers.playwright_sync import get_paragraphs
from src.llm_agents.sources.wikipedia import WikipediaSource
from src.llm_agents.extractors.cohere_terms_extractor import cohereTermsExtractor
from src.neo4j_db.neo4j_connection import Neo4jConnection
from src.llm_agents.classifiers.classify_definition import classify_definition
from src.llm_agents.utils import keep_arabic


def generate_terms(worker_id="",
                         domain="",
                         sources=[{
                             "type": "",
                             "content": ""
                         }],
                         task='key_terms',
                         words=[]):
    for source in sources:
        print(source["type"])
        if source["type"] == "Url":
            input_paragraphs = get_paragraphs(source["content"])
        elif source["type"] == "Wikipedia":
            wiki = WikipediaSource(domain=domain, n_docs=1)
            input_paragraphs = wiki.get_content()
        elif source["type"] == "File":
            input_paragraphs = source["content"]

        extractor = cohereTermsExtractor()

        conn = Neo4jConnection(
            uri='neo4j+s://5e2c94ef.databases.neo4j.io',
            user='neo4j',
            pwd='E53hCDHJjVnO8aTLMejfxtmz1G7q9LplVVO6K5L6drg')
        print('Scraping...')
        for paragraph in input_paragraphs:
            print("\nPARAGRAPH", paragraph)
            paragraph = paragraph.replace('\'', '')
            paragraph = paragraph.replace('\"', '')
            print("REPLACED", paragraph)
            extracted_text = extractor.extract(paragraph)
            for word in extracted_text:
                if word not in ["", "لا شيء"]:
                    word = keep_arabic(word)
                    conn.add_word(worker_id, word, domain, task)
                    print(word)

        conn.close()
    return "OK"