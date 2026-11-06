"""A small runnable example. The image is generated, so replace it with your own results."""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
from figkit import *


def scene(size=256):
    """A simple landscape: sky, a sun and hills."""
    im = Image.new('RGB', (size, size))
    px = im.load()
    for y in range(size):
        for x in range(size):
            hill = size * (.62 + .1 * math.sin(x / size * 7))
            if (x - size * .72) ** 2 + (y - size * .26) ** 2 < (size * .1) ** 2:
                px[x, y] = (250, 214, 90)
            elif y > hill:
                px[x, y] = (70, 135 + y * 60 // size, 80)
            else:
                px[x, y] = (110 + y * 90 // size, 170 + y * 50 // size, 235)
    return im


def build(output_dir):
    a = scene()
    f = Figure(1600, 560, 'Example framework', base=25)
    vid = f.stack(a, 40, 150, 210, 190, name='input')
    f.label(145, 372, 'Input video', 27)
    vae = f.trapezoid(320, 110, 84, 250, '3D VAE', 'right', state='snow', rotate=90, inset=.14)
    f.arrow((vid.x + vid.w, vae.cy), vae.left)
    f.rich(535, 62, [('a sunny', INK)], 24)
    f.rich(535, 92, [('valley', PROMPT), 'at noon'], 24)
    lat = f.stack(noised(a, .5), 460, 180, 130, 120, n=3, dx=12, dy=-11, back=noise_image(128), name='latent')
    f.arrow(vae.right, (lat.x, vae.cy))
    net, _ = f.unet(640, 80, 500, 310, 'Denoising Unet', state='fire', heights=(.74, .42, .74))
    f.arrow((lat.x + lat.w, net.cy), net.left)
    out = f.stack(a, 1210, 150, 250, 190, dx=16, dy=-14, pick=True, back=a, name='output')
    f.arrow(net.right, (out.x, net.cy))
    f.label(1335, 372, 'Output video', 27)
    f.legend(330, 440, [('spatial', 'Spatial-Attn'), ('cross', 'Cross-Attn'), ('temporal', 'New Module'), ('fire', 'Trainable'), ('snow', 'Frozen')], columns=5, size=24, gap_y=60)
    f.schematic('All images', 'generated placeholders, not results')
    return f.save(output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.output)
