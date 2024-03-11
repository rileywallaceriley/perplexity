import streamlit as st
import requests
import re

# Assuming your Perplexity API key is stored securely
PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]

def fetch_perplexity_results(topic, content_type, quantity):
    """
    Fetch results from the Perplexity AI based on the topic, content type, and quantity.
    Adjusted parameters for higher content quality and added repetition filtering.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {
        "model": "mistral-7b-instruct",  # Consider using the highest quality model available
        "messages": [
            {"role": "system", "content": f"Generate {quantity} high-quality {content_type.lower()} about {topic}."},
            {"role": "user", "content": topic}
        ],
        "max_tokens": 1024,  # Adjust for longer content
        "temperature": 0.5,  # Lower for more deterministic output
        "top_p": 1.0,
        "frequency_penalty": 2.0,  # Increase to reduce repetition
        "presence_penalty": 1.0  # Encourage new topics
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return remove_repetitive_content(content)
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return None

def remove_repetitive_content(content):
    """
    Basic filter to remove repetitive sentences or phrases from the generated content.
    """
    sentences = re.split(r'(?<=[.!?]) +', content)
    seen = set()
    filtered_sentences = []
    for sentence in sentences:
        if sentence not in seen:
            filtered_sentences.append(sentence)
            seen.add(sentence)
    return ' '.join(filtered_sentences)

def main():
    st.title("Enhanced Content Generator")

    topic = st.text_input("Insert Topic Prompt", "")
    
    content_type = st.selectbox("Select Content Type", ["Blog Post", "News Blurbs", "Social Media Posts"])
    
    if content_type in ["News Blurbs", "Social Media Posts"]:
        blurb_options = [1, 3] if content_type == "News Blurbs" else [1, 5, 10, 15, 20, 30]
        quantity = st.select_slider("How many items do you need?", options=blurb_options)
    else:
        quantity = 1  # Default quantity for blog posts
    
    if st.button("Generate"):
        if not topic:
            st.warning("Please insert a topic prompt.")
        else:
            cleaned_content = fetch_perplexity_results(topic, content_type, quantity)
            if cleaned_content:
                st.write(cleaned_content)
            else:
                st.write("No results found.")

if __name__ == "__main__":
    main()
