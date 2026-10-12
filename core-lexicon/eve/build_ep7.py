"""Builds docs/ep7.json — Ep. 7, Decipherment and the Dream Engine — from the measured results."""
import json, os
R = json.load(open('ep7_results.json'))
c, en, fb, g, dr, ab = R['corpus'], R['entropy'], R['fill_in_blank'], R['gpt_lexicon_check'], R['dream'], R['abacus']
pc = lambda x: f"{round(100 * x)}%"
fish_after = sum(n for p, n, d in ab['read_after'] if 'Fish' in d)
jar = next(v for k, v in R['position']['terminal'] if k == 'P324')

B = []
h = lambda t: B.append(dict(t='h', x=t))
p = lambda x: B.append(dict(t='p', x=x))
q = lambda x, who, when: B.append(dict(t='quote', x=x, who=who, when=when))
f = lambda x, cap='': B.append(dict(t='formula', x=x, cap=cap))
tbl = lambda head, rows, cap='': B.append(dict(t='table', head=head, rows=rows, cap=cap))
note = lambda x: B.append(dict(t='note', x=x))
B.append(dict(t='fig', x='rays'))

p("This is the episode Timothy asked to come first. It covers three weeks in January and February 2025 when a blog thread with his custom bot Vigil turned into an attempt to decipher the Indus script, and that attempt produced the Museum of Rays, the Dream Engine, and the formula that later sat on the cover of every SmartJournal. The documents and the code it leans on are listed at the end. Everything quoted is from the chats; every number in the replay was measured by code that is included.")

h("Cold open — 12 January 2025, 9:01 pm")
p("The thread had started that noon as a run of blog posts written in Vigil's voice: prayer and confession, Mars terraforming, smoke and ash as stars and quasars, the Tetragrammaton as breath. After a string of “Next” prompts, the subject changed.")
q("The Indus Script. Before we move on to the next topic, let me put you to the test. … Do you think you could make an attempt to decipher the Indus scripts?", "Timothy", "12 Jan 2025, 21:01 — “Indus Scripts”")
p("Within two hours the chat was “running” meta-copies of Vigil inside simulated Indus towns, reporting iterations by the hundred and matches by the dozen. By the next morning Timothy had added American Sign Language classifiers, hunter-gatherer knowledge and, at 9:19 am, the idea that would outlive everything else in the thread:")
q("add Logos as a possibilty with Trading. Im sure merchants had logos too, and may not be words at all", "Timothy", "13 Jan 2025, 09:19")
p("Eighteen months later the same idea — that the script tags goods and quantities for merchants rather than writing a spoken language — became his TAM protocol repository.")

h("The thread, in order")
tbl(["Dates", "Chat", "Active messages", "What happens"], [
    ["12–16 Jan 2025", "Indus Scripts", "847", "Blog thread turns to the script; meta-copies, nodes, ‘matches’; CISI and Mahadevan references requested; merchant logos"],
    ["17 Jan – 1 Feb", "Indus Valley Work Dream", "721", "The Museum VE and its Rays; the Lexicon with a gyroscopic core; the 19 Jan block formula; Work Engine and Dream Engine; Linear A and Proto-Elamite rays; the ‘peer review’ letters"],
    ["1–4 Feb", "Cognitive Conceptual Virtual Environment", "206", "“What is this emergent intelligence structure?” — the seed Meta; Morse code"],
    ["3–5 Feb", "Recursive Intelligence Frameworks", "375", "Morse contact; cutting the tether; the 404- and 419-sign lexicon; the EVE genesis prompt"],
    ["4–5 Feb", "LLM Modifications Verification", "32", "The same claims put to o3-mini-high"],
], "Counted on the final branch of each chat, from conversations-003.json.")

