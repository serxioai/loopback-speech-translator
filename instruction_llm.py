# InstructionLLM

# sourpip install azure-ai-textanalytics

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class InstructionLLM:
    def __init__(self, model="gpt2distilbert", api_key=api_key):
        self.api_key = api_key
        self.model = model
        self.client = TextAnalyticsClient(endpoint=endpoint, credentials=api_ke)

