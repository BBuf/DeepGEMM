"""Release-only backport of the unclamped FP8 output floor from PR #111.

Other epilogue classes and value clamping are intentionally unsupported.
"""
import math
import struct

class FP8CastWithClamp:
    def __init__(self, sfd, clamp_value=None, clamped_count=None, amax_eps=1e-4):
        if clamp_value is not None or clamped_count is not None:
            raise NotImplementedError("Release backport supports only unclamped output")
        value = struct.unpack("f", struct.pack("f", float(amax_eps)))[0]
        if not math.isfinite(value) or value <= 0:
            raise ValueError("amax_eps must be finite and positive")
        exponent = math.ceil(math.log2(value / 448.0)) + 127
        if not 1 <= exponent <= 254:
            raise ValueError("amax_eps cannot be represented by a normal UE8M0 scale")
        self.sfd, self.amax_eps, self.min_sf_exp = sfd, value, exponent
