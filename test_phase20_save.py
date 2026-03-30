#!/usr/bin/env python
import sys
import traceback

try:
    print("Testing session save with phase2.0 data...")
    from utils.session_manager import save_session, load_session
    
    # Simulate saving phase 2.0 answers
    client_id = "1"
    client_name = "Test"
    phase_name = "phase2.0"
    
    answers = {str(k): "V" for k in range(1, 31)}  # 30 questions
    print(f"Answers to save: {answers}")
    
    success = save_session(client_id, client_name, phase_name, 0, answers, 30)
    print(f"Save successful: {success}")
    
    # Try to load it back
    loaded = load_session(client_id, client_name, phase_name)
    print(f"Loaded data: {loaded}")
    
    if loaded:
        print(f"Loaded answers: {loaded.get('answers', {})}")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
