"""Generate Tidekeeper's original music and sound effects as WAV files once.

Uses only the Python standard library so no extra dependencies are needed.
"""

from pathlib import Path
import math
import random
import struct
import wave


ROOT = Path(__file__).resolve().parents[1] / "assets" / "audio"
RATE = 22050
TAU = math.tau

# Harmonic recipes as amplitudes of integer multiples of the base frequency.
PAD = (1.0, 0.35, 0.12)
PLUCK = (1.0, 0.5, 0.25, 0.1)
SQUARE_SOFT = (1.0, 0.0, 0.3, 0.0, 0.15)
BELL = (1.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.08)


def hz(midi_note: float) -> float:
    return 440.0 * 2 ** ((midi_note - 69) / 12)


def silence(seconds: float) -> list[float]:
    return [0.0] * int(seconds * RATE)


def add_voice(
    buffer: list[float],
    start: float,
    duration: float,
    freq: float,
    volume: float,
    *,
    end_freq: float | None = None,
    attack: float = 0.01,
    release: float = 0.08,
    decay: float = 0.0,
    harmonics: tuple[float, ...] = (1.0,),
    vibrato: float = 0.0,
    wrap: bool = False,
) -> None:
    """Mix one enveloped tone into the buffer; wrap=True folds tails into a loop."""
    total = len(buffer)
    offset = int(start * RATE)
    count = int(duration * RATE)
    attack_n = max(1, int(attack * RATE))
    release_n = max(1, int(release * RATE))
    phase = 0.0
    for i in range(count):
        t = i / RATE
        f = freq if end_freq is None else freq * (end_freq / freq) ** (i / count)
        if vibrato:
            f *= 1.0 + vibrato * math.sin(TAU * 4.5 * t)
        phase += TAU * f / RATE
        env = min(1.0, i / attack_n, (count - i) / release_n)
        if decay:
            env *= math.exp(-decay * t)
        value = 0.0
        for k, amplitude in enumerate(harmonics, start=1):
            if amplitude:
                value += amplitude * math.sin(phase * k)
        index = offset + i
        if wrap:
            index %= total
        elif index >= total:
            break
        buffer[index] += value * env * volume


def add_noise(
    buffer: list[float],
    start: float,
    duration: float,
    volume: float,
    *,
    attack: float = 0.005,
    release: float = 0.05,
    decay: float = 0.0,
    smoothing: float = 0.2,
    highpass: bool = False,
    seed: int = 0,
    wrap: bool = False,
) -> None:
    """Mix one-pole filtered noise; small smoothing values sound darker."""
    rng = random.Random(seed)
    total = len(buffer)
    offset = int(start * RATE)
    count = int(duration * RATE)
    attack_n = max(1, int(attack * RATE))
    release_n = max(1, int(release * RATE))
    low = 0.0
    for i in range(count):
        sample = rng.uniform(-1.0, 1.0)
        low += smoothing * (sample - low)
        value = sample - low if highpass else low
        env = min(1.0, i / attack_n, (count - i) / release_n)
        if decay:
            env *= math.exp(-decay * i / RATE)
        index = offset + i
        if wrap:
            index %= total
        elif index >= total:
            break
        buffer[index] += value * env * volume


def add_bubble(buffer: list[float], start: float, pitch: float, volume: float) -> None:
    """A short upward chirp, like an air bubble popping free."""
    add_voice(
        buffer, start, 0.07, pitch, volume,
        end_freq=pitch * 2.2, attack=0.004, release=0.03, decay=25,
    )


def save(samples: list[float], name: str, peak: float = 0.85) -> None:
    loudest = max(abs(value) for value in samples) or 1.0
    scale = peak / loudest * 32767
    frames = struct.pack(f"<{len(samples)}h", *(int(value * scale) for value in samples))
    path = ROOT / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(RATE)
        file.writeframes(frames)
    print(f"Created {path.relative_to(ROOT.parents[1])} ({len(samples) / RATE:.1f}s)")


def explore_music() -> None:
    """Slow, airy D-major pads with sparse bell-like arpeggios; loops seamlessly."""
    beat = 60 / 72
    bar = beat * 4
    chords = [
        (50, (62, 66, 69, 73)),  # Dmaj7
        (47, (59, 62, 66, 69)),  # Bm7
        (43, (55, 59, 62, 66)),  # Gmaj7
        (45, (57, 61, 64, 66)),  # A6
    ]
    chord_length = bar * 2
    track = silence(chord_length * len(chords))
    rng = random.Random(7)
    for index, (root, tones) in enumerate(chords):
        start = index * chord_length
        add_voice(
            track, start, chord_length + 1.5, hz(root - 12), 0.22,
            attack=1.2, release=2.0, harmonics=PAD, wrap=True,
        )
        for tone in tones:
            add_voice(
                track, start, chord_length + 2.0, hz(tone), 0.07,
                attack=1.8, release=2.6, harmonics=PAD, vibrato=0.003, wrap=True,
            )
        arpeggio = [tone + 12 for tone in tones] + [tones[1] + 24]
        for step in range(16):
            if rng.random() < 0.45:
                continue
            add_voice(
                track, start + step * beat / 2, 2.2, hz(rng.choice(arpeggio)), 0.06,
                attack=0.01, release=0.6, decay=2.2, harmonics=BELL, wrap=True,
            )
    for _ in range(24):
        add_bubble(track, rng.uniform(0, len(track) / RATE - 0.1), rng.uniform(500, 900), 0.025)
    save(track, "music_explore", peak=0.8)


