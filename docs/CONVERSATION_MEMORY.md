# Conversation Memory Feature

## Overview

The conversation memory system enables multi-turn context-aware conversations with the Stripe RAG agent. Users can have persistent conversations where the agent remembers previous questions and answers, enabling natural follow-up questions and clarifications.

## Architecture

### Plug-and-Play Design

The memory system follows a provider pattern, making it easy to swap implementations:

```
ConversationMemory (Abstract Base Class)
├── InMemoryConversationMemory (Fast, non-persistent)
└── SQLiteConversationMemory (Persistent, production-ready)
```

### Easy to Extend

Add new providers (Redis, PostgreSQL, MongoDB) by implementing the `ConversationMemory` interface:

```python
class ConversationMemory(ABC):
    @abstractmethod
    def create_session(self, session_id: str) -> None: ...

    @abstractmethod
    def add_messages(self, session_id: str, messages: List[BaseMessage]) -> None: ...

    @abstractmethod
    def get_messages(self, session_id: str, limit: Optional[int] = None) -> List[BaseMessage]: ...

    @abstractmethod
    def clear_session(self, session_id: str) -> None: ...

    @abstractmethod
    def session_exists(self, session_id: str) -> bool: ...

    @abstractmethod
    def get_session_metadata(self, session_id: str) -> Dict[str, Any]: ...
```

## Configuration

Edit `config.yaml`:

```yaml
services:
  memory:
    provider: "in-memory" # or "sqlite"
    sqlite_db_path: "data/conversation_memory.db" # used if provider is "sqlite"
    context_window: 5 # number of previous message pairs to include
```

### Providers

#### 1. **In-Memory** (Default)

- Fast and simple
- No persistence (data lost on restart)
- Suitable for: development, testing, single-session demos

#### 2. **SQLite**

- Persistent across restarts
- File-based database
- Suitable for: production single-server, moderate scale
- Automatic schema migration

## API Usage

### 1. Basic Query (New Session)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me how to create a customer"
  }'
```

Response:

```json
{
  "answer": "To create a customer...",
  "session_id": "abc-123-def-456"
}
```

### 2. Follow-up Query (Same Session)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What about updating it?",
    "session_id": "abc-123-def-456"
  }'
```

The agent now has context from the previous question about "creating a customer" and understands "it" refers to a customer object.

### 3. Get Session Info

```bash
curl http://localhost:8000/session/abc-123-def-456
```

Response:

```json
{
  "session_id": "abc-123-def-456",
  "created_at": "2026-02-28T10:30:00",
  "last_accessed": "2026-02-28T10:35:00",
  "message_count": 4
}
```

### 4. Clear Session

```bash
curl -X DELETE http://localhost:8000/session/abc-123-def-456
```

Response:

```json
{
  "status": "success",
  "message": "Session abc-123-def-456 cleared"
}
```

## Example Conversations

### Clarification Flow

**Turn 1:**

```
User: "Show me how to create one"
Agent: "What would you like to create? (customers, payment intents, subscriptions, etc.)"
```

**Turn 2 (with session_id):**

```
User: "A customer"
Agent: "To create a customer, use POST /v1/customers with the following parameters..."
```

The agent remembers the conversation context and understands the clarification.

### Version Comparison Follow-up

**Turn 1:**

```
User: "Compare customer creation between v1 and v2"
Agent: [Provides detailed comparison]
```

**Turn 2 (with session_id):**

```
User: "What about the differences in payment methods?"
Agent: [Knows we're still talking about customers and payment method changes between v1 and v2]
```

## Context Window

The `context_window` setting controls how many previous message pairs are included:

- `context_window: 5` → Last 10 messages (5 user + 5 assistant)
- Higher values = more context but higher token usage
- Recommended: 3-5 for most use cases

## Planner Context Awareness

The planner has been updated to use conversation history:

```python
# Before: Only looks at current query
planner(current_query)

# After: Uses conversation history for context
planner(conversation_history + current_query)
```

This enables:

- ✅ Resolving ambiguous pronouns ("it", "that", "this API")
- ✅ Understanding follow-up questions
- ✅ Remembering previous clarifications
- ✅ Maintaining conversation topic continuity

## Database Schema (SQLite)

### `sessions` table

```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    last_accessed TEXT NOT NULL
)
```

### `messages` table

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    message_data TEXT NOT NULL,  -- JSON serialized LangChain message
    timestamp TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
