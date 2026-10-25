"""Music and sound effects, staying silent if no audio device is available."""

from pathlib import Path

import pygame


AUDIO_DIR = Path(__file__).with_name("assets") / "audio"
MUSIC_VOLUME = 0.45
SOUND_VOLUMES = {
    "click": 0.5,
    "card": 0.6,
    "pickup": 0.7,
    "hurt": 0.8,
    "zone": 0.5,
    "boost": 0.4,
    "victory": 0.8,
    "game_over": 0.8,
}


class Audio:
    def __init__(self) -> None:
        self.enabled = False
        self.muted = False
        self.current_music: str | None = None
        self.music_paused = False
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            for name, volume in SOUND_VOLUMES.items():
                path = AUDIO_DIR / f"{name}.wav"
                if path.exists():
                    sound = pygame.mixer.Sound(str(path))
                    sound.set_volume(volume)
                    self.sounds[name] = sound
        except pygame.error:
            return
        self.enabled = True

    def play(self, name: str) -> None:
        if self.enabled and not self.muted and name in self.sounds:
            self.sounds[name].play()

    def play_music(self, track: str) -> None:
        """Loop assets/audio/music_<track>.wav, unless it is already playing."""
        if not self.enabled or track == self.current_music:
            return
        path = AUDIO_DIR / f"music_{track}.wav"
        if not path.exists():
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0.0 if self.muted else MUSIC_VOLUME)
            pygame.mixer.music.play(-1, fade_ms=1500)
        except pygame.error:
            return
        self.current_music = track
        self.music_paused = False

    def stop_music(self, fade_ms: int = 600) -> None:
        if self.enabled:
            pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_music_paused(self, paused: bool) -> None:
        if not self.enabled or paused == self.music_paused:
            return
        if paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.music_paused = paused

    def toggle_mute(self) -> None:
        self.muted = not self.muted
        if not self.enabled:
            return
        pygame.mixer.music.set_volume(0.0 if self.muted else MUSIC_VOLUME)
        if self.muted:
            pygame.mixer.stop()
