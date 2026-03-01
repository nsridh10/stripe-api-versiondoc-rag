# src/memory.py
"""
Conversation memory management for multi-turn context awareness.
Provides plug-and-play backends: in-memory, SQLite, and extensible for others.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import sqlite3
from pathlib import Path
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, messages_from_dict, messages_to_dict


class ConversationMemory(ABC):
    """Abstract base class for conversation memory backends."""
    
    @abstractmethod
    def create_session(self, session_id: str) -> None:
        """Create a new conversation session."""
        pass
    
    @abstractmethod
    def add_messages(self, session_id: str, messages: List[BaseMessage]) -> None:
        """Add messages to a session's history."""
        pass
    
    @abstractmethod
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[BaseMessage]:
        """Retrieve messages from a session. Returns most recent if limit is set."""
        pass
    
    @abstractmethod
    def clear_session(self, session_id: str) -> None:
        """Clear all messages from a session."""
        pass
    
    @abstractmethod
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        pass
    
    @abstractmethod
    def get_session_metadata(self, session_id: str) -> Dict[str, Any]:
        """Get metadata about a session (created_at, message_count, etc.)."""
        pass

    @abstractmethod
    def set_context(self, session_id: str, context: List[Dict]) -> None:
        """Persist the conversation operation log for a session."""
        pass

    @abstractmethod
    def get_context(self, session_id: str) -> List[Dict]:
        """Retrieve the conversation operation log for a session."""
        pass

    @abstractmethod
    def set_scope(self, session_id: str, scope: Dict) -> None:
        """Persist the active scope (api_classes + versions) for a session."""
        pass

    @abstractmethod
    def get_scope(self, session_id: str) -> Optional[Dict]:
        """Retrieve the active scope for a session."""
        pass

    @abstractmethod
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions with metadata, ordered by last_accessed descending."""
        pass

    @abstractmethod
    def set_context_start(self, session_id: str, index: int) -> None:
        """Set the message index where the current RAG context segment begins.
        
        When a new intent is detected, this is advanced so the agent only sees
        messages from the current topic, while display endpoints return all messages.
        """
        pass

    @abstractmethod
    def get_context_start(self, session_id: str) -> int:
        """Get the message index where the current RAG context segment begins."""
        pass


# ---------------------------------------------------------------------------
# In-Memory Implementation
# ---------------------------------------------------------------------------

class InMemoryConversationMemory(ConversationMemory):
    """
    In-memory conversation storage. Fast but not persistent across restarts.
    Suitable for development and single-server deployments.
    """
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        print("[Memory] Using in-memory conversation storage")
    
    def create_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "messages": [],
                "context": [],
                "scope": None,
                "context_start": 0,
                "created_at": datetime.utcnow().isoformat(),
                "last_accessed": datetime.utcnow().isoformat()
            }
            print(f"[Memory] Created session: {session_id}")
    
    def add_messages(self, session_id: str, messages: List[BaseMessage]) -> None:
        self.create_session(session_id)  # Auto-create if doesn't exist
        self._sessions[session_id]["messages"].extend(messages)
        self._sessions[session_id]["last_accessed"] = datetime.utcnow().isoformat()
        print(f"[Memory] Added {len(messages)} message(s) to session {session_id}")
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[BaseMessage]:
        if not self.session_exists(session_id):
            return []
        
        messages = self._sessions[session_id]["messages"]
        self._sessions[session_id]["last_accessed"] = datetime.utcnow().isoformat()
        
        if limit is not None:
            return messages[-limit:]
        return messages
    
    def clear_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            self._sessions[session_id]["messages"] = []
            self._sessions[session_id]["context"] = []
            self._sessions[session_id]["scope"] = None
            self._sessions[session_id]["context_start"] = 0
            print(f"[Memory] Cleared session: {session_id}")
    
    def session_exists(self, session_id: str) -> bool:
        return session_id in self._sessions
    
    def get_session_metadata(self, session_id: str) -> Dict[str, Any]:
        if not self.session_exists(session_id):
            return {}
        
        session = self._sessions[session_id]
        return {
            "session_id": session_id,
            "created_at": session["created_at"],
            "last_accessed": session["last_accessed"],
            "message_count": len(session["messages"]),
            "context_start": session.get("context_start", 0)
        }

    def set_context(self, session_id: str, context: List[Dict]) -> None:
        self.create_session(session_id)
        self._sessions[session_id]["context"] = context
        print(f"[Memory] Saved operation log ({len(context)} turn(s)) to session {session_id}")

    def get_context(self, session_id: str) -> List[Dict]:
        if not self.session_exists(session_id):
            return []
        return self._sessions[session_id].get("context", [])

    def set_scope(self, session_id: str, scope: Dict) -> None:
        self.create_session(session_id)
        self._sessions[session_id]["scope"] = scope
        print(f"[Memory] Saved active scope to session {session_id}: {scope}")

    def get_scope(self, session_id: str) -> Optional[Dict]:
        if not self.session_exists(session_id):
            return None
        return self._sessions[session_id].get("scope")

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = []
        for sid, data in self._sessions.items():
            # Extract first user message as preview
            first_user_msg = ""
            for msg in data.get("messages", []):
                if isinstance(msg, HumanMessage):
                    first_user_msg = msg.content[:100]
                    break
            sessions.append({
                "session_id": sid,
                "created_at": data["created_at"],
                "last_accessed": data["last_accessed"],
                "message_count": len(data["messages"]),
                "preview": first_user_msg
            })
        # Sort by last_accessed descending
        sessions.sort(key=lambda x: x["last_accessed"], reverse=True)
        return sessions

    def set_context_start(self, session_id: str, index: int) -> None:
        self.create_session(session_id)
        self._sessions[session_id]["context_start"] = index
        print(f"[Memory] Context start set to {index} for session {session_id}")

    def get_context_start(self, session_id: str) -> int:
        if not self.session_exists(session_id):
            return 0
        return self._sessions[session_id].get("context_start", 0)


# ---------------------------------------------------------------------------
# SQLite Implementation
# ---------------------------------------------------------------------------

class SQLiteConversationMemory(ConversationMemory):
    """
    SQLite-based conversation storage. Persistent across restarts.
    Suitable for production single-server or small-scale deployments.
    """
    
    def __init__(self, db_path: str = "data/conversation_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        print(f"[Memory] Using SQLite conversation storage at: {self.db_path}")
    
    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message_data TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session 
                ON messages(session_id)
            """)
            # Safe migration: add context_data column if it doesn't exist yet
            try:
                conn.execute("ALTER TABLE sessions ADD COLUMN context_data TEXT DEFAULT '[]'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Safe migration: add scope_data column if it doesn't exist yet
            try:
                conn.execute("ALTER TABLE sessions ADD COLUMN scope_data TEXT DEFAULT NULL")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Safe migration: add context_start column if it doesn't exist yet
            try:
                conn.execute("ALTER TABLE sessions ADD COLUMN context_start INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass  # Column already exists
            conn.commit()
    
    def create_session(self, session_id: str) -> None:
        if not self.session_exists(session_id):
            now = datetime.utcnow().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO sessions (session_id, created_at, last_accessed) VALUES (?, ?, ?)",
                    (session_id, now, now)
                )
                conn.commit()
            print(f"[Memory] Created session: {session_id}")
    
    def add_messages(self, session_id: str, messages: List[BaseMessage]) -> None:
        self.create_session(session_id)
        now = datetime.utcnow().isoformat()
        
        # Serialize messages to JSON
        serialized_messages = []
        for msg in messages:
            msg_dict = messages_to_dict([msg])[0]
            serialized_messages.append((session_id, json.dumps(msg_dict), now))
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                "INSERT INTO messages (session_id, message_data, timestamp) VALUES (?, ?, ?)",
                serialized_messages
            )
            conn.execute(
                "UPDATE sessions SET last_accessed = ? WHERE session_id = ?",
                (now, session_id)
            )
            conn.commit()
        
        print(f"[Memory] Added {len(messages)} message(s) to session {session_id}")
    
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[BaseMessage]:
        if not self.session_exists(session_id):
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            if limit is not None:
                cursor = conn.execute(
                    """SELECT message_data FROM messages 
                       WHERE session_id = ? 
                       ORDER BY id DESC LIMIT ?""",
                    (session_id, limit)
                )
                rows = list(reversed(cursor.fetchall()))  # Reverse to chronological order
            else:
                cursor = conn.execute(
                    "SELECT message_data FROM messages WHERE session_id = ? ORDER BY id",
                    (session_id,)
                )
                rows = cursor.fetchall()
            
            # Update last accessed
            conn.execute(
                "UPDATE sessions SET last_accessed = ? WHERE session_id = ?",
                (datetime.utcnow().isoformat(), session_id)
            )
            conn.commit()
        
        # Deserialize messages
        messages = []
        for (msg_data,) in rows:
            msg_dict = json.loads(msg_data)
            messages.extend(messages_from_dict([msg_dict]))
        
        return messages
    
    def clear_session(self, session_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute(
                "UPDATE sessions SET context_start = 0, context_data = '[]', scope_data = NULL WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()
        print(f"[Memory] Cleared session: {session_id}")
    
    def session_exists(self, session_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM sessions WHERE session_id = ?", (session_id,)
            )
            return cursor.fetchone() is not None
    
    def get_session_metadata(self, session_id: str) -> Dict[str, Any]:
        if not self.session_exists(session_id):
            return {}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT created_at, last_accessed, context_start FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            
            cursor = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE session_id = ?",
                (session_id,)
            )
            message_count = cursor.fetchone()[0]
        
        return {
            "session_id": session_id,
            "created_at": row[0],
            "last_accessed": row[1],
            "message_count": message_count,
            "context_start": row[2] if row[2] is not None else 0
        }

    def set_context(self, session_id: str, context: List[Dict]) -> None:
        self.create_session(session_id)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE sessions SET context_data = ? WHERE session_id = ?",
                (json.dumps(context), session_id)
            )
            conn.commit()
        print(f"[Memory] Saved operation log ({len(context)} turn(s)) to session {session_id}")

    def get_context(self, session_id: str) -> List[Dict]:
        if not self.session_exists(session_id):
            return []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT context_data FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
        if row and row[0]:
            return json.loads(row[0])
        return []

    def set_scope(self, session_id: str, scope: Dict) -> None:
        self.create_session(session_id)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE sessions SET scope_data = ? WHERE session_id = ?",
                (json.dumps(scope) if scope else None, session_id)
            )
            conn.commit()
        print(f"[Memory] Saved active scope to session {session_id}: {scope}")

    def get_scope(self, session_id: str) -> Optional[Dict]:
        if not self.session_exists(session_id):
            return None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT scope_data FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
        if row and row[0]:
            return json.loads(row[0])
        return None

    def list_sessions(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT session_id, created_at, last_accessed FROM sessions ORDER BY last_accessed DESC"
            )
            rows = cursor.fetchall()

        sessions = []
        for sid, created_at, last_accessed in rows:
            with sqlite3.connect(self.db_path) as conn:
                count_cursor = conn.execute(
                    "SELECT COUNT(*) FROM messages WHERE session_id = ?", (sid,)
                )
                message_count = count_cursor.fetchone()[0]
                # Get first user message as preview
                preview_cursor = conn.execute(
                    "SELECT message_data FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT 5",
                    (sid,)
                )
                preview = ""
                for (msg_data,) in preview_cursor.fetchall():
                    msg_dict = json.loads(msg_data)
                    if msg_dict.get("type") == "human":
                        preview = msg_dict.get("data", {}).get("content", "")[:100]
                        break

            sessions.append({
                "session_id": sid,
                "created_at": created_at,
                "last_accessed": last_accessed,
                "message_count": message_count,
                "preview": preview
            })
        return sessions

    def set_context_start(self, session_id: str, index: int) -> None:
        self.create_session(session_id)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE sessions SET context_start = ? WHERE session_id = ?",
                (index, session_id)
            )
            conn.commit()
        print(f"[Memory] Context start set to {index} for session {session_id}")

    def get_context_start(self, session_id: str) -> int:
        if not self.session_exists(session_id):
            return 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT context_start FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
        if row and row[0] is not None:
            return row[0]
        return 0


