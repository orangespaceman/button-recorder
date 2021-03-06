# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Drivers for audio functionality provided by the VoiceHat."""

import numpy as np
import struct
import time
import wave

from aiy.voice import tts
import aiy._drivers._player
import aiy._drivers._recorder
import aiy.i18n

AUDIO_SAMPLE_SIZE = 2  # bytes per sample
AUDIO_SAMPLE_RATE_HZ = 16000

# Global variables. They are lazily initialized.
_voicehat_recorder = None
_voicehat_player = None
_status_ui = None

class _WaveDump(object):
    """A processor that saves recorded audio to a wave file."""

    def __init__(self, filepath, duration):
        self._wave = wave.open(filepath, 'wb')
        self._wave.setnchannels(1)
        self._wave.setsampwidth(2)
        self._wave.setframerate(16000)
        self._bytes = 0
        self._bytes_limit = int(duration * 16000) * 1 * 2

    def add_data(self, data):
        max_bytes = self._bytes_limit - self._bytes
        data = data[:max_bytes]
        self._bytes += len(data)
        if data:
            self._wave.writeframes(data)

    def is_done(self):
        return self._bytes >= self._bytes_limit

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._wave.close()


def get_player():
    """Returns a driver to control the VoiceHat speaker.

    The aiy modules automatically use this player. So usually you do not need to
    use this. Instead, use 'aiy.audio.play_wave' if you would like to play some
    audio.
    """
    global _voicehat_player
    if not _voicehat_player:
        _voicehat_player = aiy._drivers._player.Player()
    return _voicehat_player


def get_recorder():
    """Returns a driver to control the VoiceHat microphones.

    The aiy modules automatically use this recorder. So usually you do not need to
    use this.
    """
    global _voicehat_recorder
    if not _voicehat_recorder:
        _voicehat_recorder = aiy._drivers._recorder.Recorder()
    return _voicehat_recorder


def record_to_wave(filepath, duration):
    """Records an audio for the given duration to a wave file."""
    recorder = get_recorder()
    dumper = _WaveDump(filepath, duration)
    with dumper:
        recorder.add_processor(dumper)
        while not dumper.is_done():
            time.sleep(0.1)
        recorder.remove_processor(dumper)


def play_wave(wave_file):
    """Plays the given wave file.

    The wave file has to be mono and small enough to be loaded in memory.
    """
    player = get_player()
    player.play_wav(wave_file)


def play_audio(audio_data, volume=50):
    """Plays the given audio data."""
    player = get_player()

    db_range = -60.0 - (-60.0 * (volume / 100.0))
    db_scaler = 10 ** (db_range / 20)

    adjusted_audio_data = np.multiply(np.frombuffer(
        audio_data, dtype=np.int16), db_scaler).astype(np.int16).tobytes()

    player.play_bytes(adjusted_audio_data, sample_width=AUDIO_SAMPLE_SIZE,
                      sample_rate=AUDIO_SAMPLE_RATE_HZ)


def say(words, lang=None, volume=60, pitch=130):
    """Says the given words in the given language with Google TTS engine.

    If lang is specified, e.g. "en-US", it will be used to say the given words.
    Otherwise, the language from aiy.i18n will be used.
    volume (optional) volume used to say the given words.
    pitch (optional) pitch to say the given words.
    Example: aiy.audio.say('This is an example', lang="en-US", volume=75, pitch=135)
    Any of the optional variables can be left out.
    """
    if not lang:
        lang = aiy.i18n.get_language_code()
    tts.say(words, lang=lang, volume=volume, pitch=pitch)