def play_music() -> None:
    """Upbeat A-minor groove with bass, arpeggio and soft percussion; loops seamlessly."""
    beat = 60 / 112
    bar = beat * 4
    sixteenth = beat / 4
    progression = [
        (45, (57, 60, 64)),  # Am
        (41, (53, 57, 60)),  # F
        (48, (55, 60, 64)),  # C
        (43, (55, 59, 62)),  # G
    ]
    bars = progression * 2
    track = silence(bar * len(bars))
    bass_pattern = (0, 0, 12, 0, 7, 0, 12, 7)
    for bar_index, (root, tones) in enumerate(bars):
        start = bar_index * bar
        for step, interval in enumerate(bass_pattern):
            add_voice(
                track, start + step * beat / 2, beat / 2, hz(root - 12 + interval), 0.32,
                attack=0.005, release=0.06, decay=4.0, harmonics=PLUCK, wrap=True,
            )
        ascending = [tone + 12 for tone in tones] + [tones[0] + 24]
        figure = ascending + ascending[-2:0:-1] if bar_index >= 4 else ascending
        for step in range(16):
            add_voice(
                track, start + step * sixteenth, sixteenth * 1.8,
                hz(figure[step % len(figure)]), 0.07,
                attack=0.004, release=0.05, decay=9.0, harmonics=SQUARE_SOFT, wrap=True,
            )
        add_voice(
            track, start, bar + 0.4, hz(tones[0]), 0.05,
            attack=0.25, release=0.4, harmonics=PAD, wrap=True,
        )
        for beat_index in range(4):
            beat_start = start + beat_index * beat
            if beat_index % 2 == 0:
                add_voice(
                    track, beat_start, 0.22, 140, 0.55,
                    end_freq=45, attack=0.002, release=0.05, decay=14, wrap=True,
                )
            else:
                add_noise(
                    track, beat_start, 0.12, 0.18,
                    smoothing=0.15, decay=30, seed=bar_index * 4 + beat_index, wrap=True,
                )
            add_noise(
                track, beat_start + beat / 2, 0.05, 0.07,
                smoothing=0.3, highpass=True, decay=60, seed=99 + beat_index, wrap=True,
            )
    save(track, "music_play", peak=0.8)


def sound_effects() -> None:
    click = silence(0.12)
    add_voice(click, 0, 0.12, hz(81), 0.5, attack=0.002, release=0.04, decay=35, harmonics=PLUCK)
    save(click, "click", peak=0.6)

    card = silence(0.9)
    add_voice(card, 0.0, 0.8, hz(76), 0.4, attack=0.004, release=0.3, decay=5, harmonics=BELL)
    add_voice(card, 0.09, 0.8, hz(83), 0.4, attack=0.004, release=0.3, decay=5, harmonics=BELL)
    add_bubble(card, 0.02, 600, 0.15)
    save(card, "card", peak=0.7)

    pickup = silence(0.5)
    for index, note in enumerate((72, 76, 79, 84)):
        add_voice(
            pickup, index * 0.045, 0.3, hz(note), 0.35,
            attack=0.003, release=0.1, decay=10, harmonics=SQUARE_SOFT,
        )
    add_bubble(pickup, 0.0, 700, 0.25)
    add_bubble(pickup, 0.08, 950, 0.2)
    save(pickup, "pickup", peak=0.75)

    hurt = silence(0.45)
    add_voice(hurt, 0, 0.42, 260, 0.6, end_freq=90, attack=0.003, release=0.12, decay=6, harmonics=SQUARE_SOFT)
    add_noise(hurt, 0, 0.2, 0.35, smoothing=0.1, decay=18, seed=3)
    save(hurt, "hurt", peak=0.85)

    zone = silence(1.8)
    for index, note in enumerate((69, 73, 76)):
        add_voice(
            zone, index * 0.12, 1.6, hz(note), 0.3,
            attack=0.01, release=0.6, decay=2.5, harmonics=BELL,
        )
    save(zone, "zone", peak=0.55)

    boost = silence(0.6)
    add_noise(boost, 0, 0.6, 0.8, attack=0.12, release=0.4, smoothing=0.06, seed=11)
    for index in range(5):
        add_bubble(boost, 0.05 + index * 0.08, 550 + index * 90, 0.12)
    save(boost, "boost", peak=0.6)

    victory = silence(2.4)
    for index, note in enumerate((60, 64, 67, 72)):
        add_voice(
            victory, index * 0.13, 0.5, hz(note), 0.35,
            attack=0.004, release=0.15, decay=4, harmonics=SQUARE_SOFT,
        )
    for note in (72, 76, 79, 84):
        add_voice(
            victory, 0.55, 1.8, hz(note), 0.2,
            attack=0.02, release=0.9, decay=1.2, harmonics=BELL,
        )
    add_voice(victory, 0.55, 1.8, hz(48), 0.35, attack=0.02, release=0.9, decay=1.2, harmonics=PAD)
    save(victory, "victory", peak=0.8)

    game_over = silence(2.2)
    for index, note in enumerate((69, 67, 64, 60)):
        add_voice(
            game_over, index * 0.32, 0.6 if index < 3 else 1.6, hz(note), 0.35,
            attack=0.01, release=0.3, decay=2.5 if index < 3 else 1.2, harmonics=PAD,
        )
    add_voice(game_over, 0.96, 1.2, hz(45), 0.3, attack=0.02, release=0.8, decay=1.0, harmonics=PAD)
    save(game_over, "game_over", peak=0.75)


def main() -> None:
    sound_effects()
    explore_music()
    play_music()


if __name__ == "__main__":
    main()
