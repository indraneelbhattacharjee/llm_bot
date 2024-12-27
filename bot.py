import os
import pickle
import datetime
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request  # Import the Request class
from dotenv import load_dotenv  # Import dotenv to load environment variables

from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.tools import Tool

from utils import extract_information
from templates import template_1

# Load environment variables from .env file
load_dotenv()

# Google API Setups
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_google():
    """Authenticate the user and return the Google Calendar API service"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the token if expired
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        logger.error(f'An error occurred: {error}')
        return None

def create_event(service, summary, location, start_datetime, end_datetime, email):
    """Create a Google Calendar event"""
    event = {
        'summary': summary,
        'location': location,
        'description': 'A meeting scheduled by the assistant.',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email}],
        'reminders': {'useDefault': True},
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f'Event created: {event.get("htmlLink")}')
        return event
    except HttpError as error:
        logger.error(f'An error occurred while creating the event: {error}')
        return None

# Define the system message for the chatbot
system_message_prompt = SystemMessagePromptTemplate.from_template(template_1)
human_template = "{query}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# Initialize the GPT-4 model with memory
openai_api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from environment variable
chat = ChatOpenAI(model="gpt-4", temperature=0.6, openai_api_key=openai_api_key)
memory = ConversationBufferMemory(memory_key="chat_history")

# Create a dummy tool (a placeholder tool to avoid the error)
tools = [
    Tool(
        name="dummy_tool",
        func=lambda query: "This is a dummy response.",
        description="A dummy tool to bypass ZeroShotAgent's tool requirement."
    )
]

# Initialize agent chain with the dummy tool
agent_chain = initialize_agent(tools, llm=chat, agent="zero-shot-react-description", verbose=True)

def bot_response(query):
    """
    Function to handle the conversation flow with the chatbot.
    
    Args:
    - query (str): The user input/query
    
    Returns:
    - response (str): The bot response
    """
    conversation = []
    conversation.append('User: ' + query)

    output = gpt_response(query)
    conversation.append('Bot: ' + output)

    print(conversation)

    # Extract relevant information from the conversation
    pattern_name = r'\bFull Name:\s*(.*)'
    pattern_service = r'\bService Type:\s*(.*)'
    pattern_location = r'\bLocation:\s*(.*)'
    pattern_time = r'\bdatetime:\s*(.*)'
    pattern_email = r'\bEmail Address:\s*(.*)'

    name = extract_information(conversation, pattern_name)
    service = extract_information(conversation, pattern_service)
    location = extract_information(conversation, pattern_location)
    datetime = extract_information(conversation, pattern_time)
    email = extract_information(conversation, pattern_email)

    # If all information is collected, schedule event
    if name and service and location and datetime and email:
        service = authenticate_google()
        if service:
            start_datetime = datetime.datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S')
            end_datetime = start_datetime + datetime.timedelta(hours=1)  # Set meeting duration

            # Create the Google Calendar event
            create_event(service, f"Quick Call with {name}", location, start_datetime, end_datetime, email)
        return "The meeting has been scheduled successfully."

    return output

# Chat Chain (GPT response)
def gpt_response(query):
    chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)
    response = chain.run(query)
    return response
