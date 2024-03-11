import streamlit as st
import requests
import openai

# Initialize API clients
openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_content_from_perplexity(topic):
    """
    Fetches initial content based on a given topic from Perplexity.
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
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
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
    Uses OpenAI to enhance and reformat the content for better readability.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",  # Adjust based on available engines
        prompt=f"Rewrite the following in a more engaging, user-friendly manner:\n\n{content}",
        temperature=0.5,
        max_tokens=512,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

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
