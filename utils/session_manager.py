"""
Session Manager for persisting questionnaire progress and answers.
Allows users to resume questionnaires at any time, even after closing the application.
"""
import json
import os
from datetime import datetime
from pathlib import Path


def get_session_file(client_id: str, client_name: str = None) -> str:
    """
    Get the path to the session file for a client.
    
    Args:
        client_id: Unique client identifier (e.g., "1")
        client_name: Optional client name for folder naming (e.g., "Test")
    
    Returns:
        Path to the session.json file
    """
    if client_name:
        safe_name = "_".join(client_name.split())
        folder_name = f"{client_id}_{safe_name}"
    else:
        # Fallback: create folder based on client_id only
        folder_name = f"{client_id}"
    
    client_dir = os.path.join("clients", folder_name)
    os.makedirs(client_dir, exist_ok=True)
    return os.path.join(client_dir, "session.json")


def load_session_file(session_path: str) -> dict:
    """
    Load the session data from disk.
    
    Args:
        session_path: Path to session.json file
    
    Returns:
        Dictionary with session data, or empty dict if file doesn't exist
    """
    if not os.path.exists(session_path):
        return {"sessions": {}}
    
    try:
        with open(session_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"sessions": {}}


def save_session_file(session_path: str, data: dict) -> bool:
    """
    Save session data to disk.
    
    Args:
        session_path: Path to session.json file
        data: Dictionary with session data
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(session_path), exist_ok=True)
        
        with open(session_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[ERROR] Could not save session: {e}")
        return False


def save_session(client_id: str, client_name: str, phase_name: str, 
                 question_index: int, answers: dict, total_questions: int) -> bool:
    """
    Save the current session state for a client and phase.
    Call this after the user answers each question or navigates away.
    
    Args:
        client_id: Client ID (e.g., "1")
        client_name: Client name (e.g., "Test")
        phase_name: Phase identifier (e.g., "phase1.1", "phase2.0")
        question_index: Current question index or progress
        answers: Dictionary of answers (e.g., {1: "5", 2: "3", ...})
        total_questions: Total number of questions in this phase
    
    Returns:
        True if successful, False otherwise
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    # Ensure sessions dict exists
    if "sessions" not in data:
        data["sessions"] = {}
    
    # Update or create session for this phase
    data["sessions"][phase_name] = {
        "status": "in_progress",
        "last_question_index": question_index,
        "total_questions": total_questions,
        "answers": answers,
        "timestamp": datetime.now().isoformat()
    }
    
    return save_session_file(session_path, data)


def load_session(client_id: str, client_name: str, phase_name: str) -> dict | None:
    """
    Load a saved session for a specific phase.
    
    Args:
        client_id: Client ID
        client_name: Client name
        phase_name: Phase identifier
    
    Returns:
        Session dict with 'answers', 'question_index', etc., or None if not found
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    if phase_name in data.get("sessions", {}):
        return data["sessions"][phase_name]
    return None


def has_incomplete_session(client_id: str, client_name: str, phase_name: str = None) -> bool:
    """
    Check if there's an incomplete (in-progress) session for a client.
    
    Args:
        client_id: Client ID
        client_name: Client name
        phase_name: Optional phase to check. If None, checks all phases.
    
    Returns:
        True if incomplete session exists, False otherwise
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    sessions = data.get("sessions", {})
    
    if phase_name:
        # Check specific phase
        return (phase_name in sessions and 
                sessions[phase_name].get("status") == "in_progress")
    else:
        # Check if any phase has in_progress status
        return any(s.get("status") == "in_progress" for s in sessions.values())


def get_incomplete_phases(client_id: str, client_name: str) -> list[str]:
    """
    Get list of phases with incomplete sessions.
    
    Args:
        client_id: Client ID
        client_name: Client name
    
    Returns:
        List of phase names with in_progress status
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    sessions = data.get("sessions", {})
    return [phase for phase, session in sessions.items() 
            if session.get("status") == "in_progress"]


def mark_session_complete(client_id: str, client_name: str, phase_name: str) -> bool:
    """
    Mark a session as completed.
    
    Args:
        client_id: Client ID
        client_name: Client name
        phase_name: Phase identifier
    
    Returns:
        True if successful, False otherwise
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    if phase_name in data.get("sessions", {}):
        data["sessions"][phase_name]["status"] = "completed"
        data["sessions"][phase_name]["completed_timestamp"] = datetime.now().isoformat()
        return save_session_file(session_path, data)
    
    return False


def clear_session(client_id: str, client_name: str, phase_name: str) -> bool:
    """
    Clear the session data for a specific phase.
    
    Args:
        client_id: Client ID
        client_name: Client name
        phase_name: Phase identifier
    
    Returns:
        True if successful, False otherwise
    """
    session_path = get_session_file(client_id, client_name)
    data = load_session_file(session_path)
    
    if phase_name in data.get("sessions", {}):
        del data["sessions"][phase_name]
        return save_session_file(session_path, data)
    
    return False


def clear_all_sessions(client_id: str, client_name: str) -> bool:
    """
    Clear all session data for a client.
    
    Args:
        client_id: Client ID
        client_name: Client name
    
    Returns:
        True if successful, False otherwise
    """
    session_path = get_session_file(client_id, client_name)
    return save_session_file(session_path, {"sessions": {}})
