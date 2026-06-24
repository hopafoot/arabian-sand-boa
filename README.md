# arabian_sand_boa

Run a Python file where **string `if` conditions are decided by an LLM**.

`arabian_sand_boa` is a single, dependency-free script (standard library only).
It reads your target file, rewrites every `if`/`elif` at the AST level, and runs
it. When a condition resolves to a **non-empty string**, the string is treated as
a natural-language clause and sent to an LLM along with the variables currently
in scope; the model's `True`/`False` answer decides which branch runs. Every
other condition resolves the normal way via `bool()`.

## Usage

```sh
./arabian_sand_boa <file.py> [args...]          # it's executable
```

`--debug` (or `-d`) prints, to stderr, the exact prompt sent to the LLM and the
raw reply for each clause it evaluates.

The target file runs with `__name__ == "__main__"`, so its main block executes.

## Configuration

The LLM endpoint is configured entirely through environment variables, read
lazily — a target that only uses ordinary (non-string) conditions never needs
them.

| Variable           | Meaning                            |
| ------------------ | ---------------------------------- |
| `BOA_LLM_URL`      | Full chat-completions endpoint URL |
| `BOA_LLM_API_KEY`  | Bearer token for that endpoint     |
| `BOA_LLM_MODEL`    | Model name to request              |

The endpoint is expected to speak the OpenAI-style chat-completions protocol
(`POST` a JSON body with `model` and `messages`, get back
`choices[0].message.content`).

Copy `.example.env` to `.env`, fill in your values, and load it:

```sh
cp .example.env .env
# edit .env
set -a; source .env; set +a

python3 arabian_sand_boa example.py
```

`.env` is gitignored; `.example.env` is the tracked template. If any required
variable is missing when an LLM call is needed, the run fails with a clear error
naming the missing variable(s).

## How it works

1. **Rewrite.** An `ast.NodeTransformer` replaces each `if <test>:` with
   `if __if_hook__(<test>, "<source text of test>"):`.
2. **Decide.** `__if_hook__` evaluates `<test>`. If it's a non-empty string, the
   hook gathers the caller's non-dunder local variables and asks the LLM whether
   the clause holds. Otherwise it returns `bool(<test>)` and no API call is made.
3. **Parse.** The reply is lower-cased and stripped: `true` → take the branch,
   `false` → skip it, anything else → take the branch (cautious default).

## Privacy and safety

- **Your local variables leave the machine.** For every string condition, the
  in-scope (non-dunder) local variables are serialized and sent to the
  configured LLM endpoint. Do not run this over sensitive data.
- An LLM call fires for **every executed string condition**, so loops with
  string clauses are slow and chatty against the endpoint.
- Decisions are only as reliable as the model and the wording of your clause,
  and may vary between runs.

## Example

See `example.py` for a runnable showcase mixing natural-language clauses
(drinking age, admin privileges, account health) with an ordinary boolean
condition.
