import itertools

def pred(name, *args):
    return ('pred', name, *args)

def forall(var, f):
    return ('forall', var, f)

def exists(var, f):
    return ('exists', var, f)

def neg(f):
    return ('not', f)

def conj(*args):
    return ('and',) + args

def disj(*args):
    return ('or',) + args

def var(v):
    return ('var', v)


def pretty(f):
    t = f[0]
    if t == 'pred':
        return "{}({})".format(f[1], ", ".join(f[2:]))
    if t == 'not':
        return "¬" + "(" + pretty(f[1]) + ")"
    if t == 'and' or t == 'or':
        op = " ∧ " if t == 'and' else " ∨ "
        return "(" + op.join(pretty(x) for x in f[1:]) + ")"
    if t == 'forall':
        return "∀{} {}".format(f[1], pretty(f[2]))
    if t == 'exists':
        return "∃{} {}".format(f[1], pretty(f[2]))
    return str(f)


A = forall('x',
           disj(
               neg(forall('y', neg(disj(pred('Animal','y'), pred('Loves','x','y'))))),
               exists('y', pred('Loves','y','x'))
           )
)

print("Original formula:")
print(pretty(A))
print()


def eliminate_implications(f):
    
    t = f[0]
    if t in ('pred',):
        return f
    if t == 'not':
        return ('not', eliminate_implications(f[1]))
    if t in ('and','or'):
        return (t,) + tuple(eliminate_implications(x) for x in f[1:])
    if t in ('forall','exists'):
        return (t, f[1], eliminate_implications(f[2]))
    return f

B = eliminate_implications(A)
print("After eliminating implications (no change here):")
print(pretty(B))
print("-------------------------------------------------------------")
print()


def push_negation(f):
    t = f[0]
    if t == 'not':
        inner = f[1]
        it = inner[0]
        if it == 'not':
            return push_negation(inner[1])                
        if it == 'and':
            return disj(*[push_negation(neg(s)) for s in inner[1:]])  
        if it == 'or':
            return conj(*[push_negation(neg(s)) for s in inner[1:]]) 
        if it == 'forall':
            # ¬∀y P  =>  ∃y ¬P
            return exists(inner[1], push_negation(neg(inner[2])))
        if it == 'exists':
            # ¬∃y P  =>  ∀y ¬P
            return forall(inner[1], push_negation(neg(inner[2])))
        return ('not', push_negation(inner))
    elif t in ('and','or'):
        return (t,) + tuple(push_negation(x) for x in f[1:])
    elif t in ('forall','exists'):
        return (t, f[1], push_negation(f[2]))
    else:
        return f

C = push_negation(B)
print("After pushing negations inward :")
print(pretty(C))
print("-------------------------------------------------------------")
print()


def flatten(f):
    t = f[0]
    if t in ('and','or'):
        items = []
        for x in f[1:]:
            y = flatten(x)
            if y[0] == t:
                items.extend(y[1:])
            else:
                items.append(y)
        return (t,)+tuple(items)
    if t in ('not',):
        return ('not', flatten(f[1]))
    if t in ('forall','exists'):
        return (t, f[1], flatten(f[2]))
    return f

D = flatten(C)
print("After simplifying:")
print(pretty(D))
print("-------------------------------------------------------------")
print()


counter = itertools.count()
def standardize_apart(f, env=None):
    if env is None: env = {}
    t = f[0]
    if t == 'pred':
        return ('pred', f[1]) + tuple(env.get(arg, arg) for arg in f[2:])
    if t in ('forall','exists'):
        oldv = f[1]
        newv = f"{oldv}_{next(counter)}"
        env2 = env.copy()
        env2[oldv] = newv
        return (t, newv, standardize_apart(f[2], env2))
    if t in ('and','or'):
        return (t,) + tuple(standardize_apart(x, env) for x in f[1:])
    if t == 'not':
        return ('not', standardize_apart(f[1], env))
    return f

E = standardize_apart(D)
print("After standardizing variables apart:")
print(pretty(E))
print("-------------------------------------------------------------")
print()


skolem_count = itertools.count()
def skolemize(f, universal_vars=None):
    if universal_vars is None: universal_vars = []
    t = f[0]
    if t == 'forall':
        return forall(f[1], skolemize(f[2], universal_vars + [f[1]]))
    if t == 'exists':
        varname = f[1]
        
        sk_name = f"sk_{next(skolem_count)}"
        if universal_vars:
            args = "_".join(universal_vars)
            func = f"{sk_name}({args})"
        else:
            func = f"{sk_name}()"
       
        body = substitute_var(f[2], varname, func)
        return skolemize(body, universal_vars)
    if t in ('and','or'):
        return (t,) + tuple(skolemize(x, universal_vars) for x in f[1:])
    if t == 'not':
        return ('not', skolemize(f[1], universal_vars))
    if t == 'pred':
        return f
    return f

def substitute_var(f, varname, term):
    t = f[0]
    if t == 'pred':
        return ('pred', f[1]) + tuple((term if a == varname else a) for a in f[2:])
    if t in ('and','or'):
        return (t,) + tuple(substitute_var(x, varname, term) for x in f[1:])
    if t in ('forall','exists'):
        
        if f[1] == varname:
            return f
        return (t, f[1], substitute_var(f[2], varname, term))
    if t == 'not':
        return ('not', substitute_var(f[1], varname, term))
    return f

F = skolemize(E)
print("After Skolemization :")
print(pretty(F))
print("-------------------------------------------------------------")
print()


def drop_universal(f):
    t = f[0]
    if t == 'forall':
        return drop_universal(f[2])
    if t in ('and','or'):
        return (t,) + tuple(drop_universal(x) for x in f[1:])
    if t == 'not':
        return ('not', drop_universal(f[1]))
    return f

G = drop_universal(F)
print("After dropping universal quantifiers :")
print(pretty(G))
print("-------------------------------------------------------------")
print()


def to_cnf(f):
   
    if f[0] == 'and':
        return ('and',) + tuple(to_cnf(x) for x in f[1:])
    if f[0] == 'or':
       
        items = [to_cnf(x) for x in f[1:]]
        return distribute_or(items)
    if f[0] == 'not' or f[0] == 'pred':
        return f
    return f

def distribute_or(items):
    
    if not items:
        return ('or',)
    result = items[0]
    for nxt in items[1:]:
        result = distribute_two(result, nxt)
    return result

def distribute_two(a, b):
    
    if a[0] == 'and':
        return ('and',) + tuple(distribute_two(x, b) for x in a[1:])
    if b[0] == 'and':
        return ('and',) + tuple(distribute_two(a, x) for x in b[1:])
    
    a_items = (a[1:] if a[0] == 'or' else (a,))
    b_items = (b[1:] if b[0] == 'or' else (b,))
    return ('or',) + tuple(x for x in list(a_items) + list(b_items))

H = to_cnf(G)
print("After distributing OR over AND (CNF):")
print(pretty(H))
print("-------------------------------------------------------------")
print()


def clauses_of_cnf(f):
    if f[0] == 'and':
        clauses = []
        for x in f[1:]:
            clauses.extend(clauses_of_cnf(x))
        return clauses
    if f[0] == 'or':
       
        lits = []
        for lit in f[1:]:
            lits.append(lit)
        return [lits]
    
    return [[f]]

clauses = clauses_of_cnf(H)
print("Final CNF as clause list:")
for i, cl in enumerate(clauses, 1):
    print(f"Clause {i}: " + " ∨ ".join(pretty(l) for l in cl))
print()
