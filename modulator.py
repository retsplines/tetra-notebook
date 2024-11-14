from bitarray import bitarray


class Modulator:
    # Mapping between symbol value and multiples of pi/4
    SYMBOL_DIFFS = [
        1,  # 00
        3,  # 01
        -1,  # 10
        -3,  # 11
    ]

    # 8-PSK (aka DQPSK) I/Q mappings
    SYMBOL_IQ_MAPPING = [
        (1 + 0j),  # 0
        (0.7071067690849304 + 0.7071067690849304j),  # 1pi/4
        (0 + 1j),  # 2pi/4
        (-0.7071067690849304 + 0.7071067690849304j),  # 3pi/4
        (-1 + 0j),  # 4pi/4
        (-0.7071067690849304 - 0.7071067690849304j),  # 5pi/4
        (0 - 1j),  # 6pi/4
        (0.7071067690849304 - 0.7071067690849304j)  # 7pi/4
    ]

    @staticmethod
    def encode(burst: bitarray) -> list[complex]:
        """
        Convert a series of bits into a list of symbols.
        """

        if len(burst) % 2 != 0:
            raise Exception("Not possible to modulate using an odd-length bitstream")

        # Implicit start symbol
        last_symbol = 0

        # Modulated symbols, starting with an implicit zero
        symbols = [Modulator.SYMBOL_IQ_MAPPING[0]]

        for bn in range(0, len(burst), 2):
            # Calculate the symbol
            # TODO validate that the bit order of the symbols is right here...
            next_symbol = Modulator.SYMBOL_DIFFS[int(burst[bn + 1] | burst[bn] << 1)]

            # Difference
            last_symbol = (next_symbol + last_symbol) % 8

            # Push modulated symbol
            symbols.append(Modulator.SYMBOL_IQ_MAPPING[last_symbol])

        return symbols
