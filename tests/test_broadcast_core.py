import unittest
from fractions import Fraction

from broadcast_core.sync import AudioMasterClock, FrameAction, frame_decision, frame_pts_from_index
from broadcast_core.framing import safe_fit_rect


class TestSync(unittest.TestCase):
    def test_25fps_exact(self):
        self.assertEqual(frame_pts_from_index(50, 25), Fraction(2))

    def test_ntsc_fractional_rate(self):
        self.assertEqual(frame_pts_from_index(30000, 30000, 1001), Fraction(1001))

    def test_audio_master_samples(self):
        clock = AudioMasterClock(48000, Fraction(5))
        self.assertEqual(clock.source_pts(96000), Fraction(7))

    def test_latency_compensation(self):
        clock = AudioMasterClock(48000)
        self.assertEqual(clock.source_pts(48000, 4800), Fraction(9, 10))

    def test_early_wait(self):
        self.assertEqual(frame_decision(Fraction(1, 2), Fraction(0)).action, FrameAction.WAIT)

    def test_late_drop(self):
        self.assertEqual(frame_decision(Fraction(0), Fraction(1, 2)).action, FrameAction.DROP)

    def test_on_time_present(self):
        self.assertEqual(frame_decision(Fraction(1), Fraction(1)).action, FrameAction.PRESENT)

    def test_invalid_audio_rate(self):
        with self.assertRaises(ValueError):
            AudioMasterClock(0)


class TestFraming(unittest.TestCase):
    def test_4_by_3_safe_fit(self):
        r = safe_fit_rect(720, 540)
        self.assertEqual((r.x, r.y, r.width, r.height), (240, 0, 1440, 1080))

    def test_16_by_9_fills(self):
        r = safe_fit_rect(1920, 1080)
        self.assertEqual((r.x, r.y, r.width, r.height), (0, 0, 1920, 1080))

    def test_portrait_pillarbox(self):
        r = safe_fit_rect(1080, 1920)
        self.assertEqual(r.height, 1080)
        self.assertTrue(r.x > 0)

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            safe_fit_rect(0, 1080)


if __name__ == "__main__":
    unittest.main()
