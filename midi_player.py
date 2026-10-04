import math
import struct
import wave
import sys
import os
import subprocess


class MidiPlayer:
    """
    CSDS 233 - Programming Assignment 1
    An zero-dependency, real-time wave audio synthesizer.
    Supports chords using the '+' connector (e.g. "C4+E4+G4:1.0").
    """
    NOTE_OFFSETS = {
        'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11
    }

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.temp_filename = "temp_playback.wav"

    def parse_pitch_to_midi(self, pitch: str) -> int:
        """Parses a pitch string (e.g., 'C4', 'D#5', 'Eb3') to a MIDI number."""
        clean_pitch = pitch.strip().upper()
        if not clean_pitch or clean_pitch.startswith('R'):
            return -1

        base_note = clean_pitch[0]
        if base_note not in self.NOTE_OFFSETS:
            return -1

        offset = self.NOTE_OFFSETS[base_note]
        accidental = 0
        octave_idx = 1

        if len(clean_pitch) > 1:
            if clean_pitch[1] == '#':
                accidental = 1
                octave_idx = 2
            elif clean_pitch[1] == 'B':
                accidental = -1
                octave_idx = 2

        octave = 4  # Default octave
        if octave_idx < len(clean_pitch):
            try:
                octave = int(clean_pitch[octave_idx:])
            except ValueError:
                pass

        return (octave + 1) * 12 + offset + accidental

    def midi_to_freq(self, midi_note: int) -> float:
        """Converts MIDI integer values to sound frequencies (Hz)."""
        if midi_note == -1:
            return 0.0
        return 440.0 * (2.0 ** ((midi_note - 69.0) / 12.0))

    def play(self, phrase: str):
        """Compiles note-tokens (including chords) into a temporary wave file and plays it."""
        if not phrase or not phrase.strip():
            return

        tokens = phrase.strip().split()
        all_samples = []

        print("\nPlaying Phrase Visualization:")
        print("-" * 50)

        for token in tokens:
            if ':' not in token:
                continue
            pitches_str, duration_str = token.split(':')
            duration = float(duration_str)

            # Split pitch string to check for chords
            pitch_tokens = pitches_str.split('+')
            frequencies = []

            for p in pitch_tokens:
                midi_note = self.parse_pitch_to_midi(p)
                if midi_note != -1:
                    frequencies.append(self.midi_to_freq(midi_note))

            # Display CLI visualization
            if not frequencies:
                print(f" [ REST  ] " + "." * int(duration * 10))
            else:
                notes_display = "+".join(pitch_tokens)
                visual_bar = "=" * int(duration * 10)
                print(f" [{notes_display:<10}] {visual_bar}>")

            num_samples = int(self.sample_rate * duration)
            amplitude = 0.4 * 32767  # Volume scaling

            for i in range(num_samples):
                if not frequencies:
                    val = 0
                else:
                    # Superposition: Sum all sine waves of active notes in the chord
                    wave_sum = 0.0
                    for freq in frequencies:
                        wave_sum += math.sin(2 * math.pi * freq * i / self.sample_rate)

                    # Normalize amplitude by dividing by total active voices to prevent distortion
                    wave_sum = wave_sum / len(frequencies)

                    # Apply decay envelope to prevent popping/clicks between notes
                    envelope = 1.0
                    decay_start = int(num_samples * 0.9)
                    if i > decay_start:
                        envelope = 1.0 - (i - decay_start) / (num_samples - decay_start)

                    val = int(amplitude * envelope * wave_sum)

                all_samples.append(struct.pack('<h', val))

        print("-" * 50)

        if not all_samples:
            return

        # Write data to temporary WAV file
        packed_samples = b''.join(all_samples)
        try:
            with wave.open(self.temp_filename, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(packed_samples)
        except Exception as e:
            print(f"Error compiling WAV file: {e}")
            return

        # Execute system native audio playing command
        try:
            if sys.platform.startswith('win'):
                import winsound
                winsound.PlaySound(self.temp_filename, winsound.SND_FILENAME)
            elif sys.platform == 'darwin':
                subprocess.run(['afplay', self.temp_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(['aplay', self.temp_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[SYSTEM NOTICE] Audio could not play natively on this machine: {e}")
        finally:
            if os.path.exists(self.temp_filename):
                try:
                    os.remove(self.temp_filename)
                except OSError:
                    pass

    def close(self):
        if os.path.exists(self.temp_filename):
            try:
                os.remove(self.temp_filename)
            except OSError:
                pass
