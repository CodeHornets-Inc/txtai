"""
Signal module
"""

import numpy as np

# Conditional import
try:
    from scipy import signal

    SCIPY = True
except ImportError:
    SCIPY = False


class Signal:
    """
    Utility methods for audio signal processing.
    """

    @staticmethod
    def mono(audio):
        """
        Convert stereo to mono audio.

        Args:
            audio: audio data

        Returns:
            audio data with a single channel
        """

        return audio.mean(axis=1) if len(audio.shape) > 1 else audio

    @staticmethod
    def resample(audio, rate, target):
        """
        Resample audio if the sample rate doesn't match the target sample rate.

        Args:
            audio: audio data
            rate: current sample rate
            target: target sample rate

        Returns:
            audio resampled if necessary or original audio
        """

        if rate != target:
            # Transpose audio
            audio = audio.T

            # Resample audio and tranpose back
            samples = round(len(audio) * float(target) / rate)
            audio = signal.resample(audio, samples).T

        return audio

    @staticmethod
    def float32(audio):
        """
        Converts an input NumPy array with 16-bit ints to 32-bit floats.

        Args:
            audio: input audio array as 16-bit ints

        Returns:
            audio array as 32-bit floats
        """

        i = np.iinfo(audio.dtype)
        abs_max = 2 ** (i.bits - 1)
        offset = i.min + abs_max
        return (audio.astype(np.float32) - offset) / abs_max

    @staticmethod
    def int16(audio):
        """
        Converts an input NumPy array with 32-bit floats to 16-bit ints.

        Args:
            audio: input audio array as 32-bit floats

        Returns:
            audio array as 16-bit ints
        """

        i = np.iinfo(np.int16)
        absmax = 2 ** (i.bits - 1)
        offset = i.min + absmax
        return (audio * absmax + offset).clip(i.min, i.max).astype(np.int16)

    @staticmethod
    def mix(audio1, audio2, scale1=1, scale2=1):
        """
        Mixes audio1 and audio 2 into a single output audio segment.

        Args:
            audio1: audio segment 1
            audio2: audio segment 2
            scale1: scale factor for audio segment 1
            scale2: scale factor for audio segment 2
        """

        # Reshape audio, as necessary
        audio1 = audio1.reshape(1, -1) if len(audio1.shape) <= 1 else audio1
        audio2 = audio2.reshape(1, -1) if len(audio2.shape) <= 1 else audio2

        # Scale audio
        audio1 = audio1 * scale1
        audio2 = audio2 * scale2

        # Make audio files the same length
        large, small = (audio1, audio2) if audio1.shape[1] > audio2.shape[1] else (audio2, audio1)
        small = np.tile(small, (large.shape[1] // small.shape[1]) + 1).take(axis=1, indices=range(0, large.shape[1]))

        # Mix audio together
        return small + large