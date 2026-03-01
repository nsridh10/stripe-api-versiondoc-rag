#!/usr/bin/env python3
"""
Demo script for conversation memory feature.
Run this after starting the server to see multi-turn conversation in action.
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_conversation_memory():
    """Demonstrates multi-turn conversation with context."""
    
    print("=" * 70)
    print("CONVERSATION MEMORY DEMO - AUTO SESSION MANAGEMENT")
    print("=" * 70)
    
    # Turn 1: Initial query
    print("\n[Turn 1] User: Show me how to create a customer")
    response1 = requests.post(
        f"{API_URL}/query",
        json={"query": "Show me how to create a customer"}
    )
    result1 = response1.json()
    session_id = result1["session_id"]
    
    print(f"\n[Session ID]: {session_id}")
    print(f"[Agent]: {result1['answer'][:200]}...")
    
    time.sleep(1)
    
    # Turn 2: Follow-up with pronoun reference (should keep same session)
    print("\n" + "=" * 70)
    print("\n[Turn 2] User: What about updating it?")
    print("[Expected]: Intent=follow_up, Session should remain the same")
    response2 = requests.post(
        f"{API_URL}/query",
        json={
            "query": "What about updating it?",
            "session_id": session_id
        }
    )
    result2 = response2.json()
    session_id_2 = result2["session_id"]
    
    print(f"[Session ID]: {session_id_2}")
    if session_id_2 == session_id:
        print("✓ Session maintained (follow-up detected)")
    else:
        print("✗ Session changed (unexpected for follow-up)")
    print(f"[Agent]: {result2['answer'][:200]}...")
    
    time.sleep(1)
    
    # Turn 3: Completely new topic (should create new session automatically)
    print("\n" + "=" * 70)
    print("\n[Turn 3] User: How do I create a payment intent?")
    print("[Expected]: Intent=new_intent, Session should auto-reset")
    response3 = requests.post(
        f"{API_URL}/query",
        json={
            "query": "How do I create a payment intent?",
            "session_id": session_id_2
        }
    )
    result3 = response3.json()
    session_id_3 = result3["session_id"]
    
    print(f"[Session ID]: {session_id_3}")
    if session_id_3 != session_id_2:
        print("✓ Session auto-reset (new intent detected)")
    else:
        print("✗ Session unchanged (new intent not detected)")
    print(f"[Agent]: {result3['answer'][:200]}...")
    
    # Turn 4: Follow-up on the new topic (should keep new session)
    time.sleep(1)
    print("\n" + "=" * 70)
    print("\n[Turn 4] User: What parameters does it need?")
    print("[Expected]: Intent=follow_up for payment intent, Session maintained")
    response4 = requests.post(
        f"{API_URL}/query",
        json={
            "query": "What parameters does it need?",
            "session_id": session_id_3
        }
    )
    result4 = response4.json()
    session_id_4 = result4["session_id"]
    
    print(f"[Session ID]: {session_id_4}")
    if session_id_4 == session_id_3:
        print("✓ Session maintained (follow-up on payment intent)")
    else:
        print("✗ Session changed (unexpected)")
    print(f"[Agent]: {result4['answer'][:200]}...")
    
    # Clean up sessions
    for sid in [session_id, session_id_2, session_id_3, session_id_4]:
        try:
            requests.delete(f"{API_URL}/session/{sid}")
        except:
            pass
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


def test_clarification_flow():
    """Demonstrates clarification with context."""
    
    print("\n\n" + "=" * 70)
    print("CLARIFICATION FLOW DEMO")
    print("=" * 70)
    
    # Turn 1: Ambiguous query
    print("\n[Turn 1] User: Show me how to create one")
    response1 = requests.post(
        f"{API_URL}/query",
        json={"query": "Show me how to create one"}
    )
    result1 = response1.json()
    session_id = result1["session_id"]
    
    print(f"\n[Session ID]: {session_id}")
    print(f"[Agent]: {result1['answer']}")
    
    time.sleep(1)
    
    # Turn 2: Clarification
    print("\n" + "=" * 70)
    print("\n[Turn 2] User: A customer")
    response2 = requests.post(
        f"{API_URL}/query",
        json={
            "query": "A customer",
            "session_id": session_id
        }
    )
    result2 = response2.json()
    print(f"[Agent]: {result2['answer'][:200]}...")
    
    # Clear session
    requests.delete(f"{API_URL}/session/{session_id}")
    
    print("\n" + "=" * 70)
    print("CLARIFICATION DEMO COMPLETE")
    print("=" * 70)


def test_version_comparison_followup():
    """Demonstrates version comparison with follow-up."""
    
    print("\n\n" + "=" * 70)
    print("VERSION COMPARISON FOLLOW-UP DEMO")
    print("=" * 70)
    
    # Turn 1: Version comparison
    print("\n[Turn 1] User: Compare customer creation between v1 and v2")
    response1 = requests.post(
        f"{API_URL}/query",
        json={"query": "Compare customer creation between v1 and v2"}
    )
    result1 = response1.json()
    session_id = result1["session_id"]
    
    print(f"\n[Session ID]: {session_id}")
    print(f"[Agent]: {result1['answer'][:300]}...")
    
    time.sleep(1)
    
    # Turn 2: Follow-up about specific difference
    print("\n" + "=" * 70)
    print("\n[Turn 2] User: What are the main differences?")
    response2 = requests.post(
        f"{API_URL}/query",
        json={
            "query": "What are the main differences?",
            "session_id": session_id
        }
    )
    result2 = response2.json()
    print(f"[Agent]: {result2['answer'][:300]}...")
    
    # Clear session
    requests.delete(f"{API_URL}/session/{session_id}")
    
    print("\n" + "=" * 70)
    print("VERSION COMPARISON DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    try:
        # Check if server is running
        requests.get(f"{API_URL}/")
        
        # Run demos
        test_conversation_memory()
        test_clarification_flow()
        test_version_comparison_followup()
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Server is not running!")
        print("Start the server with: uvicorn src.main:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")
