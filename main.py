import streamlit as st
import requests
import openai
import os

# Initialize OpenAI client with the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_content_from_perplexity(topic, content_type, num_results):
    """
    Fetch content from Perplexity based on the topic and content type.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {st.secrets['PERPLEXITY_API_KEY']}"}
    data = {
        "model": "gpt-3.5-turbo",  # Adjust based on available models and requirements
        "messages": [{"role": "user", "content": topic}],
        "max_tokens": 1000,  # Adjust as necessary
        "n": num_results,  # Number of completions to generate
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices']
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return []

def enhance_content_with_openai(raw_texts, content_type, desired_length):
    """
    Use OpenAI to enhance and format the raw texts for readability and content type.
    """
    enhanced_texts = []
    for text in raw_texts:
        response = openai.Completion.create(
            model="text-davinci-003",  # Consider using the latest and most capable model
            prompt=f"Summarize the following {content_type} into a {desired_length}-word, user-friendly format:\n\n{text}",
            temperature=0.7,
            max_tokens=desired_length * 5,  # Estimate max tokens based on desired word count
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        enhanced_texts.append(response.choices[0].text.strip())
    return enhanced_texts

def main():
    st.title("Content Generator with OpenAI and Perplexity")

    topic = st.text_input("Enter Topic:", "")
    content_type = st.selectbox("Content Type:", ["current news", "blog post", "research article"])
    num_results = st.number_input("Number of Results:", min_value=1, max_value=3, value=1)
    desired_length = st.number_input("Desired Length (in words):", min_value=100, max_value=500, value=200)
    
    if st.button("Generate Content"):
        if not topic:
            st.warning("Please enter a topic.")
            return
        
        raw_texts = fetch_content_from_perplexity(topic, content_type, num_results)
        if raw_texts:
            enhanced_texts = enhance_content_with_openai([text['content'] for text in raw_texts], content_type, desired_length)
            for enhanced_text in enhanced_texts:
                st.markdown(enhanced_text)
        else:
            st.write("No results found.")

if __name__ == "__main__":
    main()
