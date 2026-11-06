"""Components, lint and export for framework figures. See ../references/guide.md."""
from dataclasses import dataclass
from pathlib import Path
import base64, html, io, json, math, random, re

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'assets/ComicNeue-Regular.ttf'
_metric = ImageFont.truetype(str(FONT), 200)

INK = '#1f1f1f'
GREY = '#595959'

# Fill / stroke pairs sampled from the 2024-2026 first-author figures.
SPATIAL = ('#dceef4', '#237c94')
CROSS = ('#ffdb69', '#c55a11')
TEMPORAL = ('#b6ef07', '#000000')
ENCODER = ('#f4f2f1', '#8c7f8b')
LOSS = ('#d5b9eb', '#7030a0')
CONCAT = ('#e7e6e6', '#8c7f8b')
TEAL = ('#86dfd0', '#000000')
PEACH = ('#fbe5d6', '#c55a11')

# Containers group a sub-network or an idea.
C_NET = ('#fcf4db', '#c55a11')
C_REF = ('#e2f0d9', '#548235')
C_BLUE = ('#dceef3', '#237c94')
C_PINK = ('#fbe5d6', '#b5305f')
C_INFER = ('#f2f2f2', '#8c7f8b')
C_ZOOM = ('#f2f2f2', '#ffc000')

KEY = '#c55a11'     # highlighted words in titles and prompts
PROMPT = '#2e6da4'  # edited words in prompts
PICK = '#e8141c'    # selected frame
PURPLE = '#7030a0'  # loss arrows

LINE_STYLES = {
    'solid': None,
    'dash': '9 6',
    'dot': '2.5 5',
    'dashdot': '12 6 2.5 6',
}


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float
    name: str = ''

    @property
    def left(self): return (self.x, self.y + self.h / 2)
    @property
    def right(self): return (self.x + self.w, self.y + self.h / 2)
    @property
    def top(self): return (self.x + self.w / 2, self.y)
    @property
    def bottom(self): return (self.x + self.w / 2, self.y + self.h)
    @property
    def cx(self): return self.x + self.w / 2
    @property
    def cy(self): return self.y + self.h / 2

    def at(self, side, t=.5):
        """A point on an edge, t in 0..1 along it."""
        if side in ('left', 'right'):
            return (self.x if side == 'left' else self.x + self.w, self.y + self.h * t)
        return (self.x + self.w * t, self.y if side == 'top' else self.y + self.h)


def _esc(s):
    return html.escape(str(s), quote=True)


def text_width(s, size):
    return _metric.getlength(s) * size / 200


def load_image(path, size=None):
    im = Image.open(path).convert('RGB')
    if size:
        side = min(im.size)
        l, t = (im.width - side) // 2, (im.height - side) // 2
        im = im.crop((l, t, l + side, t + side)).resize((size, size), Image.LANCZOS)
    return im


def noise_image(size=256, seed=7):
    rng = random.Random(seed)
    return Image.frombytes('L', (size, size), bytes(rng.randrange(40, 215) for _ in range(size * size))).convert('RGB')


def noised(im, amount=.42, seed=7):
    return Image.blend(im.convert('RGB'), noise_image(im.width, seed).resize(im.size), amount)


def _outline_text(svg):
    """Keep static exports independent of Cairo's platform font substitution.

    The editable SVG/HTML retain text. This derived SVG turns only label text
    into paths from the bundled font, preserving the existing transforms.
    """
    import xml.etree.ElementTree as ET
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath
    ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', ns)
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    root = ET.fromstring(svg)
    font = FontProperties(fname=str(FONT))
    for parent in list(root.iter()):
        for index, node in enumerate(list(parent)):
            if node.tag != f'{{{ns}}}text':
                continue
            text = ''.join(node.itertext())
            size = float(node.attrib.get('font-size', 22))
            x, y = float(node.attrib['x']), float(node.attrib['y'])
            anchor = node.attrib.get('text-anchor', 'start')
            advance = text_width(text, size)
            x -= advance / 2 if anchor == 'middle' else advance if anchor == 'end' else 0
            glyphs = TextPath((0, 0), text, size=size, prop=font)
            commands = []
            for vertices, code in glyphs.iter_segments(curves=True, simplify=False):
                if code == 1: commands.append('M%g %g' % tuple(vertices))
                elif code == 2: commands.append('L%g %g' % tuple(vertices))
                elif code == 3: commands.append('Q%g %g %g %g' % tuple(vertices))
                elif code == 4: commands.append('C%g %g %g %g %g %g' % tuple(vertices))
                elif code == 79: commands.append('Z')
            attrs = {k: v for k, v in node.attrib.items()
                     if k not in ('x', 'y', 'font-size', 'text-anchor')}
            group = ET.Element(f'{{{ns}}}g', attrs)
            ET.SubElement(group, f'{{{ns}}}path', {
                'd': ' '.join(commands),
                'transform': f'translate({x} {y}) scale(1 -1)',
            })
            parent.remove(node)
            parent.insert(index, group)
    return ET.tostring(root, encoding='unicode')


