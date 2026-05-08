# Test Suite

Tests are organized by revision under `test/<revision>/<message_type>.py`.

## Test Strategy

Each message type is validated against four categories:

### 1. Valid Full Message
A fixture YAML containing a fully-populated message (all optional fields included at every nesting level) is validated and expected to produce zero errors.

### 2. Missing Required Keys
Each required field at every nesting level is removed individually. The validator must report a `MISSING_MANDATORY_KEY` error referencing the removed field.

### 3. Invalid Values
All required fields are simultaneously mutated to an incorrect type (e.g., strings where integers are expected). The validator must report an `INVALID_VALUE` error for each mutated field, identified by its full dot-notation key path.

### 4. Invalid Keys
Ten bogus keys are inserted at randomly chosen nesting levels (using a fixed seed for reproducibility). The validator must detect and report all inserted keys as `INVALID_KEY` errors.

## Running

```
uv run pytest
```

## Currently tested message type:

[x] MAP
[ ] SPAT
[ ] TIM
[ ] PSM
