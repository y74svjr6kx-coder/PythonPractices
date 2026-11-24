from pathlib import Path
import pygame


class MusicPlayer:
    def __init__(self):
        music_dir = Path(__file__).resolve().parent / 'music'

        self.playlist = sorted(
            p for p in music_dir.rglob('*')
            if p.is_file() and p.suffix.lower() in ('.mp3', '.wav', '.ogg')
        )

        self.index = 0
        self.playing = False
        self.paused = False
        self.position_seconds = 0.0
        self.duration_seconds = 0.0
        self.error = ''

        self.end_event = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.end_event)

    @property
    def current(self):
        return self.playlist[self.index] if self.playlist else None

    def _duration(self, path):
        try:
            if path.suffix.lower() == '.wav':
                import wave

                with wave.open(str(path), 'rb') as wav:
                    return wav.getnframes() / wav.getframerate()

            from mutagen import File

            audio = File(str(path))

            return (
                float(audio.info.length)
                if audio and audio.info
                else 0.0
            )

        except (
            ImportError,
            OSError,
            ValueError,
            AttributeError,
            EOFError,
            ZeroDivisionError
        ):
            return 0.0

    def play(self):
        if not self.current:
            self.error = 'No tracks found. Add MP3, WAV or OGG files to music/.'
            return

        try:
            pygame.mixer.music.load(str(self.current))
            pygame.mixer.music.play()

            self.duration_seconds = self._duration(self.current)
            self.position_seconds = 0.0

            self.playing = True
            self.paused = False
            self.error = ''

        except (pygame.error, OSError) as exc:
            self.error = f'Cannot play track: {exc}'
            self.playing = False
            self.paused = False

    def pause_resume(self):
        if not self.playing:
            return

        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def stop(self):
        pygame.mixer.music.stop()

        self.playing = False
        self.paused = False
        self.position_seconds = 0.0

    def next(self):
        if self.playlist:
            self.index = (self.index + 1) % len(self.playlist)
            self.play()

    def previous(self):
        if self.playlist:
            self.index = (self.index - 1) % len(self.playlist)
            self.play()

    def update(self):
        if self.playing and not self.paused:
            pos = pygame.mixer.music.get_pos()

            if pos >= 0:
                self.position_seconds = pos / 1000.0

    def handle_event(self, event):
        if event.type == self.end_event and self.playing and not self.paused:
            self.next()
