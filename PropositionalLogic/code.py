import itertools

values = [True, False]

def implies(a, b):
    return (not a) or b

def KB(P, Q, R):
    return implies(Q, P) and implies(P, not Q) and (Q or R)

def query_R(P, Q, R):
    return R

def query_R_implies_P(P, Q, R):
    return implies(R, P)

def query_Q_implies_R(P, Q, R):
    return implies(Q, R)

print(f"{'P':^3} {'Q':^3} {'R':^3} {'Q→P':^5} {'P→¬Q':^6} {'Q∨R':^5} {'KB':^4} {'R':^3} {'R→P':^6} {'Q→R':^6}")
print("-" * 60)

kb_models = []
for P, Q, R in itertools.product(values, repeat=3):
    q1 = implies(Q, P)
    q2 = implies(P, not Q)
    q3 = Q or R
    kb_true = q1 and q2 and q3
    r_val = R
    r_imp_p = implies(R, P)
    q_imp_r = implies(Q, R)

    print(f"{P!s:^3} {Q!s:^3} {R!s:^3} {q1!s:^5} {q2!s:^6} {q3!s:^5} {kb_true!s:^4} {r_val!s:^3} {r_imp_p!s:^6} {q_imp_r!s:^6}")

    if kb_true:
        kb_models.append((P, Q, R))
def entails(query):
    for (P, Q, R) in kb_models:
        if not query(P, Q, R):
            return False
    return True

print("\nModels where KB is True:", kb_models)
print("\nEntailment Results:")
print("Does KB entail R?        ->", entails(query_R))
print("Does KB entail (R → P)?  ->", entails(query_R_implies_P))
print("Does KB entail (Q → R)?  ->", entails(query_Q_implies_R))

