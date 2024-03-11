import streamlit as st
import requests
import re

# Use the previously working version of API interaction
PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]

def fetch_perplexity_results(topic):
    """
    Fetch results from the Perplexity AI based on the topic.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": topic}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 1.0,
        "presence_penalty": 0.0
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return remove_repetitive_content(content)
    else:
        st.error(f"Failed to fetch data from Perplexity API. Status: {response.status_code}, Response: {response.text}")
        return None

def remove_repetitive_content(content):
    """
    Simple heuristic to identify and remove repetitive sentences or phrases.
    """
    sentences = set(re.split(r'(?<=[.!?]) +', content))
    return ' '.join(sentences)

def main():
    st.title("Content Generator")

    topic = st.text_input("Insert Topic Prompt", "")
    
    if st.button("Generate"):
        if not topic:
            st.warning("Please insert a topic prompt.")
        else:
            cleaned_content = fetch_perplexity_results(topic)
            if cleaned_content:
                st.write(cleaned_content)
            else:
                st.write("No results found.")

if __name__ == "__main__":
    main()
