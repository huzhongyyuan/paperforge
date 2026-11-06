"""End-to-end test of the facts.md handoff. Run with a Python that has the framework-figure dependencies."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
FIG = SKILL
sys.path[:0] = [str(SKILL / 'scripts'), str(FIG / 'scripts')]
from check_section import check as check_section
from check_terms import check as check_terms
from figkit import Figure, noise_image

FACTS = HERE / 'fictional/facts.md'
GOOD = 'We propose the Frequency-routed Motion Prior, Band-wise Test-time Adaptation and the Spectral Alignment Loss. '
fails = 0


def expect(name, ok, detail=''):
    global fails
    fails += not ok
    print(('PASS' if ok else 'FAIL'), name, detail if not ok else '')


def levels(items, level):
    return [m for l, m in items if l == level]


def check(facts, texts, labels):
    # These upstream fixtures are complete-method / overview tests.
    return check_terms(facts, texts, labels, require_in=[n for n in ('method', 'figure')
                                                      if n in texts or n == 'figure' and labels is not None])


def figure(out, facts=None, title='Overview', labels=('Frequency-routed Motion Prior', 'BTA', 'Spectral Alignment Loss'), notes=(('Curves', 'conceptual'),)):
    f = Figure(1200, 400, title)
    f.image(noise_image(64), 20, 20, 150)
    for i, l in enumerate(labels):
        f.block(220, 20 + i * 110, 700, 90, l.split('|'))
    for p, w in notes:
        f.schematic(p, w)
    f.save(out, facts=facts)
    return json.loads((Path(out) / 'labels.json').read_text())['labels']


expect('a shared template is available', (SKILL / 'references/facts-template.md').is_file())

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    facts = d / 'facts.md'
    shutil.copy(FACTS, facts)
    before = facts.read_text()

    # ---- names
    labels = figure(d / 'a', facts)
    r = check(facts, {'method': GOOD}, labels)
    expect('clean text and figure pass', not r, r)
    r = check(facts, {'method': GOOD.replace('Frequency-routed', 'Frequency routed')}, labels)
    expect('a missing hyphen fails', any('differs' in m for m in levels(r, 'FAIL')), r)
    r = check(facts, {'method': GOOD.replace('Spectral Alignment Loss', 'Spectral Alignment Losses')}, labels)
    expect('a plural warns and the exact name is reported missing', any('differs' in m for m in levels(r, 'WARN')) and levels(r, 'FAIL'), r)
    r = check(facts, {'method': GOOD + 'Fine motion and video motion both matter, as the motion shows.'}, labels)
    expect('ordinary words near the method name do not warn', not r, r)
    r = check(facts, {'method': GOOD.replace('Band-wise Test-time Adaptation', 'adaptation')}, labels)
    expect('a module missing from the method fails', levels(r, 'FAIL'), r)
    r = check(facts, {'method': GOOD.lower().replace('spectral', 'Spectral')}, labels)
    expect('case differences pass', not r, r)
    r = check(facts, {'method': GOOD.replace('Band-wise Test-time Adaptation', 'BTA')}, labels)
    expect('an alias passes', not r, r)
    r = check(facts, {'intro': 'We present TideMotion.'}, labels)
    expect('a short intro need not enumerate all modules', not r, r)
    r = check(facts, {'method': GOOD + 'Tide Motion is fast.'}, labels)
    expect('a split method name fails', any('Tide Motion' in m for m in levels(r, 'FAIL')), r)
    tex = r'\subsection{Frequency-routed Motion Prior} We add the \textbf{Band-wise Test-time Adaptation} and the Spectral Alignment Loss~\cite{a}.'
    r = check(facts, {'method': tex}, labels)
    expect('LaTeX input passes', not r, r)
    r = check(facts, {'method': GOOD}, figure(d / 'b', labels=('Freq-routed Motion Prior', 'BTA', 'Spectral Alignment Loss')))
    expect('a drifted figure label is caught', any(m.startswith('figure:') for _, m in r), r)
    r = check(facts, {'method': GOOD}, figure(d / 'c', labels=('Frequency-routed|Motion Prior', 'BTA', 'Spectral Alignment Loss')))
    expect('a name split over two lines in a block passes', not levels(r, 'FAIL'), r)
    r = check(facts, {'method': GOOD}, figure(d / 'e', labels=('BTA', 'Spectral Alignment Loss')))
    expect('a module missing from the figure fails', any('figure: module not found' in m for m in levels(r, 'FAIL')), r)

    # ---- schematic notes
    s = facts.read_text()
    expect('notes are written', '- Curves: conceptual' in s, s[-300:])
    expect('the rest of facts.md is unchanged', s.startswith(before.rstrip()), '')
    figure(d / 'a', facts, notes=(('Curves', 'now measured elsewhere'),))
    s = facts.read_text()
    expect('rebuilding replaces the block', s.count('figure:Overview:start') == 1 and 'now measured' in s and '- Curves: conceptual' not in s, s[-300:])
    figure(d / 'f', facts, title='Second figure', notes=())
    s = facts.read_text()
    expect('a second figure gets its own block', 'figure:Second figure:start' in s and 'now measured' in s and 'No schematic parts declared' in s, s[-400:])
    plain = d / 'plain.md'
    plain.write_text('# Facts: X\n\n## Method\n\n- Name: X\n')
    figure(d / 'g', plain)
    expect('a missing Figure notes heading is added', '## Figure notes' in plain.read_text(), plain.read_text())

    r = check(facts, {'method': GOOD.replace('Spectral Alignment Loss', 'Spectral Alignment Losses are used')}, labels)
    expect('overlapping variants report once', len([m for m in levels(r, 'WARN') if 'differs' in m]) == 1, r)
    r = check(facts, {'method': GOOD + 'One tide per motion, and the Tide runs each loop.'}, labels)
    expect('short words near a one-word name do not warn', not r, r)
    r = check(facts, {'method': GOOD + 'The Motion Prior is learned offline.'}, labels)
    expect('an alias beside the full name passes', not r, r)

    # ---- CLI, on the drafts written earlier
    cmd = [sys.executable, str(SKILL / 'scripts/check_terms.py'), str(facts), '--figure', str(d / 'a/labels.json')]
    for n in ('abstract', 'intro', 'conclusion'):
        cmd += ['--text', f'{n}={HERE / "fictional" / (n + ".txt")}']
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout.strip())
    expect('the fictional drafts pass on the CLI', p.returncode == 0 and 'WARN' not in p.stdout, p.stdout + p.stderr)

# ---- section checks that a real paper exposed
body = ' '.join(['We have shown that this framework works well on the images in our benchmark.'] * 7)
limits = ' '.join(['This costs a lot of time per image at the highest resolution here.'] * 12)
items = check_section('conclusion', body + r' See \cref{tab:speed}. \paragraph{Limitations.} ' + limits)
expect('limitations do not count toward the conclusion', not [m for l, m in items if l != 'OK' and ('words =' in m or 'sentences =' in m)], items)
expect('a cross-reference is not a citation', not [m for _, m in items if 'citation' in m], items)
expect('have shown counts as a claim', not [m for l, m in items if l != 'OK' and 'what the experiments showed' in m], items)
expect('a cross-reference counts as a table reference', not [m for l, m in check_section('experiments', r'See \Cref{tab:main} and \cref{fig:a}.') if l != 'OK' and ('table' in m or 'figure' in m)], '')
expect('a real citation in the conclusion warns', any('citation' in m for _, m in check_section('conclusion', body + r' As in \cite{a}.')), '')
expect('the first stage is not a claim', not [m for _, m in check_section('method', 'The first stage is the sampler. ' * 200) if 'claim' in m], '')
expect('the first framework is a claim', any('claim' in m for _, m in check_section('method', 'This is the first framework to do so. ' * 200)), '')

print('failures:', fails)
sys.exit(1 if fails else 0)
