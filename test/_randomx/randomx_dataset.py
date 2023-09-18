import unittest
from randomx.randomx_dataset import randomx_dataset, datasetRead
from randomx.const import RegistersCount 
import os

class TestRandomxDataset(unittest.TestCase):

    def test_datasetRead(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_dump.bin'), 'rb') as f:
            data = f.read()
        dataset = randomx_dataset()
        dataset.memory = data
        # out
        datasetLine = [0] * RegistersCount

        # address = 1220394112
        blockNumber = 1220394112
        datasetRead(dataset.memory, blockNumber, datasetLine)
        self.assertEqual(datasetLine[0], 0xcf26f3c1771e4098)
        self.assertEqual(datasetLine[1], 0x9a3be331114fbe66)
        self.assertEqual(datasetLine[2], 0xa713208b0012c29b)
        self.assertEqual(datasetLine[3], 0x033ec03d81a79eb1)

