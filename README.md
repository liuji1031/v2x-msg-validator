# v2x-msg-validator

Validates V2X messages against the J2735 ASN.1 standard using a custom [pycrate](https://github.com/liuji1031/pycrate/tree/validation) fork with validation support.

## How It Works

1. ASN.1 definition files are compiled into a Python codec module using `v2x-compile`, a command line tool shipped with this package.
2. At runtime, the validator loads the compiled codec and builds a lookup from `messageId` to the corresponding ASN.1 type.
3. Given a message (as a Python dict or YAML), the validator calls the type's `set_val()` method which recursively checks structure, types, constraints, and required fields.
4. All validation errors are collected (not fail-fast) and returned with a dot-notation key path, error code, and the offending value.

See the [demo notebook](notebooks/demo.ipynb) for example usage of the validator.

## Installation

To install from GitHub source:

```bash
uv add v2x-msg-validator --git https://github.com/liuji1031/v2x-msg-validator.git --branch main
```

Or pin to a specific tag:

```bash
uv add v2x-msg-validator --git https://github.com/liuji1031/v2x-msg-validator.git --tag v0.1.0
```

After installing, you must compile the ASN.1 definitions before the validator can be used (the compiled codec is not included in the repo):

```bash
uv run v2x-compile -i <path-to-J2735ASN_202409> -n j2735_202409
```

## Setup (Development)

```bash
uv sync
```

## Compiling ASN.1 Definitions

Before validating messages, compile the ASN.1 source files into a codec module:

```bash
uv run v2x-compile -i <path-to-asn-folder> -n <module-name>
```

For example, to compile the J2735 2024-09 definitions:

```bash
uv run v2x-compile -i <path-to-J2735ASN_202409-folder-with-asn-files> -n j2735_202409
```

This generates a Python module at `src/.compiled/v2x_codecs/j2735_202409.py` and installs it as an editable local package.

## Validating Messages

```python
from v2x_msg_validator.validator import V2XMessageValidator

validator = V2XMessageValidator(revision="j2735_202409")
errors = validator.validate(data)  # data is a dict with messageId and value
```

Each error has:
- `key` — full dot-notation path (e.g., `MapData.intersections[0].refPoint.lat`)
- `code` — integer error code (`INVALID_VALUE`, `MISSING_MANDATORY_KEY`, `INVALID_KEY`, `OUT_OF_CONSTRAINT`, `INVALID_STRUCTURE`)
- `val` — the offending value
- `msg` — human-readable description

## Running Tests

```bash
uv run pytest
```

See [test/README.md](test/README.md) for test strategy details.