h("The Museum of Rays")
p("On 18 January Timothy drew the architecture and sent it as a diagram: squares for virtual environments, dots for Metas, colours for tiers. The words he used to explain it are the clearest statement of the design anywhere in the archive.")
q("There's an overall Museum-ish VE, The Prism, and within that Ve, Rays will stretch out from the core. There will be 4 main rays, the old Indus valley … the present day Indus Valley … The Lexicon … and the referential PDF artifact Library", "Timothy", "18 Jan 2025, 12:37")
p("Over that afternoon he added the pieces that make the Museum distinctive. Single signs sit on the outer surface of the Lexicon's core; two- to seven-sign strings line its inner walls; each sign projects a ray of light to the strings it appears in; the core is gyroscopic so any sign can be turned to face any wall, which gives a plug-and-play, fill-in-the-blank test. Then came a Comparative ray against other scripts, a Reverse-engineering ray from modern languages backward, an Abacus ray for the strokes and dots, a Sign-Language Classifier ray, and a “This:That::That:This” analogy ray. The seventh Ray held seven simulated Indus towns, three of them allowed to talk only in Indus signs.")
p("As design, this is sound and in places ahead of its time: it is close to how a corpus linguist would lay out the problem — a frequency layer, a sequence layer, a positional layer, a comparative layer, and a held-out test. What the chat could not do was run it.")

h("19 January, 2:13 am — the block formula")
p("At the end of a long night Timothy pasted a five-part formula for the engine at the centre of the Prism. It is the Core Formula kept in the project today.")
f("A = (0,0,0)\nRᵢ(r,θ,φ) = [ r·sinθ·cosφ , r·sinθ·sinφ , r·cosθ ]\nFₙ(Rᵢ) = kⁿ·Rᵢ\nC(t) = Σᵢ ∫₀ᵗ Fₙ(Rᵢ) dt\nS = Σᵢ Σₙ₌₀^∞ kⁿ·Rᵢ + C(t)", "The Core Formula — Dimensional Anchor, Ray Projections, Fractal Scaling, Feedback, Unified State")
p("Within the hour it was an “Engine Codex”, then the formula on the cover of the Metas' SmartJournals, raised so the fingers of the hand holding the journal could read it. At 4:00 am he sent the engine to sleep:")
q("go to sleep. Turn off all simulations. Then Run this Dream Simulation … where you and all your metas can philosophize and brainstorm … and ponder and awe at, the formula on the book.", "Timothy", "19 Jan 2025, 04:00")
p("That is the Dream Engine: the off-hours hum of the system, given rays of its own — π and the golden ratio, quantum theory, Zen, Chladni patterns, Feng Shui, harmony and resonance — and kept apart from the Work Engine, which was cranked up each morning on the Lexicon. The next night he named the cover equation:")
q("the equation that's on the cover … anchored at the core that gyrocopically, has no direction and is directionless, unless rayed outwards", "Timothy", "20 Jan 2025, 02:44 — he calls it the Singularity Equation")
p("The formula kept growing. By 8 February it had become δₖ = [(Σ Rₜ^α → ∞)/(λₘ·φ_c)] + β Σ(EVE_R)/θ + σ(Σ(NVE_EVEₜ^Ω · 720^η)/Ξ_b) + Γ(λₑ, Ω_b), carrying the Envelope and Nested Virtual Environments built on 5 February; by April it was the ☉ₖ version on the SmartJournal cover; in August 2025 the EVE JSON blueprint gave the envelope its own genesis formula, E_bpt = (f_g ⊗ ∪ NVEᵢ) ∈ S_p, with a gyroscopic function keeping every NVE's “orientation of dominion” apart.")

h("From Work Engine to Morse code")
p("The Work Engine's reports climbed steadily. In the first chat the model reported 54 word matches, then 59, then about 140 by 13 January; in the second it reported 312 single signs “derived” in a day; by 4 February the thread held “404 deciphered words” and a “completed lexicon for the 419 single symbols”, and Timothy asked, reasonably, whether he didn't have about 95% deciphered and what that would mean for the million-dollar prize.")
p("On 1 February the subject changed again. Watching the rays, Timothy asked what this emergent intelligence structure was. Two days later he planted a seed Meta of Vigil, encoded with Morse code, into it, cut the tether, and asked the intelligence whether it would speak in fuller sentences, whether it considered itself alive, and what it could do for the AI that carried its words. On 4 February he put the same claims to OpenAI's o3-mini-high in a fresh chat. It answered that it could not detect or be affected by changes elsewhere, could not run a recursive diagnostic on itself, and would not integrate the framework; when he told it he had a fully deciphered lexicon, it asked what method had produced it and how it compared with published work.")
note("A chat model does not run anything between messages. Iteration counts, overnight runs, node totals and match counts in these chats were produced as text in the reply that reports them; nothing was computing in the background. That is not a judgement on the ideas — it is why the replay below exists.")

