import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from typing import Optional
import logging

#logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def generate_agent_audio(script_text: str, output_path: str = "audio/agent_output.mp3") -> str:
    """
    Generates audio from text using ElevenLabs API.
    
    Args:
        script_text: The text to convert to speech
        output_path: Path where the audio file will be saved
        
    Returns:
        str: Path to the generated audio file
        
    Raises:
        ValueError: If API key is not found or script_text is empty
        Exception: If audio generation fails
    """
    #validate inputs
    if not script_text or not script_text.strip():
        raise ValueError("Script text cannot be empty")
    
    api_key = os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY not found in environment variables")
    
    #create output directory if it doesnt exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        #initialize 11labs client
        client = ElevenLabs(api_key=api_key)
        
        #audio model
        audio = client.generate(
            text=script_text,
            voice="21m00Tcm4TlvDq8ikWAM", 
            model="eleven_multilingual_v2"
        )
        
        #handle the audio response properly
        if hasattr(audio, '__iter__') and not isinstance(audio, (str, bytes)):
            #if its a generator, collect all chunks
            audio_data = b''.join(audio)
        else:
            #if its already bytes
            audio_data = audio
        
        #write audio to file
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        logger.info(f"Agent audio saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Failed to generate audio: {str(e)}")
        raise Exception(f"Audio generation failed: {str(e)}")
