# STIP: Structural Timeline of Intellectual Progression

"""
Main module for detecting semantic paradigm shifts in research literature.
"""

from .detector import ParadigmShiftDetector
from .embedding import TemporalEmbedding
from .shift_analyzer import ShiftAnalyzer

__version__ = "0.1.0"
__author__ = "STIP Contributors"

__all__ = [
    "ParadigmShiftDetector",
    "TemporalEmbedding",
    "ShiftAnalyzer"
]
