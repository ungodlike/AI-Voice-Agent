import os
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from typing import List

from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

class CallAnalysis(BaseModel):
    farmer_sentiment: str = Field(description="Emotion in farmer's tone - positive, neutral, or negative.")
    interest_level: str = Field(description="Signs of curiosity, confusion, or disinterest.")
    intro_clarity: str = Field(description="Did the farmer seem to understand the opening? 'understood' or 'confused'.")
    objections: List[str] = Field(description="List of farmer's concerns, e.g., 'price', 'eligibility'.")
    call_outcome: str = Field(description="Outcome of the call: 'success', 'rejection', or 'follow_up'.")

def analyze_conversation(transcript: str) -> CallAnalysis:
    """Analyzes transcript to extract insights using LangChain and an LLM."""
    parser = PydanticOutputParser(pydantic_object=CallAnalysis)
    
    prompt = PromptTemplate(
        template="Analyze the following call transcript between an Agent and a Farmer.\n{format_instructions}\nTranscript:\n{transcript}\n",
        input_variables=["transcript"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=api_key)
    chain = prompt | model | parser
    
    response = chain.invoke({"transcript": transcript})
    return response

'''
def transcribe_audio(agent_audio: str, farmer_audio: str) -> str:
    """Mocks transcription of a two-way conversation."""
    #client = OpenAI()
    #audio_file = open(farmer_audio, "rb")
    #farmer_text = client.audio.transcriptions.create(model="whisper-1", file=audio_file).text
    #mock usage:
    farmer_text = "Okay sounds good, could you tell me what exactly it is about?"
    
    transcript = f"Agent: [Agent's opening words]\nFarmer: {farmer_text}"
    print(f"\n--- Generated Transcript ---\n{transcript}")
    return transcript
'''

def transcribe_audio(agent_audio: str, farmer_audio: str = "example.mp3") -> str:
    """
    Transcribes the farmer's audio response using Groq's Whisper API and formats it as a conversation transcript.
    
    Args:
        agent_audio (str): Path to the agent's audio file (used to maintain transcript format).
        farmer_audio (str): Path to the farmer's audio file (default: 'example.mp3').
    
    Returns:
        str: Formatted transcript with agent placeholder and farmer's transcribed response.
    
    Raises:
        FileNotFoundError: If the farmer's audio file is not found.
        Exception: For other errors during transcription (e.g., API issues).
    """
    try:
        #groq init 
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        if not os.path.exists(farmer_audio):
            raise FileNotFoundError(f"Audio file not found: {farmer_audio}")
        
        #transcribe audio
        with open(farmer_audio, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(farmer_audio, file.read()),
                model="whisper-large-v3",
                response_format="text",
                language="en", #can adjust for hindi etc if required
                temperature=0.0
            )
        
        #transcript structure
        transcript = f"Agent: [Agent's opening words]\nFarmer: {transcription}"
        print(f"\n--- Generated Transcript ---\n{transcript}")
        return transcript
    
    except FileNotFoundError as e:
        raise Exception(f"Transcription failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Transcription failed due to API error: {str(e)}")