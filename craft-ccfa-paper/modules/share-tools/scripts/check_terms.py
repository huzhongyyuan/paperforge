#!/usr/bin/env python3
"""Check that module names match paper/facts.md in the text and the figure.

Usage: check_terms.py FACTS [--text NAME=FILE ...] [--figure LABELS.json]
                      [--require-in method] [--require-in figure]

Text NAME is the section, such as method, intro or abstract. Case differences are accepted, since
body text often lowercases a heading. Exit status is 1 if any FAIL is reported.
"""
import argparse, difflib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_section import strip_latex

FUZZY = .8
# A full method/overview often includes all modules, but a local excerpt or
# module-detail figure need not. Only explicitly required scopes fail omissions.
EXPECTED = {'method', 'figure'}


def parse_facts(path):
    s = Path(path).read_text(encoding='utf-8')
    m = re.search(r'^- Name:\s*(.+?)\s*$', s, re.M)
    if not m or m.group(1).startswith('[TODO'):
        raise ValueError('facts: the method name is not filled in')
    method = m.group(1)
    sec = re.search(r'^## Modules\s*$(.*?)(?=^## |\Z)', s, re.M | re.S)
    if not sec:
        raise ValueError('facts: no "## Modules" section')
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in sec.group(1).splitlines() if l.strip().startswith('|')]
    if len(rows) < 2:
        raise ValueError('facts: the Modules table needs a header and separator')
    head = [c.lower() for c in rows[0]]
    if 'name' not in head or 'aliases' not in head:
        raise ValueError('facts: the Modules table needs Name and Aliases columns')
    if any(not re.fullmatch(r':?-{3,}:?', cell) for cell in rows[1]):
        raise ValueError('facts: invalid Modules table separator')
    ni, ai = head.index('name'), head.index('aliases')
    modules = []
    for r in rows[2:]:
        if len(r) != len(head):
            raise ValueError('facts: a Modules row has the wrong number of columns')
        if r[ni].startswith('[TODO') or not r[ni]:
            raise ValueError('facts: a module name is not filled in')
        modules.append((r[ni], [a.strip() for a in r[ai].split(',') if a.strip()]))
    if not modules:
        raise ValueError('facts: the Modules table is empty')
    owners = {method.casefold(): method}
    for canonical, aliases in modules:
        for form in [canonical] + aliases:
            key = ' '.join(form.casefold().split())
            if key in owners and owners[key] != canonical:
                raise ValueError(f'facts: ambiguous module name or alias: {form!r}')
            owners[key] = canonical
    return method, modules


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def tokens(s):
    """(start, end, word stripped of surrounding punctuation), so offsets can mark what is already matched."""
    out = []
    for m in re.finditer(r'\S+', s):
        w = m.group(0)
        lead = len(w) - len(w.lstrip('([{"\'*_`'))
        core = w.strip('()[]{}"\'*_`.,;:!?')
        if re.search(r'[A-Za-z0-9]', core):
            out.append((m.start() + lead, m.start() + lead + len(core), core))
    return out


