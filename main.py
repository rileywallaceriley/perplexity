import streamlit as st
import requests
import json

# Assuming your Perplexity API key is stored in Streamlit's Secrets or environment variables
PERPLEXITY_API_KEY = st.secrets["PERPLEXITY_API_KEY"]

def fetch_perplexity_results(topic, content_type, quantity):
    """
    Fetch results from the Perplexity AI based on the topic, content type, and quantity.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    messages = [
        {"role": "system", "content": f"Generate {quantity} {content_type.lower()} about {topic}."},
        {"role": "user", "content": topic}
    ]
    
    data = {
        "model": "mistral-7b-instruct",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.0
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return None

def main():
    st.title("Content Generator")

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
            results = fetch_perplexity_results(topic, content_type, quantity)
            if results and 'choices' in results and results['choices']:
                for choice in results['choices']:
                    content = choice.get('message', {}).get('content', '')
                    if content:
                        st.write(content)
                    else:
                        st.write("No content generated.")
            else:
                st.write("No results found.")

if __name__ == "__main__":
    main()
