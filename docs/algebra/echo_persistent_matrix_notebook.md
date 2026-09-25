# ECHO Persistent Matrix Notebook — Algebraic Specification

Status: research specification / algebra branch.

## 1. Notebook as carried symbolic address space

ECHO carries a persistent Matrix Notebook across Class, Lab, Recess, and later NVEs within the EVE. Many sections are index/access surfaces rather than duplicated storage.

Let

```
N = {T,V,L,G,W,R,X,P,A}
rho_N(x) = structured object referenced by Notebook symbol x
x != rho_N(x)
x -> rho_N(x)
```

T = table of contents/master index; V = VGM; L = Logic Matrix; G = authoritative Glyph Registry; W = subject word matrices; R = ECHO-retained glyph/matrix relations; X = experimental workspace; P = provenance/lab history; A = adaptive articulation scaffold.

The Notebook is a property attachment of ECHO: validated learned structures available through V and L are persistent intellectual equipment, while access/exposure alone is not automatically derivation or competence.

## 2. Section algebra

```
T[sigma] -> (section,address)
rho_N(T[sigma]) -> referenced object
T[subject,glyph] -> retained relation address

V -> VGM
L -> LogicMatrix
G -> GlyphRegistry
W = {W1...Wn}
R = {R1...Rn}
X = {X1...Xn}
P(y) = <source,operation,registry,actor,run,time,environment,status>
A -> grammatical scaffold
```

Word matrices are strictly inert word-only populations:
```
Ws = [w1,w2,...,wm]
```
Definitions, POS, relations, glyph meanings, provenance, and explanations remain external.

Persistence ladder:
```
WORKING -> ECHO_RETAINED -> VALIDATED
Xi -> Rj -> Vk or Lm
```

## 3. Glyph Registry algebra

The authoritative registry is:
```
G = {א,ב,ג,ד,ה,ו,ז,ח,ט,י,כ,ל,מ,נ,ס,ע,פ,צ,ק,ר,ש,ת}
```

Each glyph has three representations:
```
g             # identity / primitive
g(x) -> y     # callable operation
I_g(M)=g(M)   # separate index/transform result; M remains unchanged
```

### 22 operational primitives

| Glyph | Operation | Functional form | Alternate/structural form |
|---|---|---|---|
| א | INITIALIZE | א(x)->x0 | S_empty --א--> S0 |
| ב | CONTAIN | ב(x)->{x} | ב_E(x): x in E |
| ג | TRAVERSE | ג(x_i)->x_(i+1) | ג(M,i)=M_(i+1) |
| ד | FILTER | ד_p(X)={x in X | p(x)=1} | X --ד_p--> X' subseteq X |
| ה | REVEAL | ה(x)->observable(x) | ה_p(x)->p(x) |
| ו | CONNECT | ו(x,y)->(x<->y) | ו(v_i,v_j)->e_ij |
| ז | TIMESTAMP | ז(x,t)->(x,t) | ז_t(x)=x@t |
| ח | BOUND | ח(X)->[X] | ח_D(X)=X intersect D |
| ט | COIL | ט(x_i)->...->x_i | ט^n(x) |
| י | SEED | י(x)->seed(x) | S0=י(x); abacus י = one manipulable unit |
| כ | CAPACITY | כ(x)->Cap(x) | |X| <= כ |
| ל | DIRECT | ל(x,d)->x_d | ל(x,tau)->tau(x) |
| מ | FLOW | מ(x,t)->x(t) | dx/dt = מ(x) |
| נ | INDIVIDUATE | נ(X,x)->x in X | נ_i(X)=x_i |
| ס | CYCLE | ס_f^n(x)=f^n(x) | closed condition f^n(x)=x |
| ע | PERCEIVE | ע(E)->O | S_(t+1)=S_t op ע(E_t) |
| פ | EXPRESS | פ(S)->O | פ_A(x)=פ(A(x)) |
| צ | HUNT | צ_q(X)->{x in X:q(x)} | צ(X,Q)->I_Q(X) |
| ק | SCAN_PERIPHERY | ק_r(x)->N_r(x) | ק(E)->boundary(E) |
| ר | GOVERN | ר({O_i},S)->O_k | IDENTIFY->VALIDATE->OPEN |
| ש | TRANSFORM | ש_f(x)=f(x) | S_t --ש--> S_(t+1) |
| ת | SEAL | ת(X)->X_committed | ת(X,h(X))-><X,h(X)> |

