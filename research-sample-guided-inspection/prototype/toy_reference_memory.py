"""Toy, CPU-only illustration of the proposed reference-memory pipeline.

    python3 prototype/toy_reference_memory.py

IMPORTANT: everything here is SYNTHETIC. The die images are procedurally drawn
cartoons of a die layout, and the "features" are simple multi-scale pixel-patch
descriptors, not a pretrained deep encoder. The script exists to make the
pipeline concrete (enrol -> align -> compare -> anomaly map -> decision) and to
draw the conceptual figures of the dossier. Its outputs are NOT experimental
results and must never be reported as such.

The real prototype replaces `patch_features` with a frozen WRN-50 / DINOv2
encoder and `ReferenceMemory` with a coreset-subsampled FAISS index (see
Section 23 of the dossier).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

SIZE = 192  # die image side length in pixels


# ---------------------------------------------------------------------------
# 1. Synthetic die generator
# ---------------------------------------------------------------------------
def render_die(rng: np.random.Generator, size: int = SIZE, jitter: float = 0.0,
               gain: float = 1.0, offset: float = 0.0, noise: float = 0.02) -> np.ndarray:
    """Draw a stylised die layout in [0, 1].

    The layout is deliberately ASYMMETRIC (orientation mark in one corner,
    pad ring missing on one side), so different rotations are distinguishable,
    just as real dies are.
    """
    s = size
    img = np.full((s, s), 0.30)
    u = s / 192.0

    def box(r0, r1, c0, c1, v):
        img[int(r0 * u):int(r1 * u), int(c0 * u):int(c1 * u)] = v

    # die body and seal ring
    box(6, 186, 6, 186, 0.36)
    img[int(6*u):int(186*u), int(6*u):int(9*u)] = 0.55
    img[int(6*u):int(186*u), int(183*u):int(186*u)] = 0.55
    img[int(6*u):int(9*u), int(6*u):int(186*u)] = 0.55
    img[int(183*u):int(186*u), int(6*u):int(186*u)] = 0.55
    # bond pads on three sides (left side has none -> asymmetry)
    for k in range(9):
        c = 22 + k * 17
        box(12, 22, c, c + 9, 0.78)          # top
        box(170, 180, c, c + 9, 0.78)        # bottom
        box(c, c + 9, 170, 180, 0.78)        # right
    # orientation mark (L shape, top-left)
    box(14, 30, 14, 18, 0.85)
    box(26, 30, 14, 30, 0.85)
    # memory array (regular via grid) — upper-left block
    for r in range(40, 96, 6):
        for c in range(36, 96, 6):
            box(r, r + 3, c, c + 3, 0.70)
    # horizontal metal lines — lower-left block
    for r in range(108, 160, 7):
        box(r, r + 3, 30, 100, 0.66)
    # vertical metal lines — right block
    for c in range(112, 160, 7):
        box(40, 160, c, c + 3, 0.62)
    # logic block (dark rectangle with a contact row)
    box(36, 52, 110, 162, 0.22)
    for c in range(114, 160, 6):
        box(42, 46, c, c + 2, 0.60)

    img = ndimage.gaussian_filter(img, 0.7 * u)          # optical / beam blur
    if jitter:
        dy, dx = rng.normal(0, jitter, 2)
        img = ndimage.shift(img, (dy, dx), order=1, mode="nearest")
    img = gain * img + offset
    img = img + rng.normal(0, noise, img.shape)
    return np.clip(img, 0, 1)


def add_defects(img: np.ndarray, kinds=("particle", "scratch", "bridge"), seed: int = 0):
    """Insert stylised defects. Returns (image, binary ground-truth mask)."""
    rng = np.random.default_rng(seed)
    out = img.copy()
    mask = np.zeros_like(img, dtype=bool)
    s = img.shape[0]
    u = s / 192.0
    yy, xx = np.mgrid[0:s, 0:s]
    if "particle" in kinds:
        cy, cx, r = 70 * u, 140 * u, 4.5 * u
        d = np.hypot(yy - cy, xx - cx)
        blob = np.exp(-(d / r) ** 2)
        out = np.maximum(out, 0.35 + 0.6 * blob)
        mask |= d < 1.3 * r
    if "scratch" in kinds:
        for t in np.linspace(0, 1, 400):
            y = (118 + 30 * t) * u
            x = (40 + 50 * t) * u
            yi, xi = int(round(y)), int(round(x))
            out[yi - 1:yi + 1, xi - 1:xi + 1] = 0.12
            mask[yi - 2:yi + 2, xi - 2:xi + 2] = True
    if "bridge" in kinds:
        r0, r1, c0, c1 = int(115 * u), int(122 * u), int(126 * u), int(130 * u)
        out[r0:r1, c0:c1] = 0.66
        mask[r0 - 1:r1 + 1, c0 - 1:c1 + 1] = True
    if "missing_via" in kinds:
        r0, c0 = int(64 * u), int(60 * u)
        out[r0:r0 + int(3 * u), c0:c0 + int(3 * u)] = 0.37
        mask[r0 - 1:r0 + int(4 * u), c0 - 1:c0 + int(4 * u)] = True
    out = out + rng.normal(0, 0.005, out.shape)
    return np.clip(out, 0, 1), mask


# ---------------------------------------------------------------------------
# 2. "Encoder": multi-scale patch descriptors (stand-in for a CNN / ViT)
# ---------------------------------------------------------------------------
def patch_features(img: np.ndarray, patch: int = 8, stride: int = 4, scales=(0.0, 1.5)):
    """Return (features [N, D], grid shape (H', W')).

    Each feature concatenates the mean-removed pixel patch at several blur
    levels: a crude multi-scale descriptor that, like a CNN feature map, keeps
    the spatial layout of the image.
    """
    feats = []
    for sigma in scales:
        im = ndimage.gaussian_filter(img, sigma) if sigma > 0 else img
        win = np.lib.stride_tricks.sliding_window_view(im, (patch, patch))[::stride, ::stride]
        h, w = win.shape[:2]
        f = win.reshape(h, w, -1)
        f = f - f.mean(axis=-1, keepdims=True) * 0.5   # partly brightness-invariant
        feats.append(f)
    f = np.concatenate(feats, axis=-1)
    return f.reshape(-1, f.shape[-1]), (h, w)


# ---------------------------------------------------------------------------
# 3. Geometric alignment (coarse rotation search + translation)
# ---------------------------------------------------------------------------
def estimate_rotation(reference: np.ndarray, target: np.ndarray, step: float = 1.0) -> float:
    """Brute-force search of the angle that best maps reference onto target.

    Uses normalised cross-correlation of downsampled, blurred images; a
    stand-in for Fourier–Mellin or feature-based registration.
    """
    def prep(a):
        a = ndimage.gaussian_filter(a, 2)[::2, ::2]
        return (a - a.mean()) / (a.std() + 1e-8)
    t = prep(target)
    best, best_angle = -np.inf, 0.0
    for ang in np.arange(0, 360, step):
        r = prep(ndimage.rotate(reference, ang, reshape=False, order=1, mode="nearest"))
        score = float((r * t).mean())
        if score > best:
            best, best_angle = score, float(ang)
    return best_angle


def warp_reference(reference: np.ndarray, angle: float):
    """Rotate the REFERENCE into the target's frame ("warp the reference, not
    the target"), so the target's pixels are never interpolated. Returns the
    warped image and a validity mask (False where the rotated reference has no
    data, i.e. the corners)."""
    warped = ndimage.rotate(reference, angle, reshape=False, order=1, mode="constant", cval=-1)
    valid = warped >= 0
    valid = ndimage.binary_erosion(valid, iterations=6)
    return np.clip(warped, 0, 1), valid


# ---------------------------------------------------------------------------
# 4. Reference memory + anomaly scoring
# ---------------------------------------------------------------------------
class ReferenceMemory:
    """Normal-patch memory with nearest-neighbour scoring."""

    def __init__(self):
        self.bank = None
        self.tree = None

    def enrol(self, reference_images, valid_masks=None, patch=8, stride=4):
        banks = []
        for i, img in enumerate(reference_images):
            f, (h, w) = patch_features(img, patch, stride)
            if valid_masks is not None:
                vm = np.lib.stride_tricks.sliding_window_view(valid_masks[i], (patch, patch))[::stride, ::stride]
                keep = vm.reshape(h * w, -1).all(axis=1)
                f = f[keep]
            banks.append(f)
        self.bank = np.concatenate(banks)
        self.tree = cKDTree(self.bank)
        return self

    def score_map(self, img, patch=8, stride=4):
        f, (h, w) = patch_features(img, patch, stride)
        d, _ = self.tree.query(f, k=1)
        amap = d.reshape(h, w)
        # back to pixel resolution, then light smoothing (as in PatchCore)
        zoom = (img.shape[0] / h, img.shape[1] / w)
        amap = ndimage.zoom(amap, zoom, order=1)[: img.shape[0], : img.shape[1]]
        return ndimage.gaussian_filter(amap, 2)


def calibrate_threshold(memory_images, held_out_normals, q=0.999):
    """Threshold = high quantile of anomaly scores on held-out NORMAL dies."""
    mem = ReferenceMemory().enrol(memory_images)
    vals = np.concatenate([mem.score_map(x).ravel() for x in held_out_normals])
    return float(np.quantile(vals, q))


def demo(seed: int = 7):
    """Run the whole toy pipeline and return a dict of images for plotting."""
    rng = np.random.default_rng(seed)
    refs = [render_die(rng, jitter=0.6) for _ in range(5)]
    held = [render_die(rng, jitter=0.6) for _ in range(3)]
    tau = calibrate_threshold(refs, held)
    mem = ReferenceMemory().enrol(refs)

    target_clean = render_die(rng, jitter=0.6)
    target, gt = add_defects(target_clean)
    amap = mem.score_map(target)
    decision = amap > tau

    # rotated target: naive (no alignment) vs aligned (warp references)
    angle_true = 37.0
    rot_target = np.clip(ndimage.rotate(target, angle_true, reshape=False, order=1, mode="nearest"), 0, 1)
    naive_map = mem.score_map(rot_target)
    angle_est = estimate_rotation(refs[0], rot_target)
    warped = [warp_reference(r, angle_est) for r in refs]
    mem_rot = ReferenceMemory().enrol([w for w, _ in warped], [v for _, v in warped])
    aligned_map = mem_rot.score_map(rot_target)
    valid_t = warp_reference(np.ones_like(target), angle_est)[1]
    aligned_map = np.where(valid_t, aligned_map, 0)
    naive_map_v = np.where(valid_t, naive_map, 0)
    return dict(refs=refs, target=target, gt=gt, amap=amap, tau=tau, decision=decision,
                rot_target=rot_target, naive_map=naive_map_v, aligned_map=aligned_map,
                angle_true=angle_true, angle_est=angle_est, valid=valid_t)


if __name__ == "__main__":
    out = demo()
    inside = out["amap"][out["gt"]].mean()
    outside = out["amap"][~out["gt"]].mean()
    print("TOY SYNTHETIC DEMO — not an experimental result")
    print(f"threshold tau (99.9% quantile of held-out normal pixels): {out['tau']:.3f}")
    print(f"mean anomaly score inside defects: {inside:.3f}, outside: {outside:.3f}")
    print(f"true rotation {out['angle_true']:.0f} deg, estimated {out['angle_est']:.0f} deg")
    fa_naive = (out['naive_map'] > out['tau']).mean()
    fa_aligned = ((out['aligned_map'] > out['tau']) & ~ndimage.rotate(out['gt'].astype(float), out['angle_true'], reshape=False, order=0).astype(bool)).mean()
    print(f"fraction of pixels flagged, rotated target, no alignment: {fa_naive:.3f}")
    print(f"fraction of non-defect pixels flagged, rotated target, aligned references: {fa_aligned:.4f}")
