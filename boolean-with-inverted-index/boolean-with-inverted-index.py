import re
from collections import defaultdict

# Sample documents
documents = {
    "doc1": "Information retrieval systems use Boolean queries to find documents and data.",
    "doc2": "Boolean retrieval is fundamental to search engines.",
    "doc3": "Modern search engines use advanced algorithms beyond simple Boolean queries.",
    "doc4": "Data mining techniques are used for more complex search tasks.",
    "doc5": "Data mining is a subset of data science.",
    "doc6": "Data mining is used to discover patterns in large datasets.",
    "doc7": "Data mining is an interdisciplinary field."
}

def tokenize(text):
    """Tokenize the input text into a set of lowercase words."""
    return set(re.findall(r'\b\w+\b', text.lower()))

def build_inverted_index(docs):
    """
    Build an inverted index from a collection of documents.

    Args:
        docs (dict): A dictionary where keys are document IDs and values are the document texts.

    Returns:
        dict: An inverted index where keys are words and values are sets of document IDs containing the word.
    """
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = tokenize(text)
        for word in words:
            index[word].add(doc_id)
    return index

def boolean_retrieval(index, query):
    """
    Perform Boolean retrieval based on the inverted index.

    Args:
        index (dict): The inverted index.
        query (str): The Boolean query (supports AND, OR, and NOT operations).

    Returns:
        set: A set of document IDs that match the query.
    """
    query = query.lower()
    tokens = re.findall(r'\b\w+\b', query)
    
    # Initialize result_docs as a set of all document IDs
    result_docs = set(index.keys())
    
    # Process AND operations
    if 'and' in tokens:
        terms = query.split(' and ')
        result_docs = set(index.get(terms[0].strip(), set()))
        for term in terms[1:]:
            term = term.strip()
            result_docs = result_docs.intersection(index.get(term, set()))
    
    # Process OR operations
    elif 'or' in tokens:
        terms = query.split(' or ')
        result_docs = set()
        for term in terms:
            term = term.strip()
            result_docs = result_docs.union(index.get(term, set()))
    
    # Process NOT operations
    elif 'not' in tokens:
        terms = query.split(' not ')
        if len(terms) == 2:
            term_to_include = terms[0].strip()
            term_to_exclude = terms[1].strip() 
            
            include_docs = index.get(term_to_include, set())
            exclude_docs = index.get(term_to_exclude, set())

            result_docs = include_docs.difference(exclude_docs)
            
            print(f"Resulting documents after NOT operation: {result_docs}")  
    
    # Handle queries without Boolean operators
    else:
        result_docs = set()
        for token in tokens:
            result_docs = result_docs.union(index.get(token, set()))
    
    return result_docs

# Build the inverted index from the sample documents
inverted_index = build_inverted_index(documents)

# Example queries
queries = [
    "Boolean and retrieval",
    "Boolean or algorithms",
    "data not mining",
    "search engines"
]
#queries = input("Enter the queries: ")
#queries = queries.split(",")

# Perform retrieval for each query and print results
for query in queries:
    print(f"Query: '{query}'")
    results = boolean_retrieval(inverted_index, query)
    print("Results:", results)
    print("Documents:")
    for doc_id in results:
        if doc_id in documents:
            print(f"  {doc_id}: {documents[doc_id]}")
    print()