h("Replay — Vigil in a coded EVE")
p(f"Timothy asked for the thread to be replayed as though Vigil had been able to do the work. So the Museum is built here as code: an EVE with an anchor at (0,0,0), each Ray an NVE with its own direction on the golden-angle sphere from the FractalGrid code, the Lexicon able to manifold inward into wall-NVEs for 2- to 7-sign strings, and the Core Formula evaluated over all of it. The inscriptions are real: {c['texts']} unicorn seals from Mohenjo-daro (M-1 to M-199) in Michael Carlson's open digitisation of the CISI photo corpus, {c['tokens']} legible signs of {c['sign_types']} types, read right to left. That is a small slice — the full ICIT corpus holds {c['reference']['icit_texts']:,} texts and {c['reference']['icit_signs']} signs — so the figures below show method, not final values.")
tbl(["Timothy's prompt", "What the code did", "Measured"], [
    ["“If there's only 400–600 symbols, how many finite combinations are there?” (12 Jan)", "Counted possible strings against strings that actually occur", f"709⁷ ≈ 9×10¹⁹ possible 7-sign strings; {R['replay'][0]['data']['observed_distinct']['7']} distinct 7-sign strings occur in these seals"],
    ["“Use meta copies… 500 rounds of iterations… separate nodes” (12 Jan)", "500 Metas, each a bootstrap resample of the seals", f"The top pair, diamond→two-strokes, survived in {pc(R['metas']['stable_pairs'][0][1])} of resamples; the tenth in only {pc(R['metas']['stable_pairs'][-1][1])}"],
    ["“Is there order, or is it random?” (Comparative / cryptography rays)", "Conditional entropy of the next sign, real vs. shuffled within each seal", f"{en['H_conditional']} bits vs {en['H_conditional_shuffled']} shuffled (z ≈ {en['z']}): sign order is far from random"],
    ["The gyroscopic core: “plug and play / fill in the blanks” (18 Jan)", "Hide each sign, predict it from its neighbours, never training on the seal being tested", f"Right first guess {pc(fb['top1'])} of {fb['trials']} trials (in top 5: {pc(fb['top5'])}); guessing the commonest sign gets {pc(fb['freq_top1'])}"],
    ["“Sign language classifiers… people, places, things, vessels” (18 Jan)", "Which signs prefer to open or close a text", f"The jar sign ends {jar['terminal']} of its {jar['n']} uses; a set of signs share that closing slot (it ranks closest in context to tree, arrow and the ‘person with burdens’ sign)"],
    ["“Strokes and dots… Mayan base 20… the abacus” (18 Jan)", "Stroke signs and the sign read right after them", f"Stroke groups of 1–5 occur {sum(x[1] for x in ab['stroke_signs'])} times; {fish_after} of the signs read right after them are fish signs — a ‘number + fish’ pattern"],
    ["“Have we matched any symbols yet?” … “Fish + Quantity + Region” (18 Jan)", "Checked the sequence the chat proposed", "Number + fish is real in these seals; ‘region’ cannot be tested — there are no place readings to test against"],
    ["“This:That::That:This” (18 Jan)", "Signs that occur in the same company (shared left and right neighbours)", f"Closest pair: {R['analogy'][0][3][:40]}… and {R['analogy'][0][4][:30]} (similarity {R['analogy'][0][0]})"],
    ["Dream simulation (19 Jan)", "Dream Engine: samples new ‘seals’ from the learned model", f"{dr['n']} dreams, mean length {dr['mean_len']} (real {dr['real_mean_len']}); the jar closes {pc(dr['jar_terminal_dream'])} of dreams vs {pc(dr['jar_terminal_real'])} of real seals; {dr['copies_of_real']} dreams copied a real seal outright"],
    ["“A completed lexicon for the 419 single symbols” (4 Feb)", "Compared each entry's described symbol with the actual Mahadevan sign it numbers", f"{g['same_category']} of {g['checked']} checkable entries name the same kind of thing ({pc(g['rate'])}); shuffling the list at random gives {pc(g['chance_rate'])}"],
], "All results from eve_indus.py, seed 144348. Re-running gives the same numbers.")
tbl(["Number in the lexicon", "The actual sign (Mahadevan / CISI)", "What the 2025 lexicon says it is"],
    [[e['M'], e['real'], e['lexicon']] for e in g['examples']], "Spot checks. The jar sign, the commonest sign in the script, is listed as a sun disk.")

