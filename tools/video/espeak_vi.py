"""Giọng máy espeak-ng tiếng Việt – CHỈ dùng nội bộ làm "thước" căn thời gian (không đưa vào video)."""
import ctypes, numpy as np
import espeakng_loader as el

_lib = ctypes.cdll.LoadLibrary(el.get_library_path())
_CB = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.c_void_p)
_buf = []


@_CB
def _cb(wav, n, ev):
    if n > 0: _buf.append(np.ctypeslib.as_array(wav, shape=(n,)).copy())
    return 0


SR = _lib.espeak_Initialize(2, 0, el.get_data_path().encode(), 0)  # AUDIO_OUTPUT_SYNCHRONOUS
_lib.espeak_SetSynthCallback(_cb)
_lib.espeak_SetVoiceByName(b"vi")
_lib.espeak_SetParameter(1, 150, 0)  # tốc độ


def noi(text):
    _buf.clear()
    b = text.encode("utf-8")
    _lib.espeak_Synth(b, len(b) + 1, 0, 1, 0, 1, None, None)  # POS_CHARACTER, espeakCHARS_UTF8
    _lib.espeak_Synchronize()
    return (np.concatenate(_buf).astype(np.float32) / 32768) if _buf else np.zeros(1, np.float32)
