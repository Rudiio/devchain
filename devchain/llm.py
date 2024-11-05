import os

from dotenv import find_dotenv, load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_community.llms.ollama import Ollama
from langchain_openai import AzureChatOpenAI, ChatOpenAI


def load_llm(kind: str, model: str, temperature: float = 0.0):
    """Load an llm"""

    if kind == "Azure_openai":
        return load_Azure_OpenAI(model=model, temperature=temperature)

    elif kind == "Huggingface":
        return load_Hugging_face(repo_id=model, temperature=temperature)

    elif kind == "Ollama":
        return Ollama2(model=model)

    elif kind == "openai":
        return load_OpenAI(model=model, temperature=temperature)

    else:
        print("Error : Model not supported, loading gpt-35-turbo.")
        return load_Azure_OpenAI(model="gpt-35-turbo")


def load_Azure_OpenAI(
    model: str = "gpt-35-turbo", temperature: float = 0.0
) -> AzureChatOpenAI:
    """Load a AzureChatOpenAI model from Langchain
    The key are passed by reading the environnmnent variables in the .env file"""

    load_dotenv(find_dotenv())

    if model == "gpt-4":
        endpoint = os.environ["AZURE_OPENAI_ENDPOINT_4"]
        return AzureChatOpenAI(
            azure_endpoint=endpoint,
            azure_deployment="gpt-4",
            model="gpt-4",
            temperature=temperature,
        )

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT_35"]
    llm = AzureChatOpenAI(
        azure_endpoint=endpoint,
        azure_deployment="gpt-35-turbo",
        model="gpt-35-turbo",
        temperature=temperature,
    )
    return llm


def load_OpenAI(
    model: str = "gpt-4o-mini", temperature: float = 0.0
) -> AzureChatOpenAI:
    """Load a AzureChatOpenAI model from Langchain
    The key are passed by reading the environnmnent variables in the .env file"""

    load_dotenv(find_dotenv())

    llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model=model,temperature=temperature)
    return llm


def load_Hugging_face(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2", temperature: float = 0.0
) -> HuggingFaceHub:
    """Load a model from Huggingface Hub"""

    load_dotenv(find_dotenv())
    llm = HuggingFaceEndpoint2(
        repo_id=repo_id, temperature=temperature, max_new_tokens=2000
    )
    return llm


def load_Hugging_face_embeddings(model: str = "sentence-transformers/all-MiniLM-l6-v2"):
    """Load a Hugging face embeddings model"""
    # Define the path to the pre-trained model you want to use
    # Need the library sentence_transformers
    modelPath = model

    # Create a dictionary with model configuration options, specifying to use the CPU for computations
    model_kwargs = {"device": "cpu"}

    # Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
    encode_kwargs = {"normalize_embeddings": False}

    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,  # Provide the pre-trained model's path
        model_kwargs=model_kwargs,  # Pass the model configuration options
        encode_kwargs=encode_kwargs,  # Pass the encoding options
    )

    return embeddings


class HuggingFaceEndpoint2(HuggingFaceEndpoint):
    model_name: str = "Huggingface"

    def __init__(self, *args, **kwargs):
        super(HuggingFaceEndpoint2, self).__init__(*args, **kwargs)
        self.model_name = kwargs["repo_id"].split(sep="/")[1]


class Ollama2(Ollama):
    model_name: str = "Ollama"

    def __init__(self, *args, **kwargs):
        super(Ollama2, self).__init__(*args, **kwargs)
        self.model_name = "Ollama/" + kwargs["model"]
