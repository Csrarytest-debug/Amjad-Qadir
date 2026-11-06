"""Audio-master playback timeline helpers.

These helpers do not decode media or play audio. Integrate with a decoder's
presentation timestamps and the actual audio device's played-sample counter.
Do not drive the audio clock from decoded samples or wall-clock guesses.
"""
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction


class FrameAction(str, Enum):
    WAIT = "wait"
    PRESENT = "present"
    DROP = "drop"


@dataclass(frozen=True)
class FrameDecision:
    action: FrameAction
    offset_seconds: float


@dataclass(frozen=True)
class AudioMasterClock:
    """Map an audio device's sample playback position to source PTS.

    start_pts is the source timestamp (seconds) at which playback began.
    played_samples is a hardware-reported counter, not a queued-sample count.
    device_latency_samples is samples already counted but not yet audible.
    """
    sample_rate: int
    start_pts: Fraction = Fraction(0)

    def __post_init__(self):
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")

    def source_pts(self, played_samples: int, device_latency_samples: int = 0) -> Fraction:
        if played_samples < 0 or device_latency_samples < 0:
            raise ValueError("sample counters must not be negative")
        audible_samples = max(0, played_samples - device_latency_samples)
        return self.start_pts + Fraction(audible_samples, self.sample_rate)


def frame_decision(
    frame_pts: Fraction,
    audio_pts: Fraction,
    *,
    early_tolerance: Fraction = Fraction(1, 100),
    late_tolerance: Fraction = Fraction(2, 25),
) -> FrameDecision:
    """WAIT for early frames, DROP frames too late for the audio master."""
    if early_tolerance < 0 or late_tolerance < 0:
        raise ValueError("tolerances must not be negative")
    offset = frame_pts - audio_pts
    if offset > early_tolerance:
        return FrameDecision(FrameAction.WAIT, float(offset))
    if offset < -late_tolerance:
        return FrameDecision(FrameAction.DROP, float(offset))
    return FrameDecision(FrameAction.PRESENT, float(offset))


def frame_pts_from_index(frame_index: int, fps_numerator: int, fps_denominator: int = 1, start_pts: Fraction = Fraction(0)) -> Fraction:
    """Exact CFR timestamp. For VFR use decoded per-frame PTS instead."""
    if frame_index < 0 or fps_numerator <= 0 or fps_denominator <= 0:
        raise ValueError("invalid frame index or frame rate")
    return start_pts + Fraction(frame_index * fps_denominator, fps_numerator)