```

## Integration Points

### 1. API Layer (`main.py`)

- Manages session IDs
- Retrieves conversation history
- Saves new messages after each turn

### 2. Agent Layer (` agent.py`)

- Planner receives full conversation context
- Makes context-aware planning decisions

### 3. Memory Layer (`memory.py`)

- Abstract interface for storage backends
- Provider implementations (in-memory, SQLite)

## Future Extensions

### Potential Providers

1. **Redis**: Distributed caching, multi-server support
2. **PostgreSQL**: Production-grade RDBMS, advanced querying
3. **MongoDB**: Document store, flexible schema
4. **DynamoDB**: AWS serverless, global distribution
5. **Firestore**: Google Cloud, real-time sync

### Example: Adding Redis Provider

```python
class RedisConversationMemory(ConversationMemory):
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)

    def create_session(self, session_id: str) -> None:
        # Implementation using Redis hashes
        ...
```

Then update `memory.py` factory:

```python
elif provider == "redis":
    redis_url = kwargs.get("redis_url", "redis://localhost:6379")
    return RedisConversationMemory(redis_url=redis_url)
```

## Performance Considerations

### In-Memory

- **Pros**: Instant access, no I/O overhead
- **Cons**: Memory usage scales with sessions, lost on restart
- **Best for**: Development, demos, single-user scenarios

### SQLite

- **Pros**: Persistent, zero-config, file-based
- **Cons**: File locking limits concurrent writes
- **Best for**: Single-server production, moderate scale (< 1000 sessions)

### Future (Redis/PostgreSQL)

- **Pros**: Distributed, concurrent, scalable
- **Cons**: Requires infrastructure setup
- **Best for**: Multi-server, high-volume production

## Monitoring

### Logs to Watch

```
[Memory] Using in-memory conversation storage
[Memory] Created session: abc-123-def-456
[Memory] Added 2 message(s) to session abc-123-def-456
[API] Session: abc-123-def-456 | Query: What about v2?
[API] Using 4 previous messages for context
[Planner] Using conversation context (5 total messages)
```

### Key Metrics

- **session_count**: Number of active sessions
- **messages_per_session**: Average conversation depth
- **context_window_usage**: How often context is actually used
- **session_duration**: Time between first and last message

## Testing

### Test Multi-Turn Conversation

```bash
# First query
RESPONSE=$(curl -s -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I create a customer?"}')

SESSION_ID=$(echo $RESPONSE | jq -r '.session_id')

# Follow-up query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What fields are required?\", \"session_id\": \"$SESSION_ID\"}"
```

### Test Session Persistence (SQLite)

```bash
# Create session
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Test", "session_id": "test-123"}'

# Restart server
# ...

# Query same session - should have history
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What was my last question?", "session_id": "test-123"}'
```

## Migration Guide

### From Old API (No Sessions) to New API

**Before:**

```bash
curl -X POST http://localhost:8000/query \
  -d '{"query": "..."}'
```

**After (Backward Compatible):**

```bash
# Omit session_id for one-off queries (auto-generates session)
curl -X POST http://localhost:8000/query \
  -d '{"query": "..."}'

# Or include session_id for multi-turn
curl -X POST http://localhost:8000/query \
  -d '{"query": "...", "session_id": "my-session"}'
```

The API is backward compatible - existing clients work without changes!

## Troubleshooting

### Issue: Session not found

```json
{ "detail": "Session abc-123 not found" }
```

**Solution**: Session ID doesn't exist. Create new session or check ID spelling.

### Issue: SQLite database locked

```
sqlite3.OperationalError: database is locked
```

**Solution**: Multiple processes trying to write simultaneously. Use WAL mode or switch to Redis/PostgreSQL for multi-process scenarios.

### Issue: Memory usage growing

**Solution**: Implement session expiration/cleanup:

```python
# TODO: Add session TTL and cleanup job
def cleanup_old_sessions(max_age_hours: int = 24):
    # Delete sessions older than max_age_hours
    ...
```

## Summary

✅ **Plug-and-play**: Switch providers via config  
✅ **Context-aware**: Planner uses conversation history  
✅ **Extensible**: Easy to add new storage backends  
✅ **Production-ready**: SQLite for persistence  
✅ **Backward compatible**: API works with or without sessions  
✅ **Session management**: Info, clear, metadata endpoints

This feature enables natural multi-turn conversations while maintaining a clean, extensible architecture!
