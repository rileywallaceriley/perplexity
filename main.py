import streamlit as st
import requests
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def fetch_content_from_perplexity(topic, content_type, num_results):
    """
    Fetch initial content based on a given topic, content type, and number of results from Perplexity.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {st.secrets['PERPLEXITY_API_KEY']}"}
    data = {
        "model": "mistral-7b-instruct",  # Adjust based on available models
        "messages": [
            {"role": "user", "content": f"Please provide {num_results} pieces of {content_type} about '{topic}'."}
        ],
        "max_tokens": 1000,  # Adjust based on expected response length
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        responses = response.json()['choices']
        return [resp['message']['content'] for resp in responses]
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return []

def enhance_content_with_openai(content):
    """
    Enhance and reformat the content for better readability using OpenAI.
    """
    response = client.completions.create(
        model="text-davinci-003",  # Adjust based on available models
        prompt=f"Rewrite the following in a clear, engaging, and informative manner for web publication:\n\n{content}",
        temperature=0.7,
        max_tokens=1000,  # Adjust based on your needs
        top_p=1.0
    )
    return response.choices[0].text

def main():
    st.title("Enhanced Content Generator")

    topic = st.text_input("Topic Prompt:")
    content_type = st.selectbox("Content Type:", ["current news", "blog post", "research article"])
    num_results = st.number_input("Number of Results:", min_value=1, max_value=5, value=3)

    if st.button("Generate"):
        if not topic:
            st.warning("Please insert a topic prompt.")
            return
        
        raw_contents = fetch_content_from_perplexity(topic, content_type, num_results)
        if raw_contents:
            for raw_content in raw_contents:
                enhanced_content = enhance_content_with_openai(raw_content)
                st.write(enhanced_content)
        else:
            st.write("Unable to generate content.")

if __name__ == "__main__":
    main()
