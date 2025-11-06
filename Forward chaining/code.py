facts = {
    "Man(Marcus)",
    "Pompeian(Marcus)"
}

rules = [
    ("Pompeian(x) -> Roman(x)"),
    ("Roman(x) -> Loyal(x)"),
    ("Man(x) -> Person(x)"),
    ("Person(x) -> Mortal(x)")
]

def substitute(statement, var, const):
    return statement.replace(f"({var})", f"({const})").replace(f"{var},", f"{const},").replace(f",{var}", f",{const}")

def forward_chain(facts, rules):
    step = 1
    new_fact_added = True
    while new_fact_added:
        new_fact_added = False
        print(f"\n--- Step {step} ---")
        print("Current Facts:", ", ".join(sorted(facts)))
        for rule in rules:
            premise, conclusion = rule.split("->")
            premise = premise.strip()
            conclusion = conclusion.strip()
            var = 'x'
            for fact in list(facts):
                if premise.startswith(fact.split("(")[0]):
                    const = fact[fact.find("(")+1:fact.find(")")]
                    new_fact = substitute(conclusion, var, const)
                    if new_fact not in facts:
                        print(f"Applied Rule: {rule}")
                        print(f"Matched Fact: {fact}")
                        print(f"Inferred: {new_fact}")
                        print("---------------------------------")
                        facts.add(new_fact)
                        new_fact_added = True
        step += 1
    return facts

print("=== Forward Reasoning Process ===")
derived_facts = forward_chain(facts.copy(), rules)

query = "Mortal(Marcus)"
print("\n=== Final Result ===")
if query in derived_facts:
    print(f" Query '{query}' is PROVED TRUE.")
else:
    print(f" Query '{query}' cannot be proved from the Knowledge Base.")
