from fastapi import FastAPI, HTTPException
import uvicorn
import json
from typing import Dict, Any

from agentt import generate_agent_audio
from analysis import transcribe_audio, analyze_conversation
from reinforcement import adapt_script
from config import INITIAL_SCRIPTS

app = FastAPI()

#database for real app eg. redis, postgreSQL
def load_current_script_state() -> Dict[str, Any]:
    """Load the current script state from file or return default."""
    try:
        with open("current_script.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "intro": INITIAL_SCRIPTS["default_intro"],
            "benefits": INITIAL_SCRIPTS["default_benefits"],
            "cta": INITIAL_SCRIPTS["default_cta"],
        }

def save_current_script_state(script_state: Dict[str, Any]) -> None:
    """Save the current script state to file."""
    try:
        with open("current_script.json", "w") as f:
            json.dump(script_state, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save script state: {str(e)}")

@app.post("/run_simulation_cycle")
def run_simulation_cycle():
    """
    Runs a single cycle:
    1. Generate Agent Audio from the current script.
    2. "Transcribe" the call (using a dummy farmer response).
    3. Analyze the transcript for insights.
    4. Adapt the script for the next call.
    """
    try:
        #load current script state
        current_script_state = load_current_script_state()
        
        #1 : voice agent simulation
        full_script_text = f"{current_script_state['intro']} {current_script_state['benefits']} {current_script_state['cta']}"
        agent_audio_path = generate_agent_audio(full_script_text)
        
        #2 : call analysis layer
        #dummy audio

        transcript = transcribe_audio(agent_audio_path, "example.mp3")
        analysis_result = analyze_conversation(transcript)
        
        #print analysis result using model_dump_json for proper JSON formatting
        print(f"\n--- Call Analysis Result ---\n{analysis_result.model_dump_json(indent=2)}")
        
        #3 : rule based reinforcement learning loop
        next_script = adapt_script(current_script_state, analysis_result)
        
        #save new script for the next run
        save_current_script_state(next_script)
        
        return {
            "message": "Simulation cycle complete.",
            "analysis": analysis_result.model_dump(),  #using model_dump() instead of dict()
            "next_script": next_script
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation cycle failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
