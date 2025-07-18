from analysis import CallAnalysis
from config import INITIAL_SCRIPTS

#rule based reinforcement loop saves money instead of using llms, llms
#can still be used for some fine tune responses in conjunction with this

def adapt_script(current_script: dict, analysis: CallAnalysis) -> dict:
    """Adapts the script based on call analysis."""
    new_script = current_script.copy()
    print("\n--- Adapting Script based on Analysis ---")

    #1 : confusion in intro
    if analysis.intro_clarity == 'confused':
        new_script['intro'] = INITIAL_SCRIPTS['simple_intro']
        print("Action: Intro was confusing. Switching to simpler opening.")

    #2 : negative sentiment (finer 11labs management for this)
    if analysis.farmer_sentiment == 'negative':
        # logging for now
        print("Action: Negative sentiment detected. Next call should use a softer tone.")

    #3 : ignored CTA
    if 'success' not in analysis.call_outcome and 'follow_up' not in analysis.call_outcome:
        new_script['cta'] = INITIAL_SCRIPTS['yes_no_cta']
        print("Action: CTA was ignored. Switching to a direct yes/no question.")

    #4 : call me later response
    if analysis.call_outcome == 'follow_up':
        #ideally, this would add the contact to a CRM with a callback tag.
        print("Action: Farmer requested a follow-up. Added to callback list.")

    return new_script