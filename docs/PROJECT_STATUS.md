# Broadcast-Studio Pro V05.0 — development restart

## Source of truth
The supplied screenshot is a **visual reference**, not proof of a working application. Preserve the approved dark navy, royal gold and electric-blue, single-window layout, large Input/Output monitors, processing controls, and full output path. Previous explicit instruction removed the BS Broadcast logo from this app; do not add it to the release without renewed approval.

## Required behavior
- Independent source loading in Input and Output monitors, synchronized playback and reliable audio/video lip-sync.
- Actual enhanced frames displayed in Output monitor; no fake 'AI rendering' status.
- Default 16:9 Safe Fit: no destructive cropping of heads or important content.
- MP4 export only. Stop & Save must finalize the successfully processed portion.
- Real-ESRGAN model and executable must be bundled for offline Windows distribution, not just model names in UI.
- Output directory D:\Broadcast-Studio Pro\Output; create automatically when possible, and display the complete path.
- RTX 4050 support should be verified on the target machine.
- Standalone Windows Setup must not require Python on the target machine.

## Work completed on this branch
- Pure-Python audio-master PTS and frame scheduling helpers in broadcast_core/sync.py.
- Pure-Python 16:9 Safe Fit geometry in broadcast_core/framing.py.
- Windows GitHub Actions unit-test workflow.
- The existing Windows packaging pipeline is inherited from the separate build-pipeline branch.

## Integration blockers
The connected repository does not yet contain the verified full application source. The latest individual V05 Python file found in the user's Library imports an optional urdu_edl module that is not available as a standalone Library Python file, and the corresponding verified tools/AI model assets have not been checked. No source has been copied from an unverified archive into this public repository.

These helpers are **not yet integrated into a GUI or media playback engine**. Unit tests do not verify exported lip-sync, GPU AI enhancement, real-time preview, UI visual parity, or standalone installer portability.

## Release gates
1. Identify verified current source ZIP/commit; inventory imports, DLLs, FFmpeg and Real-ESRGAN model weights.
2. Fix preview/output synchronization against actual decoded PTS and audio hardware clock.
3. Verify real AI preview, full headroom Safe Fit and MP4 Stop & Save.
4. Integrate approved interface without changing its placement.
5. Build Windows EXE and Setup; install on clean Windows PC.
6. Test real clips, long-run freezes, lip-sync, GPU model availability and stop/resume/export.
