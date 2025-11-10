import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_otetaan_liikaa(self):
        self.varasto.lisaa_varastoon(5)
        otettu = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(otettu, 5)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_tyhja_varasto_ja_otetaan(self):
        self.varasto.lisaa_varastoon(0)
        otettu = self.varasto.ota_varastosta(5)
        self.assertAlmostEqual(otettu, 0)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisataan_liikaa_tavaraa(self):
        self.varasto.lisaa_varastoon(15) # yli tilavuuden
        self.assertAlmostEqual(self.varasto.saldo, 10)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 0)

    # I <3 TKO ÄLY

    def test_konstruktori_rajaa_alkuarvot(self):
        v1 = Varasto(-5, -5)      # tilavuus ja saldo negatiiviset
        v2 = Varasto(5, 10)       # saldo yli tilavuuden
        self.assertAlmostEqual(v1.tilavuus, 0)
        self.assertAlmostEqual(v1.saldo, 0)
        self.assertAlmostEqual(v2.saldo, 5)

    def test_negatiivinen_lisays_ei_muuta_saldoa(self):
        self.varasto.lisaa_varastoon(-5)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivinen_otto_palauttaa_nollan(self):
        self.varasto.lisaa_varastoon(5)
        saatu = self.varasto.ota_varastosta(-1)
        self.assertAlmostEqual(saatu, 0)
        self.assertAlmostEqual(self.varasto.saldo, 5)

    def test_tulostus(self):
        self.varasto.lisaa_varastoon(5)
        teksti = str(self.varasto)
        self.assertIn("saldo = 5", teksti)
        self.assertIn("vielä tilaa 5", teksti)