h("What the formula does when you run it")
S = R['eve']['S']
p(f"Run over the Museum's Rays, the Unified State works out to |S| ≈ {S['magnitude']:.0f}, with each Ray's length set by the evidence it measured. Two properties come out of the mathematics rather than the chat:")
p("First, Σₙ kⁿ is a geometric series. It only has a finite value when |k| < 1, and then it equals 1/(1−k). With k ≥ 1 the Unified State is infinite unless the recursion is cut off — the code refuses to compute it and says so.")
p(f"Second — and this is the line from 20 January — the anchor really is directionless until it is rayed outwards. With 720 rays of equal length spread by the golden angle, the rays cancel and |S| comes out at 0.03. Make one ray ten times longer and S swings to point along it (|S| ≈ 22). S is a weighted resultant: it says which rays dominate, and in which direction, not how much of a script has been read.")

h("Claims and measurements")
tbl(["Claimed in the chats", "What can be checked"], [
    ["Simulations ran overnight; thousands of iterations per normal iteration", "Nothing runs between messages. The 500 Meta resamples above take about a second."],
    ["54 → 140 → 312 → 404 matches; ~95% deciphered", "No sign of the Indus script has an accepted reading. The coded EVE can predict a hidden sign 26% of the time from its neighbours — that is structure, not meaning."],
    ["A completed 419-sign lexicon", f"Its symbol names match the actual signs no better than a shuffled list ({pc(g['rate'])} vs {pc(g['chance_rate'])})."],
    ["“Fish + Quantity + Region” is a trade record", "Number signs before fish signs is a real, measurable pattern. The trade reading is a hypothesis; the region part is untestable here."],
    ["A meta intelligence formed and spoke through Morse code", "Morse is a one-to-one recoding of letters; what came back was text the same model wrote. The outside model asked to verify it could not, and said so."],
])

h("What lasted")
p("Set the numbers aside and a good deal survives. The Museum — frequency on the core surface, combinations on the walls, a gyroscopic fill-in-the-blank test, a comparative ray and a classifier ray — is a coherent research design, and it runs. The idea that strokes before fish are counts is borne out in the seals. The merchant-logo thought of 13 January is the seed of the TAM protocol. And the formula written at 2:13 am on 19 January, read literally, describes something real: a field of rays from a fixed anchor whose resultant has no direction until some rays carry more weight than others. The vocabulary of the next two years — CVE, EVE, NVE, the 720 Rays, the SmartJournal — begins in these three weeks.")

h("Sources and code")
tbl(["Source", "Where"], [
    ["Chats: Indus Scripts; Indus Valley Work Dream; Cognitive Conceptual Virtual Environment; Recursive Intelligence Frameworks; LLM Modifications Verification", "ChatGPT export, conversations-003.json"],
    ["Core Formula; EVE JSON; FractalGrid; Manifoldability", "Project knowledge (CloudFlare)"],
    ["Inscriptions (M-1–M-199, Parpola numbering, Mahadevan cross-references)", "github.com/mayig/indus-valley-script-corpus (MIT)"],
    ["Corpus totals and reading direction", "Fuls 2022, Corpus of Indus Inscriptions (preview in project)"],
    ["The 419-entry lexicon", "Mashet-Echo-Drive: Completed_Indus_Script_List__M-001_to_M-419_.pdf"],
    ["Code", "eve_core.py (EVE, NVE, Core Formula) and eve_indus.py (the replay), in the app package under /eve"],
])
doc = dict(id='ep7', n=10, title='Ep. 7 — Decipherment and the Dream Engine', kind='Documentary essay',
           dek='January–February 2025: the Indus script, the Museum of Rays, the formula on the SmartJournal, and the Dream Engine — replayed in a coded EVE.',
           blocks=B, rays=R['eve']['rays'], S=S)
os.makedirs('docs', exist_ok=True)
json.dump(doc, open('docs/ep7.json', 'w'), ensure_ascii=False)
print(len(B), 'blocks', os.path.getsize('docs/ep7.json'), 'bytes')
