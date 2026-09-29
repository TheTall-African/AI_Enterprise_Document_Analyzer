import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def create_embedding(text):
    """ This is the function that converts text into numerical
    embedding vector that the computer can now read and process
    in machine language through synonyms between the words."""

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = text
    )

    embedding = response.data[0].embedding

    return embedding

'''TEST RUN OF EMBEDDINGS FUNCTION
if __name__ == "__main__":

    text = (
        "Transactions above $100,000 "
        "require CFO approval."
    )

    embedding = create_embedding(text)

    print(
        "Embedding length:",
        len(embedding)
    )

    print(
        "First 10 values:",
        embedding[:10]
    )
    '''