class Figure:
    """A fixed canvas. print_width_in is the printed width at \\textwidth, used by the size lint."""

    def __init__(self, w, h, title, print_width_in=6.7, base=22):
        self.W, self.H, self.title = w, h, title
        self.print_width_in = print_width_in
        self.base = base
        self.parts = []
        self.texts = []      # (x0, y0, x1, y1, string)
        self.solids = []     # (x0, y0, x1, y1, name): opaque things a line must not cross
        self.lines = []      # (points, name)
        self.images = []     # (x0, y0, x1, y1, name)
        self.frames = []     # (x0, y0, x1, y1, name): containers, whose borders text must not straddle
        self.states_used, self.states_in_legend = set(), set()
        self.kinds_used, self.kinds_in_legend = set(), set()
        self.warned = []
        self.notes = []      # (part, why): what is schematic, for the caption
        self.rect(0, 0, w, h, 'white', 'none')

    def add(self, s):
        self.parts.append(s)

    def schematic(self, part, why):
        """Declare a part that is illustrative or a stand-in. save() passes the list on to the caption."""
        self.notes.append((part, why))

    def labels(self):
        """Every drawn string, plus the whole name of each multi-line block."""
        seen = [t[4] for t in self.texts] + [s[4] for s in self.solids] + [f[4] for f in self.frames]
        return list(dict.fromkeys(str(x) for x in seen))

    def write_notes(self, facts):
        """Replace this figure's block under Figure notes; the rest of facts.md is left untouched."""
        facts = Path(facts)
        s = facts.read_text(encoding='utf-8')
        start, end = f'<!-- figure:{self.title}:start -->', f'<!-- figure:{self.title}:end -->'
        rows = [f'- {p}: {w}' for p, w in self.notes] or ['- No schematic parts declared.']
        block = '\n'.join([start, f'### {self.title}', '', 'Schematic parts, to state in the caption:', '', *rows, end])
        pat = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
        if pat.search(s):
            s = pat.sub(lambda _: block, s)
        else:
            if not re.search(r'^## Figure notes\s*$', s, re.M):
                s = s.rstrip() + '\n\n## Figure notes\n'
            s = s.rstrip() + '\n\n' + block + '\n'
        facts.write_text(s, encoding='utf-8')

    # ---------------------------------------------------------------- primitives
    def rect(self, x, y, w, h, fill='white', stroke=INK, r=0, dash=None, sw=2):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def path(self, d, stroke=INK, sw=2.2, dash=None, fill='none', join='round'):
        da = f' stroke-dasharray="{dash}"' if dash else ''
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"{da}/>')

    def shadow(self, x, y, w, h, r=0, off=3):
        """Layered translucent rects: identical in browsers and CairoSVG, which has no blur filter."""
        for k, o in zip((.05, .05, .06, .08), (off + 3, off + 2, off + 1, off)):
            self.add(f'<rect x="{x + o:.2f}" y="{y + o:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="#000" fill-opacity="{k}"/>')

    # ---------------------------------------------------------------- text
    def label(self, x, y, s, size=None, fill=INK, anchor='middle', bold=False, italic=False, rotate=None, check=True):
        """y is the vertical centre of the line, so labels align with the boxes beside them."""
        size = size or self.base
        attrs = f'font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
        # Comic Neue is lighter than the corpus's handwriting font, so regular text gets a hairline too.
        attrs += f' stroke="{fill}" stroke-width="{size * (.04 if bold else .024):.2f}" stroke-linejoin="round"'
        base = y + size * .33
        tr = ''
        if rotate is not None:
            tr = f' transform="rotate({rotate} {x} {y})"'
        elif italic:
            tr = f' transform="translate({x} {base}) skewX(-12) translate({-x} {-base})"'
        self.add(f'<text x="{x:.2f}" y="{base:.2f}"{tr} {attrs}>{_esc(s)}</text>')
        tw = text_width(s, size)
        if rotate in (90, -90, 270):
            self.texts.append((x - size * .55, y - tw / 2, x + size * .55, y + tw / 2, s))
        else:
            left = x if anchor == 'start' else x - tw / 2 if anchor == 'middle' else x - tw
            self.texts.append((left, y - size * .5, left + tw, y + size * .5, s))
        if check and len(str(s).split()) > 6:
            self.warned.append(f'long label ({len(str(s).split())} words): {s!r}')
        return tw

    def lines_of(self, x, y, lines, size=None, fill=INK, **kw):
        size = size or self.base
        for i, l in enumerate(lines):
            self.label(x, y + (i - (len(lines) - 1) / 2) * size * 1.2, l, size, fill, **kw)

    def rich(self, x, y, segs, size=None, anchor='middle', italic=True):
        """One line of (text, colour) segments, for prompts with highlighted words."""
        size = size or self.base
        segs = [(s, INK) if isinstance(s, str) else s for s in segs]
        total = sum(text_width(s, size) for s, _ in segs) + size * .28 * (len(segs) - 1)
        cur = x - total / 2 if anchor == 'middle' else x - total if anchor == 'end' else x
        for s, c in segs:
            self.label(cur, y, s, size, c, 'start', italic=italic, check=False)
            cur += text_width(s, size) + size * .28

    def math(self, x, y, formula, size=None, fill=INK, anchor='middle'):
        """Mathtext drawn as paths, so it needs no math font in the viewer."""
        import matplotlib
        matplotlib.use('Agg')
        matplotlib.rcParams['mathtext.fontset'] = 'stix'
        from matplotlib.font_manager import FontProperties
        from matplotlib.textpath import TextPath
        size = size or self.base * 1.1
        tp = TextPath((0, 0), formula, size=size, prop=FontProperties(family='STIXGeneral'))
        b = tp.get_extents()
        off = -b.x0 if anchor == 'start' else -(b.x0 + b.width / 2) if anchor == 'middle' else -b.x1
        cmds = []
        for v, code in tp.iter_segments(curves=True, simplify=False):
            if code == 1: cmds.append('M%g %g' % tuple(v))
            elif code == 2: cmds.append('L%g %g' % tuple(v))
            elif code == 3: cmds.append('Q%g %g %g %g' % tuple(v))
            elif code == 4: cmds.append('C%g %g %g %g %g %g' % tuple(v))
            elif code == 79: cmds.append('Z')
        base = y + size * .3
        self.add(f'<g transform="translate({x} {base}) scale(1 -1) translate({off} 0)"><path d="{" ".join(cmds)}" fill="{fill}"/></g>')
        left = x if anchor == 'start' else x - b.width / 2 if anchor == 'middle' else x - b.width
        self.texts.append((left, base - b.y1, left + b.width, base - b.y0, formula))

    # ---------------------------------------------------------------- icons
    def fire(self, x, y, s=26):
        """Trainable. (x, y) is the centre."""
        self.states_used.add('fire')
        k = s / 24
        self.add(f'<g transform="translate({x - 12 * k:.2f} {y - 13 * k:.2f}) scale({k:.3f})">'
                 '<path d="M12 0C13 5 19 8 20.5 13.5C22 20 17.5 26 12 26C6 26 2 21 3 15C3.6 12 5.5 10 6.5 8C7 10 8 11.5 9 12C8.8 8 9.5 3.5 12 0Z" fill="#e8481c" stroke="#b92c10" stroke-width=".6"/>'
                 '<path d="M12.3 10C13 13 16.5 15 16.5 19C16.5 22.5 14.5 24.8 12 24.8C9.4 24.8 7.5 22.6 7.8 19.6C8 17.6 9.3 16.6 9.8 15C10.5 16 11 16.5 11.5 16.6C11.3 14.5 11.3 12 12.3 10Z" fill="#ffb31a"/>'
                 '<path d="M12 17.5C12.6 19.2 14.2 20 14.2 21.8C14.2 23.4 13.2 24.6 12 24.6C10.8 24.6 9.8 23.5 9.9 22C10 20.3 11.5 19.5 12 17.5Z" fill="#fff0a8"/></g>')

    def snow(self, x, y, s=26):
        """Frozen. (x, y) is the centre."""
        self.states_used.add('snow')
        r = s / 2
        d = ''
        for a in range(0, 360, 60):
            c, n = math.cos(math.radians(a)), math.sin(math.radians(a))
            d += f'M{x:.2f} {y:.2f}L{x + c * r:.2f} {y + n * r:.2f}'
            px, py = x + c * r * .62, y + n * r * .62
            for t in (-1, 1):
                ang = math.radians(a + t * 50)
                d += f'M{px:.2f} {py:.2f}L{px + math.cos(ang) * r * .34:.2f} {py + math.sin(ang) * r * .34:.2f}'
        self.path(d, 'white', s * .2)
        self.path(d, '#57b5e8', s * .085)

    def dice(self, x, y, s=44):
        """Random sampling."""
        k = s / 44
        g = f'<g transform="translate({x - 22 * k:.2f} {y - 22 * k:.2f}) scale({k:.3f})" stroke="{INK}" stroke-width="2" stroke-linejoin="round">'
        g += '<path d="M22 3L41 13L41 33L22 42L3 33L3 13Z" fill="white"/><path d="M3 13L22 23L41 13M22 23L22 42" fill="none"/>'
        g += '</g>'
        self.add(g)
        for u, v in [(22, 13), (13, 13), (31, 13), (10, 24), (16, 32), (34, 25), (28, 30)]:
            self.add(f'<circle cx="{x + (u - 22) * k:.2f}" cy="{y + (v - 22) * k:.2f}" r="{2.1 * k:.2f}" fill="{INK}"/>')
        self.solids.append((x - 22 * k, y - 22 * k, x + 22 * k, y + 22 * k, 'dice'))

    def robot(self, x, y, s=44):
        """A pretrained tool such as SAM or a depth estimator."""
        k = s / 44
        g = f'<g transform="translate({x - 22 * k:.2f} {y - 22 * k:.2f}) scale({k:.3f})" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round">'
        g += '<path d="M12 8C15 2 29 2 32 8" fill="none" stroke="#3aa0d8" stroke-width="2.4"/><circle cx="22" cy="4" r="2" fill="#e8481c"/>'
        g += '<rect x="3" y="17" width="5" height="11" rx="2" fill="#e8481c"/><rect x="36" y="17" width="5" height="11" rx="2" fill="#3aa0d8"/>'
        g += '<rect x="8" y="9" width="28" height="29" rx="8" fill="#d9d4c7"/><circle cx="16" cy="20" r="4.6" fill="#555"/><circle cx="28" cy="20" r="4.6" fill="#555"/>'
        g += '<rect x="13" y="29" width="18" height="6" rx="1.5" fill="#f4efe2"/><path d="M17 29V35M22 29V35M27 29V35" fill="none" stroke-width="1"/></g>'
        self.add(g)
        self.solids.append((x - 22 * k, y - 22 * k, x + 22 * k, y + 22 * k, 'robot'))

    def state_icon(self, state, x, y, s=26):
        if state == 'fire':
            self.fire(x, y, s)
        elif state == 'snow':
            self.snow(x, y, s)

    # ---------------------------------------------------------------- images
    def _embed(self, im, x, y, w, h):
        px = max(int(round(w * 3)), 32)
        buf = io.BytesIO()
        im.resize((px, int(px * h / w)), Image.LANCZOS).save(buf, format='JPEG', quality=88)
        uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
        self.add(f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" preserveAspectRatio="none" xlink:href="{uri}"/>')

    def image(self, im, x, y, w, h=None, border='white', sw=1.5, shadow=True, name='image'):
        h = h or w
        if shadow:
            self.shadow(x, y, w, h)
        self._embed(im, x, y, w, h)
        if border:
            self.rect(x, y, w, h, 'none', border, sw=sw)
        self.images.append((x, y, x + w, y + h, name))
        self.solids.append((x, y, x + w, y + h, name))
        return Box(x, y, w, h, name)

    def stack(self, im, x, y, w, h=None, n=3, dx=14, dy=-12, back=None, pick=False, border='white', name='stack'):
        """A video: back cards stay plain so each stack embeds one image. (x, y) is the front card."""
        h = h or w
        for k in reversed(range(1, n)):
            bx, by = x + k * dx, y + k * dy
            self.shadow(bx, by, w, h)
            if back is not None:
                self._embed(back, bx, by, w, h)
                self.rect(bx, by, w, h, 'none', 'white', sw=1.5)
            else:
                self.rect(bx, by, w, h, '#efefef', INK, sw=1.2)
        b = self.image(im, x, y, w, h, PICK if pick else border, 3 if pick else 1.5, name=name)
        all_ = Box(x, y + (n - 1) * dy, w + (n - 1) * dx, h - (n - 1) * dy, name)
        self.solids.append((all_.x, all_.y, all_.x + all_.w, all_.y + all_.h, name))
        return all_

    def noise(self, x, y, w, h=None, n=3, dx=12, dy=-11, seed=7, name='noise'):
        im = noise_image(128, seed)
        return self.stack(im, x, y, w, h, n, dx, dy, back=im if n > 1 else None, name=name)

    def slab(self, x, y, w=46, h=110, depth=20, name='latent'):
        """A latent drawn as a tilted grey block."""
        self.add(f'<path d="M{x} {y + depth}L{x + depth} {y}H{x + depth + w}V{y + h}L{x + w} {y + h + depth}H{x}Z" fill="#d0d0d0" stroke="#b5b5b5" stroke-width="1"/>')
        self.add(f'<path d="M{x} {y + depth}H{x + w}V{y + h + depth}H{x}Z" fill="#bcbcbc"/>')
        self.add(f'<path d="M{x + w} {y + depth}L{x + w + depth} {y}V{y + h}L{x + w} {y + h + depth}Z" fill="#a6a6a6"/>')
        b = Box(x, y, w + depth, h + depth, name)
        self.solids.append((b.x, b.y, b.x + b.w, b.y + b.h, name))
        return b

    # ---------------------------------------------------------------- modules
    def block(self, x, y, w, h, text=None, colors=ENCODER, r=14, dash=None, sw=2.4, size=None, state=None, shadow=False, rotate=None, name=None):
        name = name or (' '.join(text) if isinstance(text, (list, tuple)) else text) or 'block'
        if shadow:
            self.shadow(x, y, w, h, r)
        self.rect(x, y, w, h, colors[0], colors[1], r, dash, sw)
        if text:
            ls = [text] if isinstance(text, str) else list(text)
            if rotate is not None:
                self.label(x + w / 2, y + h / 2, ls[0], size, rotate=rotate)
            else:
                self.lines_of(x + w / 2, y + h / 2, ls, size)
        self.solids.append((x, y, x + w, y + h, name))
        if state:
            self.state_icon(state, x + 2, y + 2)
        return Box(x, y, w, h, name)

    def trapezoid(self, x, y, w, h, text=None, narrow='right', colors=ENCODER, inset=.22, size=None, state=None, rotate=None, name=None):
        """Encoder: narrow='right'. Decoder: narrow='left'. Also 'top' and 'bottom'."""
        name = name or (' '.join(text) if isinstance(text, (list, tuple)) else text) or 'trapezoid'
        ix, iy = w * inset, h * inset
        pts = {
            'right': [(x, y), (x + w, y + iy), (x + w, y + h - iy), (x, y + h)],
            'left': [(x, y + iy), (x + w, y), (x + w, y + h), (x, y + h - iy)],
            'bottom': [(x, y), (x + w, y), (x + w - ix, y + h), (x + ix, y + h)],
            'top': [(x + ix, y), (x + w - ix, y), (x + w, y + h), (x, y + h)],
        }[narrow]
        d = 'M' + ' L'.join(f'{a:.2f} {b:.2f}' for a, b in pts) + ' Z'
        self.path(d, colors[1], 2.8, fill=colors[0])
        if text:
            ls = [text] if isinstance(text, str) else list(text)
            if rotate is not None:
                self.label(x + w / 2, y + h / 2, ls[0], size, rotate=rotate)
            else:
                self.lines_of(x + w / 2, y + h / 2, ls, size)
        # The slanted sides are valid arrow targets, so only the inner rectangle counts as solid.
        sx, sy = (ix, 0) if narrow in ('top', 'bottom') else (0, iy)
        self.solids.append((x + sx, y + sy, x + w - sx, y + h - sy, name))
        if state:
            self.state_icon(state, x + 6, y + 6)
        return Box(x, y, w, h, name)

    def bar(self, x, cy, w, h, kind='spatial'):
        """One layer of a network, drawn tall. Kinds carry fixed colours across the figure."""
        self.kinds_used.add(kind)
        if kind == 'spatial':
            self.rect(x, cy - h / 2, w, h, SPATIAL[0], SPATIAL[1], 0, None, 3)
        elif kind == 'cross':
            self.rect(x, cy - h / 2, w, h, CROSS[0], CROSS[1], min(w, h) * .42, None, 3)
        elif kind == 'temporal':
            self.rect(x, cy - h / 2, w, h, TEMPORAL[0], TEMPORAL[1], min(w, h) * .42, '6 4', 2.6)
        else:
            raise ValueError(kind)
        return Box(x, cy - h / 2, w, h, kind)

    def unet(self, x, y, w, h, title=None, kinds=('spatial', 'cross', 'temporal'), colors=C_NET, heights=(.72, .36, .72),
             state=None, title_pos='top', bar_w=None, gap=None, dash='9 6', dots=True):
        """A sub-network in a dashed pastel container, with bars rising at each end. Returns (box, level columns)."""
        self.rect(x, y, w, h, colors[0], colors[1], min(46, h * .18), dash, 2.8)
        box = Box(x, y, w, h, title or 'net')
        self.frames.append((x, y, x + w, y + h, box.name))
        n = len(kinds)
        bar_w = bar_w or max(16, min(26, w * .045))
        gap = gap if gap is not None else bar_w * .1
        group = n * bar_w + (n - 1) * gap
        pad = (w - group * len(heights)) / (len(heights) * 2 + 2)
        pad = max(pad, 10)
        title_h = self.base * 1.35 if title else 0
        cy = y + h / 2 + (title_h / 2 if title_pos == 'top' else -title_h / 2)
        columns = []
        spacing = (w - 2 * pad - group) / max(1, len(heights) - 1)
        for i, hk in enumerate(heights):
            gx = x + pad + i * spacing
            bh = (h - title_h - 18) * hk
            columns.append([self.bar(gx + j * (bar_w + gap), cy, bar_w, bh, kinds[j]) for j in range(n)])
            if dots and i < len(heights) - 1:
                self.ellipsis(gx + group + spacing / 2 - group / 2, cy)
        if title:
            ty = y + self.base * .85 if title_pos == 'top' else y + h - self.base * .85
            tw = self.label(x + w / 2, ty, title)
            if state:
                self.state_icon(state, x + w / 2 + tw / 2 + 16, ty)
        elif state:
            self.state_icon(state, x + 6, y + 6)
        return box, columns

    def ellipsis(self, x, y, r=2.2):
        for d in (-7, 0, 7):
            self.add(f'<circle cx="{x + d:.2f}" cy="{y:.2f}" r="{r}" fill="{INK}"/>')

    def op(self, x, y, kind='+', r=15):
        """Plus, times or concat node."""
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="white" stroke="{INK}" stroke-width="2.4"/>')
        k = r * .95
        if kind == '+':
            self.path(f'M{x - k} {y}H{x + k}M{x} {y - k}V{y + k}', INK, 2.4)
        elif kind == 'x':
            q = k * .7
            self.path(f'M{x - q} {y - q}L{x + q} {y + q}M{x + q} {y - q}L{x - q} {y + q}', INK, 2.4)
        b = Box(x - r, y - r, 2 * r, 2 * r, 'op')
        self.solids.append((b.x, b.y, b.x + b.w, b.y + b.h, 'op'))
        return b

    # ---------------------------------------------------------------- grouping
    def container(self, x, y, w, h, colors=C_BLUE, title=None, r=26, dash='9 6', sw=2.6, title_size=None):
        self.rect(x, y, w, h, colors[0], colors[1], r, dash, sw)
        self.frames.append((x, y, x + w, y + h, title or 'container'))
        if title:
            self.label(x + w / 2, y + (title_size or self.base) * .95, title, title_size)
        return Box(x, y, w, h, title or 'container')

    def stage_title(self, x, y, s, size=None, fill='#5b5b5b', anchor='start'):
        """Bold italic grey heading for a stage."""
        self.label(x, y, s, size or self.base * 1.3, fill, anchor, bold=True, italic=True)

    def phase(self, x, y, s, size=None):
        """Rotated Training / Inference label on the far left."""
        self.label(x, y, s, size or self.base * 1.2, INK, rotate=-90, bold=True)

    def divider(self, x, y0, y1, dash='9 8', color='#7f7f7f', sw=2.4):
        self.path(f'M{x} {y0}V{y1}', color, sw, dash)

    def zoom(self, src, dst, color='#7f7f7f', dash='7 6', sw=1.8):
        """Two dashed lines from a small part to its enlarged panel. Exempt from the line lint."""
        for a, b in ((src.at('left', 0) if dst.x < src.x else src.at('right', 0), dst.at('top', 0)),
                     (src.at('left', 1) if dst.x < src.x else src.at('right', 1), dst.at('top', 1))):
            self.path(f'M{a[0]} {a[1]}L{b[0]} {b[1]}', color, sw, dash)

    def legend(self, x, y, items, columns=None, box=True, gap_y=None, size=None, w=None):
        """items are ('spatial'|'cross'|'temporal'|'fire'|'snow'|('arrow',color,style), text).

        columns=None gives a vertical dotted box; columns=n gives a strip of n per row.
        """
        size = size or self.base * .92
        gap_y = gap_y or size * 1.8
        columns = columns or 1
        widths = [52 + text_width(t, size) + 28 for _, t in items]
        cols = [max(widths[c::columns]) for c in range(columns)]
        rows = math.ceil(len(items) / columns)
        W = w or sum(cols) + 16
        H = rows * gap_y + 14
        if box:
            self.rect(x, y, W, H, 'white', INK, 12, '2.5 5', 2)
        for i, (kind, t) in enumerate(items):
            cx = x + 26 + sum(cols[:i % columns])
            cy = y + 7 + gap_y * (i // columns + .5)
            if kind in ('fire', 'snow'):
                self.states_in_legend.add(kind)
                self.state_icon(kind, cx, cy, 24)
            elif kind in ('spatial', 'cross', 'temporal'):
                self.kinds_in_legend.add(kind)
                self.bar(cx - 12, cy, 24, 24, kind)
            elif isinstance(kind, tuple) and kind[0] == 'arrow':
                self._line([(cx - 16, cy), (cx + 18, cy)], kind[1], LINE_STYLES[kind[2]], 2.4, True)
            self.label(cx + 26, cy, t, size, anchor='start')
        return Box(x, y, W, H, 'legend')

    # ---------------------------------------------------------------- connections
    def _head(self, x, y, a, color, s=12):
        c, n = math.cos(a), math.sin(a)
        pts = [(x, y), (x - s * c + s * .42 * n, y - s * n - s * .42 * c), (x - s * .78 * c, y - s * .78 * n), (x - s * c - s * .42 * n, y - s * n + s * .42 * c)]
        self.add(f'<path d="M{" L".join(f"{p:.2f} {q:.2f}" for p, q in pts)} Z" fill="{color}"/>')

    def _line(self, pts, color, dash, sw, tip):
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        a = math.atan2(y1 - y0, x1 - x0)
        end = (x1 - 8 * math.cos(a), y1 - 8 * math.sin(a)) if tip else (x1, y1)
        d = 'M' + ' L'.join(f'{p:.2f} {q:.2f}' for p, q in list(pts[:-1]) + [end])
        self.path(d, color, sw, dash)
        if tip:
            self._head(x1, y1, a, color)

    def arrow(self, a, b, route='auto', color=INK, style='solid', sw=3, tip=True, gap=7, mid=None, lint=True, name='arrow'):
        """Connect two points with square elbows. route: h, v, hv, vh, hvh, vhv.

        gap pulls both ends away from the boxes they join; mid sets the elbow position of hvh and vhv.
        """
        (x0, y0), (x1, y1) = a, b
        if route == 'auto':
            route = 'h' if abs(y0 - y1) < 1 else 'v' if abs(x0 - x1) < 1 else 'hvh'
        if route in ('h', 'v'):
            pts = [(x0, y0), (x1, y1)]
        elif route == 'hv':
            pts = [(x0, y0), (x1, y0), (x1, y1)]
        elif route == 'vh':
            pts = [(x0, y0), (x0, y1), (x1, y1)]
        elif route == 'hvh':
            m = mid if mid is not None else (x0 + x1) / 2
            pts = [(x0, y0), (m, y0), (m, y1), (x1, y1)]
        elif route == 'vhv':
            m = mid if mid is not None else (y0 + y1) / 2
            pts = [(x0, y0), (x0, m), (x1, m), (x1, y1)]
        else:
            raise ValueError(route)
        pts = _trim(pts, gap)
        self._line(pts, color, LINE_STYLES[style], sw, tip)
        if lint:
            self.lines.append((pts, name))

    def curve(self, a, b, bend=60, color=INK, style='solid', sw=2.6, tip=True, name='curve'):
        """A curved arrow for reuse, loss and feedback paths. Exempt from the line lint."""
        (x0, y0), (x1, y1) = a, b
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / ln * bend, my + dx / ln * bend
        ang = math.atan2(y1 - cy, x1 - cx)
        ex, ey = x1 - 8 * math.cos(ang), y1 - 8 * math.sin(ang)
        self.path(f'M{x0:.2f} {y0:.2f} Q{cx:.2f} {cy:.2f} {ex:.2f} {ey:.2f}', color, sw, LINE_STYLES[style])
        if tip:
            self._head(x1, y1, ang, color)

    # ---------------------------------------------------------------- lint
    def lint(self, min_pt=7):
        issues = list(self.warned)
        for t in self.texts:
            if t[0] < 0 or t[1] < 0 or t[2] > self.W or t[3] > self.H:
                issues.append(f'off canvas: {t[4]!r}')
        for i, a in enumerate(self.texts):
            for b in self.texts[i + 1:]:
                if a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 2 and b[1] < a[3] - 2:
                    issues.append(f'text overlap: {a[4]!r} / {b[4]!r}')
        for t in self.texts:
            for fr in self.frames:
                inter = t[0] < fr[2] and fr[0] < t[2] and t[1] < fr[3] and fr[1] < t[3]
                inside = t[0] >= fr[0] and t[2] <= fr[2] and t[1] >= fr[1] and t[3] <= fr[3]
                if inter and not inside:
                    issues.append(f'text straddles the border of {fr[4]!r}: {t[4]!r}')
            for im in self.images:
                if t[0] < im[2] - 1 and im[0] < t[2] - 1 and t[1] < im[3] - 1 and im[1] < t[3] - 1:
                    issues.append(f'text over image {im[4]!r}: {t[4]!r}')
        for pts, name in self.lines:
            for p, q in zip(pts, pts[1:]):
                for t in self.texts:
                    if _hits(p, q, t, 2):
                        issues.append(f'line crosses text: {t[4]!r} ({p} -> {q})')
                for s in self.solids:
                    if _hits(p, q, s, -2):
                        issues.append(f'line crosses {s[4]!r} ({p} -> {q})')
        for s in sorted(self.states_used - self.states_in_legend):
            issues.append(f'state icon not in legend: {s}')
        for k in sorted(self.kinds_used - self.kinds_in_legend):
            issues.append(f'layer kind not in legend: {k}')
        pt = self.print_width_in * 72 / self.W
        sizes = [float(p.split('font-size="')[1].split('"')[0]) for p in self.parts if 'font-size="' in p]
        if sizes and min(sizes) * pt < min_pt:
            issues.append(f'smallest text prints at {min(sizes) * pt:.1f} pt (< {min_pt})')
        if self.images:
            big = max(i[2] - i[0] for i in self.images) / self.W
            if big < .08:
                issues.append(f'largest image is {big:.0%} of the width; the corpus range is 8-15%')
        # A vector-only method can be valid. Presence of image panels does not
        # establish that they are real results; provenance is a semantic check.
        return issues

    # ---------------------------------------------------------------- export
    def svg(self):
        font = base64.b64encode(FONT.read_bytes()).decode()
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}" role="img">'
                f'<title>{_esc(self.title)}</title>'
                f'<defs><style>@font-face{{font-family:"Comic Neue";src:url(data:font/ttf;base64,{font})}}text{{font-family:"Comic Neue",sans-serif}}</style></defs>'
                + ''.join(self.parts) + '</svg>')

    def save(self, out, strict=False, facts=None):
        """Writes index.html, framework.svg, framework.pdf, preview.png and labels.json. Prints the lint result.

        facts is the path of the project's facts.md, which receives the schematic list.
        """
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'labels.json').write_text(json.dumps({'title': self.title, 'labels': self.labels(), 'schematic': self.notes}, ensure_ascii=False, indent=1), encoding='utf-8')
        if facts:
            self.write_notes(facts)
        svg = self.svg()
        (out / 'framework.svg').write_text(svg, encoding='utf-8')
        (out / 'index.html').write_text(
            f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{_esc(self.title)}</title>'
            f'<style>html,body{{margin:0;background:white}}main{{max-width:{self.W}px;margin:24px auto}}svg{{display:block;width:100%;height:auto}}@media print{{@page{{size:{self.print_width_in}in {self.print_width_in * self.H / self.W}in;margin:0}}main{{margin:0;max-width:none}}}}</style><main>{svg}</main></html>', encoding='utf-8')
        # CairoSVG does not consistently honor embedded @font-face. Export
        # bundled glyph outlines instead of changing process-wide Fontconfig.
        static_svg = _outline_text(svg)
        (out / 'framework-outlined.svg').write_text(static_svg, encoding='utf-8')
        import cairosvg
        cairosvg.svg2png(bytestring=static_svg.encode(), write_to=str(out / 'preview.png'), output_width=self.W * 3 // 2, output_height=self.H * 3 // 2)
        # CairoSVG interprets output pixels at 96 dpi. Respect the same physical
        # width used by the print-size lint.
        width_px = self.print_width_in * 96
        cairosvg.svg2pdf(bytestring=static_svg.encode(), write_to=str(out / 'framework.pdf'), output_width=width_px, output_height=width_px * self.H / self.W)
        issues = self.lint()
        print('lint:', 'clean' if not issues else f'{len(issues)} issue(s)')
        for i in issues:
            print('  -', i)
        if strict and issues:
            raise SystemExit(1)
        return issues


def _trim(pts, gap):
    """Pull the start of a polyline away from its source box; the tip keeps the same gap."""
    pts = [tuple(p) for p in pts]
    if gap:
        for i, j in ((0, 1), (-1, -2)):
            (x0, y0), (x1, y1) = pts[i], pts[j]
            d = math.hypot(x1 - x0, y1 - y0) or 1
            g = min(gap, d / 3)
            pts[i] = (x0 + (x1 - x0) / d * g, y0 + (y1 - y0) / d * g)
    return pts


def _hits(p, q, r, pad):
    """Does segment pq enter rectangle r (x0, y0, x1, y1, ...) grown by pad?"""
    x0, y0, x1, y1 = r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for d, a, lo, hi in ((dx, p[0], x0, x1), (dy, p[1], y0, y1)):
        if abs(d) < 1e-9:
            if a <= lo or a >= hi:
                return False
        else:
            u, v = (lo - a) / d, (hi - a) / d
            t0, t1 = max(t0, min(u, v)), min(t1, max(u, v))
            if t0 >= t1:
                return False
    return True
