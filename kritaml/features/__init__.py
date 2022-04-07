from .denoise.process import apply_denoise
from .dehaze.process import apply_dehaze
from .monodepth.process import apply_monodepth
from .recolor.process import apply_recolor
from .super_resolution.process import apply_super_resolution
from .sketch.process import apply_sketch
__all__ = ["apply_denoise", "apply_dehaze", "apply_monodepth", "apply_recolor", "apply_super_resolution","apply_sketch"]
