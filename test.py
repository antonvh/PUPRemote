import unittest
from PUPRemote.pd_emu import _calc_checksum

class TestCalcChecksum(unittest.TestCase):

    def test_bytes_input(self):
        data = bytes([0x51, 0x07, 0x07, 0x0a, 0x07 ])
        self.assertEqual(_calc_checksum(data), 0xa3)

    def test_list_of_integers_input(self):
        data = [0x49, 0x05, 0x02]
        self.assertEqual(_calc_checksum(data), 0xb1)

    def test_mixed_input(self):
        data = [0x52, bytes([0x00, 0xc2]), [0x01, 0x00] ]
        self.assertEqual(_calc_checksum(data), 0x6e)

    def test_empty_bytes(self):
        data = bytes([])
        self.assertEqual(_calc_checksum(data), 0xff)

    def test_empty_list(self):
        data = []
        self.assertEqual(_calc_checksum(data), 0xff)

    def test_mixed_with_empty_elements(self):
        data = [0x49, [], bytes([]), [0x05, 0x02]]
        self.assertEqual(_calc_checksum(data), 0xb1)

if __name__ == '__main__':
    unittest.main()