def scan(text, terms):
    """Returns (forms found exactly, variants as (kind, found, canonical))."""
    toks = tokens(text)
    known = {}
    for canon, aliases in terms:
        for form in [canon] + aliases:
            known[' '.join(form.lower().split())] = canon
    found, spans = set(), []
    for form, canon in known.items():
        n = len(form.split())
        for i in range(len(toks) - n + 1):
            if ' '.join(t[2].lower() for t in toks[i:i + n]) == form:
                found.add((canon, form))
                spans.append((len(norm(form)), set(range(i, i + n))))
    variants, near = set(), []
    for form, canon in known.items():
        target = norm(form)
        if len(target) < 6:
            continue
        n = len(form.split())
        # Only an equal or longer exact match settles these words. A short alias inside a
        # misspelt full name must not hide the misspelling.
        used = set().union(*[s for size, s in spans if size >= len(target)])
        for size in range(1, n + 3):
            # Fuzzy matching compares like with like, or "fine motion" would match "TideMotion".
            fuzzy = abs(size - n) <= 1 and (n > 1 or size == 1)
            for i in range(len(toks) - size + 1):
                if used.intersection(range(i, i + size)):
                    continue
                raw = ' '.join(t[2] for t in toks[i:i + size])
                nr = norm(raw)
                if not nr or raw.lower() in known:
                    continue
                if nr == target:
                    variants.add(('FAIL', raw, canon))
                elif fuzzy and abs(len(nr) - len(target)) <= (1 if n == 1 else len(target) * .5):
                    sm = difflib.SequenceMatcher(None, nr, target)
                    if sm.quick_ratio() >= FUZZY and sm.ratio() >= FUZZY:
                        near.append((sm.ratio(), canon, raw, set(range(i, i + size))))
    # Overlapping windows are one finding: keep the closest match in each region.
    taken = {}
    for _, canon, raw, span in sorted(near, key=lambda x: (-x[0], x[2])):
        if not taken.setdefault(canon, set()) & span:
            taken[canon] |= span
            variants.add(('WARN', raw, canon))
    return found, variants


def check(facts, texts, labels, require_in=()):
    method, modules = parse_facts(facts)
    require_in = set(require_in)
    supplied = set(texts) | ({'figure'} if labels is not None else set())
    if require_in - supplied:
        raise ValueError('required scopes have no input: ' + ', '.join(sorted(require_in - supplied)))
    items = []
    terms = [(method, [])] + modules
    for name, body in texts.items():
        body = re.sub(r'\s+', ' ', strip_latex(body) if '\\' in body else body)
        found, variants = scan(body, terms)
        have = {c for c, _ in found}
        for canon, _ in modules:
            if canon not in have:
                if name in require_in:
                    items.append(('FAIL', f'{name}: module not found: {canon!r}'))
                elif name in EXPECTED:
                    items.append(('WARN', f'{name}: module not mentioned: {canon!r}'))
        for level, raw, canon in sorted(variants):
            items.append((level, f'{name}: {raw!r} differs from {canon!r}; use the exact name or add an alias'))
    if labels is not None:
        have = set()
        for label in labels:
            found, variants = scan(re.sub(r'\s+', ' ', label), terms)
            have |= {c for c, _ in found}
            for level, raw, canon in sorted(variants):
                items.append((level, f'figure: {raw!r} differs from {canon!r}; use the exact name or add an alias'))
        for canon, _ in modules:
            if canon not in have:
                level = 'FAIL' if 'figure' in require_in else 'WARN'
                items.append((level, f'figure: module not found: {canon!r}'))
    return list(dict.fromkeys(items))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('facts')
    p.add_argument('--text', action='append', default=[], metavar='NAME=FILE')
    p.add_argument('--figure', metavar='LABELS.json')
    p.add_argument('--require-in', action='append', default=[], metavar='SCOPE',
                   help='require every registered module in this supplied complete scope (e.g. method or figure)')
    a = p.parse_args()
    if not a.text and not a.figure:
        p.error('supply at least one --text or --figure input')
    texts = {}
    for t in a.text:
        name, _, path = t.partition('=')
        if not path:
            p.error(f'--text needs NAME=FILE, got {t!r}')
        if name in texts or name == 'figure':
            p.error(f'duplicate or reserved text scope: {name!r}')
        texts[name] = Path(path).read_text(encoding='utf-8')
    labels = json.loads(Path(a.figure).read_text(encoding='utf-8'))['labels'] if a.figure else None
    if labels is not None and (not isinstance(labels, list) or any(not isinstance(l, str) for l in labels)):
        p.error('figure: labels must be a list of strings')
    try:
        items = check(a.facts, texts, labels, require_in=a.require_in)
    except ValueError as e:
        p.error(str(e))
    if not items:
        print('OK   module names are consistent')
    for level, msg in items:
        print(f'{level:4} {msg}')
    sys.exit(1 if any(l == 'FAIL' for l, _ in items) else 0)


if __name__ == '__main__':
    main()
