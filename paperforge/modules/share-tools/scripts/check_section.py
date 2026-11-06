#!/usr/bin/env python3
"""Optional section-style diagnostics, not scientific or venue acceptance gates.

Usage: check_section.py SECTION FILE [--json]. Valid input exits 0 even with
warnings: word ranges and observed structures describe a small source corpus.
"""
import argparse, json, re, sys


def strip_latex(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    s = re.sub(r'\\cite[a-z]*\*?(?:\[[^\]]*\])?\{[^}]*\}', ' CITE ', s)
    s = re.sub(r'\\label\{[^}]*\}', ' ', s)
    # Keep the target, as sections are checked for references to tables and figures.
    s = re.sub(r'\\(?:[cC]ref|ref|eqref|autoref)\*?\{([^}]*)\}', r' REF:\1 ', s)
    s = re.sub(r'\\begin\{(?:equation|align|figure|table)\*?\}.*?\\end\{(?:equation|align|figure|table)\*?\}', ' ', s, flags=re.S)
    s = re.sub(r'\\item\b', '\n- ', s)
    s = re.sub(r'\\(?:begin|end)\{[^}]*\}', ' ', s)
    s = re.sub(r'\\(?:section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}', r'\n## \1\n', s)
    s = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\[a-zA-Z]+\*?', ' ', s)
    return s.replace('{', '').replace('}', '').replace('~', ' ')


def words(s):
    return len([w for w in s.split() if re.search(r'[A-Za-z0-9]', w)])


def sentences(s):
    s = re.sub(r'\b(e\.g|i\.e|et al|etc|vs|Fig|Eq|Sec)\.', r'\1', s)
    return len([x for x in re.split(r'(?<=[.!?])\s+', s.strip()) if words(x) > 2])


def bullets(s):
    return re.findall(r'^\s*(?:[-•∗*]|\d+[.)])\s+(\S.*)$', s, re.M)


class Report:
    def __init__(self):
        self.items = []

    def warn(self, msg): self.items.append(('WARN', msg))
    def ok(self, msg): self.items.append(('OK', msg))

    def need(self, cond, msg, level='warn'):
        if cond:
            self.ok(msg)
        else:
            getattr(self, level)('missing: ' + msg)

    def rng(self, name, v, lo, hi, tlo, thi):
        """Both ranges are descriptive style hints, never acceptance thresholds."""
        if v < lo or v > hi:
            self.warn(f'{name} = {v}, outside the source sample range {lo}-{hi}')
        elif v < tlo or v > thi:
            self.warn(f'{name} = {v}, outside the target {tlo}-{thi}')
        else:
            self.ok(f'{name} = {v}')


CHALLENGE = r'challeng|however|suffer|restrict|nevertheless|struggl|limited|lack|yet\b|despite|unfortunately'
PROPOSE = r'\bwe\s+(?:\w+\s+)?(?:propose|present|introduce|design|develop)|\bwe\s+study|\bthis (?:paper|work) (?:proposes|presents|introduces)'
ASSERT = r'demonstrat|outperform|achiev|superior|verif|show that|have shown|results? (?:show|indicate)|experiments?'
FIRST = r'\bthe first\s+(?:[\w-]+\s+){0,3}?(?:method|framework|model|approach|work|system|benchmark|dataset|to\b)|best of our knowledge'
NUMBER = r'\d+(?:\.\d+)?\s*(?:%|×|\\times|x\b)|R@\d'


def flags(s, r):
    for m in sorted({m.group(0).lower() for m in re.finditer(FIRST + r'|state-of-the-art', s, re.I)}):
        r.warn(f'confirm this claim has evidence: "{m}"')
    n = len(re.findall(r'\[TODO|\[CITE', s))
    if n:
        r.warn(f'{n} [TODO]/[CITE] placeholder(s) still open')


def title(s, r):
    s = s.strip()
    r.rng('words', words(s), 3, 12, 4, 11)
    if ':' not in s:
        r.warn('no colon; 20/21 titles are "Name: description"')
    if re.search(r'[?!]', s):
        r.warn('question or exclamation mark; confirm the intended title style')
    if re.search(r'\b(novel|rethinking|revisiting)\b|^a unified', s, re.I):
        r.warn('generic word the corpus avoids')
    if re.search(NUMBER, s):
        r.warn('number in the title; the corpus keeps numbers for the experiments')


def abstract(s, r):
    r.rng('words', words(s), 160, 262, 185, 235)
    r.rng('sentences', sentences(s), 6, 16, 8, 14)
    if bullets(s):
        r.warn('abstract uses bullets; check the venue format')
    r.need(re.search(CHALLENGE, s, re.I), 'challenge or contrast sentence', 'warn')
    r.need(re.search(PROPOSE, s, re.I), 'statement of the method', 'warn')
    r.need(re.search(ASSERT, s, re.I), 'closing claim from experiments', 'warn')


def intro(s, r):
    r.rng('words', words(s), 480, 1050, 620, 900)
    r.need(re.search(PROPOSE, s, re.I), 'statement of the method')
    r.need(re.search(r'however|yet\b|despite|unfortunately|nevertheless', s, re.I), 'turn against existing work', 'warn')
    b = bullets(s)
    if not b:
        r.warn('no contribution bullets; 19/21 have them')
    else:
        r.rng('contribution bullets', len(b), 2, 5, 3, 4)
        if not re.search(r'experiment|evaluat|benchmark|dataset|results?', b[-1], re.I):
            r.warn('last bullet is not experiments or a benchmark (12/19 are)')
    r.need(re.search(r'contributions?', s, re.I), 'contributions lead-in', 'warn')


def related(s, r):
    r.rng('words', words(s), 200, 850, 300, 650)
    topics = len(re.findall(r'^\s*(?:\*\*[^*\n]{3,70}\*\*|#{1,6}\s+\S.*)', s, re.M)) + len(re.findall(r'\\(?:paragraph|textbf)\{', s))
    if topics < 2:
        r.warn('fewer than 2 explicit topics; confirm whether grouping helps this section')
    elif topics > 4:
        r.warn(f'{topics} topics; the corpus mostly has 2-3')
    else:
        r.ok(f'topics = {topics}')
    if not re.search(r'\b(our|we|in contrast|unlike|different from)\b', s[-600:], re.I):
        r.warn('does not close by relating back to this work (13/19 do)')


def method(s, r):
    n = words(s)
    if n < 500:
        r.warn(f'words = {n}; corpus sections are mostly above 900')
    else:
        r.ok(f'words = {n}')
    r.need(re.search(r'\b(?:Fig\.?|Figure)\s*~?\d|\bREF\b', s), 'reference to the pipeline figure', 'warn')
    for h in re.findall(r'^\s*#{1,6}\s+(.+)$', s, re.M):
        if re.search(r'^(?:[\d.]*\s*)?(overview|loss functions?|implementation|module \w+|representation|method overview)\s*$', h.strip(), re.I):
            r.warn(f'generic heading; name the mechanism: {h.strip()!r}')


def experiments(s, r):
    r.need(re.search(r'implementation|experimental setup|\bsettings?\b', s, re.I), 'implementation details', 'warn')
    r.need(re.search(r'baseline|compar', s, re.I), 'baseline comparison')
    r.need(re.search(r'ablation', s, re.I), 'ablation study', 'warn')
    r.need(re.search(r'\bTable\b|tab:', s), 'reference to a table', 'warn')
    r.need(re.search(r'\bFig(?:ure|\.)?\b|fig:', s), 'reference to a figure', 'warn')
    r.need(re.search(r'\bGPU|A100|H20|RTX|V100|TITAN', s), 'hardware (13/21 state it)', 'warn')


def conclusion(s, r):
    # The ranges describe the summary; 9/21 papers state limitations separately.
    s = re.split(r'^\s*(?:#{1,6}\s*|\*\*)(Limitations?)\b', s + '\n', maxsplit=1, flags=re.M | re.I)[0]
    r.rng('words', words(s), 55, 200, 80, 140)
    r.rng('sentences', sentences(s), 2, 10, 4, 7)
    r.need(re.search(ASSERT, s, re.I), 'statement of what the experiments showed', 'warn')
    if re.search(r'(?<!\[)\bCITE\b', s):
        r.warn('citation in the conclusion')


SECTIONS = dict(title=title, abstract=abstract, intro=intro, related=related, method=method, experiments=experiments, conclusion=conclusion)


def check(section, raw):
    s = strip_latex(raw) if '\\' in raw else raw
    r = Report()
    SECTIONS[section](s, r)
    flags(s, r)
    return r.items


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('section', choices=SECTIONS)
    p.add_argument('file')
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    items = check(a.section, open(a.file, encoding='utf-8').read())
    if a.json:
        print(json.dumps(items, ensure_ascii=False, indent=1))
    else:
        for level, msg in items:
            print(f'{level:4} {msg}')
    # Style findings do not invalidate otherwise legitimate writing.
    sys.exit(0)


if __name__ == '__main__':
    main()
