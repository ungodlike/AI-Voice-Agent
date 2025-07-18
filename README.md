
# AI Voice Agent

An AI voice agent that can call users and reinforce the call script based on analyzing the end users response.


## Features


1. The simulation cycle runs a general audio script. Create a dummy user response file, named "example.mp3".

2. The user output is converted to text using whisper stt and analyzed based on pre-given sentiments (found in analysis.py) and a new audio script is generated comparing the sentiments to the initial script (config.py). 

3. Final output has a the users response and the new script along with the sentiment analysis results. The new script is stored in current_script.json and is called the next time. 

I used a rule based reinforcement loop instead of LLM generated responses for cost efficiency. LLMs can and should be used in conjunction with this for fine tuning new scripts.

## Installation

First install the requirements

```bash
pip install -r requirements.txt
```
Then run the fastapi backend using
```bash
uvicorn main:app --reload 
```

## FastAPI Backend

The FastAPI backend runs a simulated cycle and outputs a new script as well as the sentiment of the user in a json format. The new script is saved as a current_script.json 

-------------------------------------------------------------
Example Output 

```bash
--- Generated Transcript ---
Agent: [Agent's opening words]
Farmer:  I don't know, it sounds a bit confusing. Maybe get back to me a week later?
INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"

--- Call Analysis Result ---
{
  "farmer_sentiment": "negative",
  "interest_level": "confusion",
  "intro_clarity": "confused",
  "objections": [
    "price",
    "eligibility"
  ],
  "call_outcome": "follow_up"
}

--- Adapting Script based on Analysis ---
Action: Intro was confusing. Switching to simpler opening.
Action: Negative sentiment detected. Next call should use a softer tone.
Action: Farmer requested a follow-up. Added to callback list.
```

