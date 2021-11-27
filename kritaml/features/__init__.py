from .denoise.process import apply_denoise
from .dehaze.process import apply_dehaze
from .monodepth.process import apply_monodepth
__all__ = ["apply_denoise", "apply_dehaze", "apply_monodepth"]