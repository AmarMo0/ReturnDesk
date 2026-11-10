from functools import cache

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

MODEL_NAME = "gpt-4o-mini"
ROUTER_TEMPERATURE = 0.0
WRITER_TEMPERATURE = 0.3

REQUEST_TYPES = ("standard_return", "damaged_replacement")


@cache
def get_router_llm():
    return init_chat_model(MODEL_NAME, model_provider="openai", temperature=ROUTER_TEMPERATURE)


@cache
def get_writer_llm():
    return init_chat_model(MODEL_NAME, model_provider="openai", temperature=WRITER_TEMPERATURE)
