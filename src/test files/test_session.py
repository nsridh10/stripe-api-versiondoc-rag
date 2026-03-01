"""
End-to-end test: session continuity + context_start tracking.

This script tests the multi-turn conversation flow, verifying that:
1. Sessions are maintained across follow-up queries
2. Context boundaries (context_start) are properly advanced on new intents
3. The frontend would still see all messages while the agent only reads relevant context

Usage:
    cd /Users/navein/stripe-rag-agent
    source venv/bin/activate
    # Start server first: uvicorn src.main:app --reload
    python -m "src.test files.test_session"
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import requests
import json
import time

BASE = "http://localhost:8000"


def query(text, session_id=None):
    """Send a query to the agent."""
    payload = {"query": text}
    if session_id:
        payload["session_id"] = session_id
    r = requests.post(f"{BASE}/query", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()


def session_info(sid):
    """Get session metadata."""
    r = requests.get(f"{BASE}/session/{sid}", timeout=10)
    r.raise_for_status()
    return r.json()


def session_messages(sid):
    """Get all messages in a session."""
    r = requests.get(f"{BASE}/session/{sid}/messages", timeout=10)
    r.raise_for_status()
    return r.json()


def sessions_list():
    """List all sessions."""
    r = requests.get(f"{BASE}/sessions", timeout=10)
    r.raise_for_status()
    return r.json()


def run_session_test():
    """Run the full session continuity test."""
    print("=" * 60)
    print("STEP 1: New intent — 'How do I create a customer?'")
    print("=" * 60)
    r1 = query("How do I create a customer in Stripe?")
    sid = r1["session_id"]
    print(f"  Session ID : {sid}")
    print(f"  Type       : {r1['message_type']}")
    print(f"  Sources    : {len(r1['sources'])}")
    for s in r1["sources"]:
        print(f"    {s['api_class']} {s['version']} -> {s['source_file']}")
    info1 = session_info(sid)
    print(f"  Messages   : {info1['message_count']}")
    print(f"  ctx_start  : {info1['context_start']}")
    print()

    print("=" * 60)
    print("STEP 2: Follow-up — 'How to update them?'")
    print("=" * 60)
    r2 = query("How to update them?", session_id=sid)
    print(f"  Session ID : {r2['session_id']}  (same={r2['session_id']==sid})")
    print(f"  Type       : {r2['message_type']}")
    for s in r2["sources"]:
        print(f"    {s['api_class']} {s['version']} -> {s['source_file']}")
    info2 = session_info(sid)
    print(f"  Messages   : {info2['message_count']}")
    print(f"  ctx_start  : {info2['context_start']}  (should still be 0)")
    print()

    print("=" * 60)
    print("STEP 3: New intent — 'How do refunds work?'")
    print("=" * 60)
    r3 = query("How do refunds work?", session_id=sid)
    print(f"  Session ID : {r3['session_id']}  (same={r3['session_id']==sid})")
    print(f"  Type       : {r3['message_type']}")
    for s in r3["sources"]:
        print(f"    {s['api_class']} {s['version']} -> {s['source_file']}")
    info3 = session_info(sid)
    print(f"  Messages   : {info3['message_count']}")
    print(f"  ctx_start  : {info3['context_start']}  (should be 4 — past the first 2 Q/A pairs)")
    print()

    print("=" * 60)
    print("STEP 4: Follow-up on refunds — 'What about partial refunds?'")
    print("=" * 60)
    r4 = query("What about partial refunds?", session_id=sid)
    print(f"  Session ID : {r4['session_id']}  (same={r4['session_id']==sid})")
    print(f"  Type       : {r4['message_type']}")
    for s in r4["sources"]:
        print(f"    {s['api_class']} {s['version']} -> {s['source_file']}")
    info4 = session_info(sid)
    print(f"  Messages   : {info4['message_count']}")
    print(f"  ctx_start  : {info4['context_start']}  (should still be 4)")
    print()

    print("=" * 60)
    print("ALL MESSAGES IN SESSION (frontend would show all of these)")
    print("=" * 60)
    msgs = session_messages(sid)
    print(f"  Total: {len(msgs)} messages")
    for i, m in enumerate(msgs):
        marker = " <-- ctx_start" if i == info4["context_start"] else ""
        preview = m["content"][:70].replace("\n", " ")
        print(f"  [{i}] {m['role']:9s}: {preview}...{marker}")
    print()

    print("=" * 60)
    print("SESSIONS LIST")
    print("=" * 60)
    for s in sessions_list():
        print(f"  {s['session_id'][:16]}... msgs={s['message_count']}")

    print()
    print("✅ Session continuity test complete!")


if __name__ == "__main__":
    try:
        # Check if server is running
        requests.get(f"{BASE}/", timeout=5)
        run_session_test()
    except requests.exceptions.ConnectionError:
        print("ERROR: Server is not running!")
        print("Start the server with: uvicorn src.main:app --reload")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