# ---------------------------------------------------------------------------
# Factory Function
# ---------------------------------------------------------------------------

# Singleton cache for memory instances
_memory_instances: Dict[str, "ConversationMemory"] = {}

def get_conversation_memory(provider: str = "in-memory", **kwargs) -> ConversationMemory:
    """
    Factory function to get the configured conversation memory backend.
    Returns a cached singleton instance for each provider configuration.
    
    Args:
        provider: "in-memory" or "sqlite"
        **kwargs: Provider-specific arguments (e.g., db_path for SQLite)
    
    Returns:
        ConversationMemory instance (singleton per provider)
    """
    provider = provider.lower()
    
    # Create a cache key based on provider and relevant kwargs
    cache_key = provider
    if provider == "sqlite":
        cache_key = f"{provider}:{kwargs.get('db_path', 'data/conversation_memory.db')}"
    
    # Return cached instance if exists
    if cache_key in _memory_instances:
        return _memory_instances[cache_key]
    
    # Create new instance
    if provider == "in-memory":
        instance = InMemoryConversationMemory()
    
    elif provider == "sqlite":
        db_path = kwargs.get("db_path", "data/conversation_memory.db")
        instance = SQLiteConversationMemory(db_path=db_path)
    
    else:
        raise ValueError(
            f"Unsupported memory provider: {provider}. "
            f"Available: 'in-memory', 'sqlite'"
        )
    
    # Cache and return
    _memory_instances[cache_key] = instance
    return instance
