# RPN Scientific Calculator

A REST API service that evaluates scientific expressions written in
[Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) (RPN),
also known as postfix notation. Built with Python 3, FastAPI, and Poetry.

## Why RPN?

In RPN, operators follow their operands (e.g. `3 4 +` instead of `3 + 4`), which
removes the need for parentheses or operator-precedence rules — the order of
tokens alone determines the order of evaluation. For example, `(3 + 4) * 2` is
written as `3 4 + 2 *`.

## Supported operators

| Operator | Meaning                        | Arity  |
|----------|---------------------------------|--------|
| `+`      | Addition                        | binary |
| `-`      | Subtraction                     | binary |
| `*`      | Multiplication                  | binary |
| `/`      | Division                        | binary |
| `^`      | Exponentiation (power)          | binary |
| `sqrt`   | Square root                     | unary  |
| `sin`    | Sine (radians)                  | unary  |
| `cos`    | Cosine (radians)                | unary  |
| `tan`    | Tangent (radians)                | unary  |
| `log`    | Natural logarithm (base e)      | unary  |

The evaluator rejects malformed expressions with clear error messages, including:

- **Stack underflow** — an operator doesn't have enough operands available.
- **Division by zero**.
- **Unknown operators / non-numeric tokens** — any token that isn't a number
  or one of the supported operators above.
- **Leftover operands** — an expression that doesn't reduce to exactly one
  final result (e.g. `1 2 3 +`).
- **Invalid domain** — e.g. `sqrt` of a negative number, `log` of a
  non-positive number.

## API

### `POST /calculate`

**Request body:**

```json
{ "expression": "3 4 + 2 *" }
```

**Success response (`200 OK`):**

```json
{ "result": 14.0 }
```

**Error response (`400 Bad Request`):**

```json
{ "error": "division by zero" }
```

## Build

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
poetry install
```

## Run

Start the development server with:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive API docs
(Swagger UI) are available at `http://127.0.0.1:8000/docs`.

## Example curl requests

**Basic addition:**

```bash
curl -s -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "3 4 +"}'
# {"result":7.0}
```

**Operator precedence expressed via RPN ordering — `(3 + 4) * 2`:**

```bash
curl -s -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "3 4 + 2 *"}'
# {"result":14.0}
```

**Scientific operators — `sqrt(3^2 + 4^2)`:**

```bash
curl -s -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "3 2 ^ 4 2 ^ + sqrt"}'
# {"result":5.0}
```

**Error case — division by zero (returns HTTP 400):**

```bash
curl -s -X POST http://127.0.0.1:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"expression": "5 0 /"}'
# {"error":"division by zero"}
```

## Testing

Run the unit and integration test suite with:

```bash
poetry run pytest -v
```

Tests cover the happy path, RPN-expressed operator precedence, every
supported operator, and error handling (stack underflow, division by zero,
unknown operators, non-numeric tokens, and invalid math domains).

## Development

Common commands for working on this project:

```bash
# Install runtime + dev dependencies
poetry install

# Run the full test suite
poetry run pytest -v

# Run a single test file or test case
poetry run pytest tests/test_rpn.py -v
poetry run pytest tests/test_rpn.py::test_error_division_by_zero -v

# Start the API with auto-reload for local development
poetry run uvicorn app.main:app --reload
```

Project layout:

```
app/
  main.py    # FastAPI app and the /calculate endpoint
  rpn.py     # RPN evaluation engine (tokenizing, stack, operators)
tests/
  test_api.py   # Integration tests against the HTTP endpoint
  test_rpn.py   # Unit tests for the evaluation engine
```

## License

No license file is currently included in this repository, so all rights are
reserved by default. If you intend to reuse this code, please open an issue
to discuss adding an explicit open-source license (e.g. MIT).
