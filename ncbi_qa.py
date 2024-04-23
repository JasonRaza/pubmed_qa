import requests
import random
import re

def fetch_data(theme, api_key):
    """Fetch data from PubMed based on the theme."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': theme,
        'retmode': 'json',
        'apikey': api_key,
        'retmax': 500  # Fetching more articles to increase chances of finding suitable data
    }
    response = requests.get(base_url, params=params)
    return response.json()

def extract_question(data, api_key):
    """Extract a question from the data."""
    ids = data['esearchresult']['idlist']
    if not ids:
        return "No data available for this theme.", None

    random.shuffle(ids)  # Shuffle to randomize the selection process
    details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    for random_id in ids[:10]:  # Limit to 10 to avoid excessive processing
        params = {
            'db': 'pubmed',
            'id': random_id,
            'retmode': 'json',
            'apikey': api_key
        }
        response = requests.get(details_url, params=params)
        details = response.json()

        article = details['result'][random_id]
        abstract = article.get('abstract', article['title'])
        sentences = re.split(r'(?<=[.!?]) +', abstract)
        theme_sentences = [sentence for sentence in sentences if ',' in sentence or len(sentence.split()) > 8]

        for chosen_sentence in theme_sentences:
            words = re.findall(r'\b\w+\b', chosen_sentence)
            suitable_words = [word for word in words if len(word) > 3 and word.lower() not in ["the", "and", "for", "with", "are", "is", "was", "were"]]
            if suitable_words:
                correct_answer = random.choice(suitable_words)
                question = chosen_sentence.replace(correct_answer, "...")
                return question, correct_answer

    return "Still unable to generate a specific question; please retry.", None