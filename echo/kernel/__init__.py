"""The ECHO kernel.

skeleton.py is copied unchanged from echo_governor_skeleton.py in the
repository, so local ECHO and repository ECHO are the same code. Update it
by replacing the file, never by editing it here.
"""
import warnings as _w
with _w.catch_warnings():
    _w.simplefilter("ignore", SyntaxWarning)  # one invalid escape at line 6892 of the original
    from . import skeleton as K

HEBREW_LETTER_INDEX = K.HEBREW_LETTER_INDEX
AlgorithmMatrix = K.AlgorithmMatrix
State, Request, Context = K.State, K.Request, K.Context
run_cycle, phi = K.run_cycle, K.phi


def kernel_lines():
    import os
    try:
        with open(os.path.join(os.path.dirname(__file__), "skeleton.py"), encoding="utf-8") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0
