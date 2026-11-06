"""Non-destructive 16:9 Safe Fit geometry. Never stretch or crop a source."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FitRect:
    x: int
    y: int
    width: int
    height: int


def safe_fit_rect(source_width: int, source_height: int, canvas_width: int = 1920, canvas_height: int = 1080) -> FitRect:
    """Integer destination rectangle centered in the output canvas.

    Preserve entire image; letterbox or pillarbox if necessary.
    """
    if min(source_width, source_height, canvas_width, canvas_height) <= 0:
        raise ValueError("all dimensions must be positive")
    # Cross-multiplication avoids floating point aspect-ratio drift.
    if source_width * canvas_height >= source_height * canvas_width:
        width = canvas_width
        height = max(1, source_height * canvas_width // source_width)
    else:
        height = canvas_height
        width = max(1, source_width * canvas_height // source_height)
    return FitRect((canvas_width - width) // 2, (canvas_height - height) // 2, width, height)
