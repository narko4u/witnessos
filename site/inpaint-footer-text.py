"""Remove the baked-in footer link text from the Empire Labs banner.

The banner artwork carries its own link row inside a chevron frame. The site needs
real anchors there, so the labels are painted out and replaced by a live HTML row
positioned inside the same frame. Only the small text glyphs are touched: the frame
lines, the globe and the city lights stay as they are.

Method without OpenCV: mask the glyphs, then repeatedly copy a blurred copy of the
image back into the masked pixels. The surroundings are dark and smooth, so a few
dozen passes converge to a clean plate with no visible scar.
"""
import sys

import numpy as np
from PIL import Image, ImageFilter

SRC = "/home/vault/.hermes/cache/images/img_60c7d45e7018.jpg"
OUT = "/home/vault/work/witnessos-site-clone/publish-v2/assets/empire-footer.webp"
DEBUG = "/tmp/footer-inpaint-mask.png"

# The frame: top rail near y=342, bottom rail near y=402, inner text between them.
TEXT_TOP, TEXT_BOTTOM = 347, 396
TEXT_LEFT, TEXT_RIGHT = 40, 1252
LUM_THRESHOLD = 44


def main() -> int:
    im = Image.open(SRC).convert("RGB")
    a = np.array(im).astype(np.float32)
    lum = a.mean(axis=2)

    mask = np.zeros(lum.shape, dtype=bool)
    band = np.zeros(lum.shape, dtype=bool)
    band[TEXT_TOP:TEXT_BOTTOM, TEXT_LEFT:TEXT_RIGHT] = True
    mask |= band & (lum > LUM_THRESHOLD)

    # Grow the mask so antialiased glyph edges go too.
    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(5))
    mask = np.array(m) > 127
    print(f"masked pixels: {mask.sum()} ({mask.sum() / mask.size:.3%} of the plate)")

    work = a.copy()
    for i in range(60):
        blurred = np.array(
            Image.fromarray(work.clip(0, 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(radius=6)
            )
        ).astype(np.float32)
        work[mask] = blurred[mask]
    print("fill converged")

    out = Image.fromarray(work.clip(0, 255).astype(np.uint8))
    out.save(OUT, "WEBP", quality=90, method=6)

    # Debug: the mask over the original, so the region can be checked by eye.
    dbg = np.array(im).copy()
    dbg[mask] = [255, 0, 128]
    Image.fromarray(dbg).crop((0, 320, 1280, 455)).resize((1280, 270), Image.LANCZOS).save(DEBUG)
    print(f"wrote {OUT} {out.size}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
