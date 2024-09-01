import streamlit as st
import re
from collections import defaultdict


def tokenize(text):
    
    return set(re.findall(r'\b\w+\b', text.lower()))

def build_inverted_index(docs):
   
    index = defaultdict(set)
    for doc_id, text in docs.items():
        words = tokenize(text)
        for word in words:
            index[word].add(doc_id)
    return index

def boolean_retrieval(index, query):
   
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



# Initialize session state variables if they don't exist
if "file_dict" not in st.session_state:
    st.session_state.file_dict = {}
if "processed_results" not in st.session_state:
    st.session_state.processed_results = None
if "queries_input" not in st.session_state:
    st.session_state.queries_input = ""
if "inverted_index" not in st.session_state:
    st.session_state.inverted_index = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "upload"

# Function to switch pages
def switch_page(page_name):
    st.session_state.current_page = page_name

# Page 1: File Upload
if st.session_state.current_page == "upload":
    st.header("Upload Files")
    uploaded_files = st.file_uploader('Select files', type=['txt'], accept_multiple_files=True)

    if uploaded_files:
        # Populate the session state dictionary with uploaded files
        for uploaded_file in uploaded_files:
            file_content = uploaded_file.read().decode()
            st.session_state.file_dict[uploaded_file.name] = file_content

    # Button to process files and switch to query input page
    if st.button("Process Files"):
        if len(st.session_state.file_dict) < 2:
            st.warning("Please upload at least two files.")
        else:
            st.session_state.processed_results = "Files processed successfully!"
            st.write(st.session_state.processed_results)

            # Build the inverted index and store in session state
            st.session_state.inverted_index = build_inverted_index(st.session_state.file_dict)

            # Switch to the next page
            switch_page("query")

# Page 2: Query Input
elif st.session_state.current_page == "query":
    st.header("Enter Queries")

    st.session_state.queries_input = st.text_input(
        "Enter the queries:",
        placeholder="e.g., Boolean and retrieval, Boolean or algorithms, data not mining, search engines"
    )

    # Process the queries after the submit button is clicked
    if st.button("Submit Queries"):
        if st.session_state.queries_input:
            st.write("**Results:**")
            queries = [query.strip() for query in st.session_state.queries_input.split(",")]

            for query in queries:
                st.write(f"**Query:** '{query}'")
                results = boolean_retrieval(st.session_state.inverted_index, query)
                st.write("**Results:**", results)
                st.write("**Documents:**")
                for doc_id in results:
                    if doc_id in st.session_state.file_dict:
                        st.write(f"  **{doc_id}:** {st.session_state.file_dict[doc_id]}")
        else:
            st.warning("Please enter a query before submitting.")

    if st.button("Back to Upload"):
        switch_page("upload")