PLUGIN_CATEGORY = 'Q'
PLUGIN_NAME     = 'QFernet24'
PLUGIN_TAGS     = ['optical', 'modulation', 'fernet', 'post-quantum']


import math
from qfernet24 import EvoDecoderEnhanced

class QFernet24:
    def __init__(self, laser_wavelengths=None, laser_intensities=None, lookup_table=None,
                 alpha=0.4, threshold=0.015, crystal_lambda=440e-9):
        self.decoder = EvoDecoderEnhanced(
            laser_wavelengths=laser_wavelengths,
            laser_intensities=laser_intensities,
            lookup_table=lookup_table,
            alpha=alpha,
            threshold=threshold,
            crystal_lambda=crystal_lambda
        )
        self.bits_per_symbol = math.log2(24)
        self.num_symbols = math.ceil(64 / self.bits_per_symbol)

    def encode_block(self, block: int) -> list[list[int]]:
        bitstr = format(block & ((1 << 64) - 1), '064b')
        bits_per_sym = math.ceil(64 / self.num_symbols)
        states = []
        for i in range(self.num_symbols):
            grp = bitstr[i*bits_per_sym:(i+1)*bits_per_sym].ljust(bits_per_sym, '0')
            bits = [int(b) for b in grp]
            state = bits[:5] + [0]*(5 - len(bits))
            states.append(state)
        return states

    def decode_block(self, symbol_states: list[list[int]]) -> int:
        bits = []
        for state in symbol_states:
            symbol = self.decoder.step(state)
            bitchunk = format(symbol, f"0{int(self.bits_per_symbol)}b")
            bits.extend(int(b) for b in bitchunk)
        bits = bits[:64] + [0]*(64 - len(bits))
        value = 0
        for b in bits:
            value = (value << 1) | b
        return value
        