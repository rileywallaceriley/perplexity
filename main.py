import streamlit as st
import requests
import openai

# Setup OpenAI client with API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_content_from_perplexity(topic):
    """
    Fetch initial content based on a given topic from Perplexity.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {st.secrets['PERPLEXITY_API_KEY']}"}
    data = {
        "model": "mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": topic}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1.0
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content
    else:
        st.error("Failed to fetch data from Perplexity API.")
        return ""

def enhance_content_with_openai(content):
    """
    Enhance and reformat the content for better readability using OpenAI.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "The following is a piece of content that needs to be rewritten in a more engaging, user-friendly manner."},
                {"role": "user", "content": content}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Failed to process content with OpenAI: {str(e)}")
        return ""

def main():
    st.title("Enhanced Content Generator")

    topic = st.text_input("Topic Prompt:", "")

    if st.button("Generate"):
        if not topic:
            st.warning("Please insert a topic prompt.")
            return
        
        raw_content = fetch_content_from_perplexity(topic)
        if raw_content:
            enhanced_content = enhance_content_with_openai(raw_content)
            st.write(enhanced_content)
        else:
            st.write("Unable to generate content.")

if __name__ == "__main__":
    main()
