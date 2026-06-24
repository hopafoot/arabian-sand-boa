# Run me with the arabian_sand_boa interpreter:
#     python3 arabian_sand_boa example.py
#     python3 arabian_sand_boa --debug example.py
#
# String conditions are natural-language clauses judged by the LLM against the
# in-scope variables. Normal (non-string) conditions resolve the usual way.

name = "Ada"
age = 29
country = "United Kingdom"
balance = -12.50
roles = ["engineer", "admin"]

# Natural-language clause -> sent to the LLM with the variables above.
if "the person is old enough to legally drink in their country":
    print(f"{name} can be served a drink")
else:
    print(f"{name} cannot be served a drink")

# The LLM can reason over collections in scope, too.
if "the user has administrative privileges":
    print(f"{name} sees the admin panel")
else:
    print(f"{name} sees the normal dashboard")

# A clause the variables actively contradict.
if "the account balance is healthy and in the black":
    print("account: good standing")
else:
    print("account: overdrawn, send a warning")

# A plain boolean condition -> no LLM call, resolved by bool() as always.
if balance < 0:
    print(f"(reminder: {name}'s balance is {balance})")
