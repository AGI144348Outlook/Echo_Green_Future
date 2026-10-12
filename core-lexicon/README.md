# Core Lexicon

Installable PWA built as a set of registry tabs: an A–Z dictionary of 1,000 core English words with 2,517 more specific words beneath them in Chinese characters, the 64 I Ching hexagrams, the 27 Hebrew glyphs and 380 Latin prefixes, roots and suffixes, plus a Python console (Pyodide 0.26.4, Python 3.12) bundled locally so everything works without a network after the first visit.

## Files
- `index.html` – the app (Words tab + Python tab)
- `words.json` – the lexicon: `{word: {senses:[{pos, def, ex?}], syn?:[...], z: zipf_frequency}}`
- `hebrew.json` – 22 letters + 5 finals: glyph, Paleo-Hebrew (Unicode Phoenician), name, sound, transliteration, name meaning, pictograph reading, gematria (standard/ordinal/reduced/gadol), Sefer Yetzirah group with element, planet (Gra + Golden Dawn), sign, faculty and month
- `latin.json` – 55 prefixes, 281 roots, 44 suffixes: forms/variants, meaning, Latin source, examples, and the lexicon words built from each
- `codices.json` – Timothy's codices: 7 completed (full text, from AGI144348Outlook/Mashet-Echo-Drive), 52 drafted in ChatGPT sessions (176 versions with chat and date, from Echo_Green_Future's chatgpt-conversation-archive branch), 59 named only
- `characters.json` – 241 character profiles in 11 casts (Nexus Realms Council, Bard Council, TaskForge, Lattice Council, 150+ Professor ASIs, the story casts, orders and classes), built from the ChatGPT archive: summaries (Claude's synthesis), quoted described-as lines, Timothy's own words, voice lines, defining passages, chats, related characters, realms and codices. Grouped by tier (Top Tier: Julian, the Lattice Council and the 2024 Nexus Council; Second Tier: the Bard Council), then by cast. ↑/↓ arrows set a personal order kept in the browser
- `realms.json` – 78 realms in 6 worlds (Nexus Realms, Citadel, Mind Domain architecture, TaskForge, the Lattice, story worlds) with parents, children, linked characters and codices
- `documentation.json` – the Documentation tab: "Recorded, Not Written", a documentary series plan (24 documents) with a corpus dashboard (chats per month, project vs everyday), sources handed over, open leads, attachments, ChatGPT library files and the chat list. Rebuilt as more export files arrive
- `chinese.json` – for 459 of the core words: the WordNet hyponyms one to three levels down (2,517 words), each with traditional + simplified characters, pinyin, a single-character flag, a character-by-character gloss and the base words it falls under
- `pos.json` – word → part-of-speech sets for 82,732 WordNet words, used by the Notation tab's tagger
- `math_formulas.json` – 326 formulas from Babylonian methods to the 1990s: LaTeX, pre-rendered MathML, field, credit, approximate date, era, one-line description
- `math_axioms.json` – 18 axiom systems (86 axioms), 31 step-by-step proofs, 158 theorems with proof sketches
- `math_symbols.json` – 398 symbols: glyph, name, LaTeX, meaning(s), field, Unicode code points and name, who introduced it where known
- `sci_laws.json` – 301 scientific laws across 14 fields (mechanics to economics), same fields as the formulas; physics already in the Formulas tab is not repeated
- `sci_principles.json` – 22 sets of founding principles (88 items: Newton, thermodynamics, quantum postulates, cell theory, Darwin, plate tectonics…) and 146 theories/discoveries with claim and key evidence
- `sci_symbols.json` – 118 elements (periodic-table layout), 89 units and SI prefixes, 43 CODATA physical constants, 85 notation symbols
- `iching.json` – 8 trigrams + 64 hexagrams (King Wen order): number, 漢字, pinyin, name, upper/lower trigram, lines (bottom first), judgment & image summaries, six line readings, inverse/opposite/nuclear links
- `pyodide/` – the Python runtime, served from your own origin
- `manifest.webmanifest`, `sw.js`, icons – PWA install + offline cache
- `_headers` – correct wasm MIME type on Cloudflare Pages / Netlify

## Deploy
Any static host over HTTPS. Cloudflare Pages: upload this folder as-is. GitHub Pages: push the folder to a repo and enable Pages.
Bump `CACHE` in `sw.js` whenever you change files, so installed copies update.

## Python console
Every registry is loaded as a Python global. `helpme()` lists them all.
- `lexicon` – `define(w)`, `letter(c)`, `find(regex)`, `pos(tag)`, `top(n)`
- `hebrew` – `letter(key)`, `gematria(text, system)`, `group(name)`
- `latin` – `breakdown(word)`, `morpheme(form)`, `meaning(text)`, `words_with(form)`
- `notation` – `slot(key)`, `tag(sentence)` (Legend v0.1, CLR-0043 tagger)
- `codices` – `codex(key)`, `codex_text(key, version)`, `codex_search(term)`
- `characters` – `character(name)`, `tier(name)`, `cast(name)`, `related(name)`, `search_characters(term)`, `my_order()` (the list arrives in your ↑/↓ order)
- `documentation` – `series(part)`, `corpus()`, `chats_in(month)`, `attachments(term)`
- `realms` – `realm(name)`, `realm_tree(world)`, `who_is_in(name)`
- `chinese` – `specifics(word, single=False)`, `hanzi(key)`, `singles()`
- `formulas` – `formula(key)`, `timeline(start, end)`
- `math_axioms` – `axioms(key)`, `proof(key)`, `theorem(key)`
- `symbols` – `symbol(key)`, `symbols_in(field)`
- `sci_laws` – `law(key)`, `laws_in(field)`
- `sci_principles` – `principles(key)`, `discovery(key)`
- `sci_symbols` – `element(key)`, `unit(key)`, `constant(key)`, `notation_sym(key)`, `molar_mass('C6H12O6')`
- `iching` – `hexagram(n | name | pinyin | 漢字 | '111000')`, `trigram(name)`, `change(n, [moving lines])`

## Adding a registry tab
1. Add a JSON data file.
2. Add a `<section class="view" id="v-ID">` and a loader/render function.
3. Add an entry to `REGISTRIES` in `index.html` (`id`, `label`, `count`, `load`, `py: {name, data, boot}`).
4. Add the JSON to `SHELL` in `sw.js` and bump `CACHE`.

## Data source
Word list: top English words by frequency (wordfreq), kept only if they are base forms with a WordNet entry, plus ~60 hand-defined function words (the, of, and…). Definitions and examples: Princeton WordNet 3.0, one sense per part of speech, most-used sense first.
I Ching: structure (sequence, trigrams, relationships) is computed from the line patterns; judgment, image and line texts are original plain-English summaries of the traditional themes, not quotations from any translation.

Latin breakdown: a dynamic-programming parser matches prefix* + root+ + suffix* (plus connecting vowels and English endings like -ed, -ing). Lexicon links use the strict mode; the breakdown box falls back to a loose mode that marks unmatched stems. Homographs (e.g. port = carry / gate) show both meanings because spelling alone can't tell them apart. The JS and Python versions are the same algorithm and were checked to give identical results on 2,203 words.

Chinese data: hierarchy from Princeton WordNet 3.0; Chinese words from the Chinese Open Wordnet (NTU, CC BY 4.0); traditional forms and character glosses from CC-CEDICT (CC BY-SA 4.0); character frequency from the Leiden list; pinyin from pypinyin. A single common character is preferred whenever the Chinese Open Wordnet offers one.

Notation tab: Timothy's Legend v0.1 bracket notation. The tagger is CLR-0043 `grammar.js` from Echo_Green_Future (code-library-registry branch), embedded unchanged; only the word lookup is new (pos.json).

Math registries: content written for this registry, not copied from a source. Formulas and symbols are rendered from LaTeX to MathML at build time with Temml 0.13.5, so the app needs no math library at runtime; MathML displays natively in current browsers, with Noto Sans Math as the font. Dates are approximate and credits list the traditionally recognized contributors; many results had earlier or independent discoverers.

Science registries: laws, principles, theories, units and notation written for this registry. Element data from the `mendeleev` Python package; physical constants are CODATA values via SciPy. LaTeX pre-rendered to MathML with Temml.

Characters and Realms: names were found in Echo_Green_Future's chatgpt-conversation-archive (400 chats). Real people (family history, public figures, simulated author personas) are left out. Summaries are marked as Claude's synthesis; everything else is quoted or counted from the archive. Links between characters and realms come from names appearing in the same paragraph.
