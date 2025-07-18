import os
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from typing import List

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