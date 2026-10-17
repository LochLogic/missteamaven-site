"""Resize the photos and logos pulled from the old Wix site into web-sized assets.

Usage: python -I tools/prep_images.py <original-images-dir> <output-dir>
"""
import glob
import os
import sys

from PIL import Image, ImageOps

SRC, OUT = sys.argv[1], sys.argv[2]

# name: (wix id fragment, max width, optional crop aspect w/h)
PHOTOS = {
    "hero-world-cup": ("5db8529090884d19", 2000, None),
    "portrait": ("325939f3282d433b", 1000, 4 / 5),
    "england-bench": ("5deef36a0d414d28", 800, None),
    "jump": ("7e8b1e1160ab4bd4", 1000, 4 / 5),
    "maven-1706-back": ("97eff92cbb0d4c38", 1400, None),
    "maven-1706-red": ("faa0eb53d0164cfe", 1600, None),
    "green-smile": ("e123f08fdc9c4983", 1000, None),
    "gotham-bw": ("09f4db16e98d4ac0", 1200, None),
    "gotham-podium": ("316b9dd3b04e45f0", 1400, None),
    "clinic-group": ("efee27999c1b4938", 1400, None),
    "clinic-group-2": ("55e6cf617f344d83", 1200, None),
    "outdoor-group": ("ee77ac7596354b16", 1400, None),
    "footage-laptop": ("6fb2ca07b8b0437c", 720, None),
    "practice": ("51db06a00b744db0", 1600, None),
    "ny-team": ("8582be9ea7ab4117", 1400, None),
    "yellow-jam": ("85ac8b59a5914305", 1600, None),
    "denver-pack": ("a297d79c2d9842b9", 1000, None),
    "red-star": ("2c2064080aa44f3d", 1400, None),
    "bw-blocking": ("5536b3a711c64a0b", 1400, None),
    "purple-smile": ("98569d3ac1944c6f", 1400, None),
    "ref-umbrella": ("7a860f3516ff4098", 800, None),
    "huddle": ("9da08ee5087e472c", 1200, None),
    "bw-bench": ("efd632661ce24917", 1000, None),
    "gotham-pack": ("7cc79da8d9804c97", 1400, None),
    "blue-jam": ("7cddaf2950b74c8b", 1400, None),
    "gotham-cheers": ("271917aa3948409a", 960, None),
}

# name: (wix id fragment, league/event name)
LOGOS = {
    "gotham": "2c6db9c4f93144ed",
    "gotham-juniors": "28590f36faef452f",
    "denver": "493dea847e3a4a07",
    "ny-all-stars": "f8e206e02fd243da",
    "ny-shock-exchange": "16bb9644f39d4e3d",
    "rollercon": "6194d86affee450b",
    "camp-elite": "52bf4dc0e67f4515",
    "nedc": "ae9e616b2a0b4fcc",
    "nashville": "b9394026ee954dfc",
    "garden-state": "2f432528ab014d91",
    "new-jersey": "991952011a60467a",
    "dirty-jersey": "771106ad3a3f4b67",
    "carolina": "ea57c0b5a3a74ce4",
    "tampa": "e0dce8f53a5647f2",
    "jacksonville": "08b0db156e414699",
    "molly-roger": "ea57c5e93dd04e20",
    "rage-city": "165b1045c9054919",
    "boom-town": "4de7748686234ae1",
    "united-we-roll": "5e57859202854171",
    "saskatoon": "dcb833a3b3ab413d",
    "canada-juniors": "91413893a69740bf",
    "beijing": "089551f8643449f7",
    "ark-valley": "62575a0392024ef9",
    "jackson-hole": "6cffbf9affbf4bf7",
}


def find(fragment):
    hits = glob.glob(os.path.join(SRC, f"*{fragment}*"))
    if not hits:
        raise SystemExit(f"missing source for {fragment}")
    return hits[0]


def crop_to(im, aspect):
    w, h = im.size
    if w / h > aspect:
        nw = int(h * aspect)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / aspect)
    y = max(0, int((h - nh) * 0.25))  # bias toward the top so heads stay in frame
    return im.crop((0, y, w, y + nh))


os.makedirs(os.path.join(OUT, "logos"), exist_ok=True)

for name, (frag, width, aspect) in PHOTOS.items():
    im = ImageOps.exif_transpose(Image.open(find(frag))).convert("RGB")
    if aspect:
        im = crop_to(im, aspect)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, f"{name}.webp"), "WEBP", quality=78, method=6)
    print(f"{name:18s} {im.width}x{im.height}")

for name, frag in LOGOS.items():
    im = Image.open(find(frag)).convert("RGBA")
    # trim built-in padding (white or transparent) so every logo fills its tile
    flat = Image.new("RGBA", im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)
    mask = ImageOps.invert(flat.convert("L")).point(lambda v: 255 if v > 40 else 0)
    if mask.getbbox():
        im = im.crop(mask.getbbox())
    # pad onto a square white tile so the wall reads as one grid
    scale = 340 / max(im.size)  # upscale small sources too, so every mark reads at the same size
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    tile = Image.new("RGBA", (400, 400), (255, 255, 255, 255))
    tile.alpha_composite(im, ((400 - im.width) // 2, (400 - im.height) // 2))
    tile.convert("RGB").save(os.path.join(OUT, "logos", f"{name}.webp"), "WEBP", quality=82)

# favicon / social mark from the existing star logo
star = Image.open(find("f06f62e75599410988e9")).convert("RGBA")
star.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "icon-192.png"))
star.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT, "favicon-32.png"))
print("logos + icons done")