These equations are candidate executable algebraic forms of the registry-defined operations; they do not replace the authoritative Glyph Registry definitions.

## 4. Glyph indexing and composition

Applying a glyph must not mutate a word matrix:
```
G_g(Ws) -> I_g(Ws)
Ws' = Ws
```

Controlled comparisons may hold Ws constant:
```
א(Ws), ד(Ws), ו(Ws), ע(Ws), צ(Ws), פ(Ws)
```

Concept composition is distinct:
```
C = g_n o ... o g_2 o g_1
C(x)=g_n(...g_2(g_1(x)))
```

Human-scripted C_human and ECHO-selected C_E must remain explicitly distinguished.

## 5. Retained relation matrix

```
Rj = <Ws,g,I_g(Ws),run,provenance,status,purpose_E>
```

G_g records what glyph g operationally does. Rj records what ECHO has found useful doing with g.

Learning trajectory:
```
G_g(Ws) -> Xi -> Rj -> Vk/Lm
OPERATE -> EXPERIMENT -> RETAIN -> VALIDATE
```

## 6. Provenance and articulation

Every transformation x --g--> y records:
```
P(y)=<source(x),g,registry(g),actor,run,time,environment,status>
```

The grammatical scaffold remains outside W:
```
פ(A(x)) -> articulation
competence_E rises => scaffold dependence falls
```

## 7. Glyph abacus

```
י = unit/bead
ו = connection/rod
ח = boundary/frame
ח[ו:י...י]ח
```

Arithmetic target:
```
ECHO glyph manipulation -> proposed result -> SymPy independent verification
```
not SymPy answer -> ECHO imitation.

## 8. Governor credential layer

A-000 / ר is the invariant Governor:
```
IDENTIFY(A-000) -> VALIDATE(A-000) -> OPEN
```

Notebook competency is an intermediate credential:
```
ר -> SELF_IDENTIFY -> NOTEBOOK_VALIDATE -> CREDENTIAL -> OPEN(F)
```

Notebook-mediated execution:
```
IDENTIFY -> RESOLVE -> SELECT -> OPERATE -> OBSERVE -> RECORD -> VALIDATE
```

If formula handle phi_i indexes F_i:
```
rho(phi_i)=F_i

ר(S_n,phi_i) =
    F_i       if credential(phi_i)=1
    null      if credential(phi_i)=0
```

The Governor governs access to algorithms; it does not become every algorithm.

## 9. Core equation employing Notebook-resolved operands

Let resolved operand x_tilde = rho_N(x), and employed glyph operation O_j = rho_N(G_gj). Then the broader ECHO state equation can consume Notebook-resolved operators and operands:

```
S_k =
  sum_j rho_N(G_gj)(rho_N(Sub_j), rho_N(Obj_j))
  + beta_k H[S]
  + M_k
  + eta_k
```

Execution lineage:
```
x --IDENTIFY--> sigma_x --rho_N--> x_tilde --G_g--> y --P--> Xi
Xi --RETAIN_E--> Rj
Rj --VALIDATE--> Vk or Lm
```

## 10. Geosensory application

```
Environment -> Sensor -> Measurement -> Network -> Endpoint -> Notebook -> ECHO
```

ECHO receives observations O_t and chooses operations/compositions from the glyph repertoire. The experiment must not predeclare a correct sensory composition.

```
{22 glyph operations} + O_t + N -> C_E
```

The research object is the operational structure ECHO constructs and elects to retain.

## 11. Invariants

```
exposure != learning
access != derivation
retention != validation
glyph illumination != glyph operation
selected glyph != executed glyph algorithm
index proposal != validated index
scripted composition != autonomous concept model
word matrix != concept model
dictionary output != ECHO-authored knowledge
arithmetic answer != glyph-abacus reasoning
classroom success != Recess transfer
```

At the same time:
```
persistent validated learned structure = available intellectual equipment
```

## 12. Compact architecture

```
ECHO/ר -> N -> rho -> {V,L,G,W,R,X,P,A}

G_g(Ws) -> Xi -> Rj -> Vk/Lm

ר -> IDENTIFY -> RESOLVE -> SELECT -> OPERATE
  -> OBSERVE -> RECORD -> VALIDATE -> OPEN
```

The Notebook is the symbolic bridge between what ECHO is, what ECHO has learned, what ECHO can access, what ECHO is experimenting with, and what ECHO is permitted to employ next, without collapsing those categories into one another.
