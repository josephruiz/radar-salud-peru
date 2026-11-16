import unittest
from collector.daily import region_in_title, parse_rss, REGIONS
class DailyTests(unittest.TestCase):
    def test_region(self):
        self.assertEqual(region_in_title("Nueva campaña de salud en Piura"),"Piura")
        self.assertIsNone(region_in_title("Campaña nacional de salud"))
    def test_region_count(self):
        self.assertEqual(len(REGIONS),25)
    def test_rss_date(self):
        sample=b"<rss><channel><item><title>Salud en Tumbes</title><link>https://example.org/a</link><pubDate>Sun, 15 Nov 2026 17:00:00 GMT</pubDate><source>Ejemplo</source></item></channel></rss>"
        found=parse_rss(sample,"2026-11-15")
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]["region"],"Tumbes")
        self.assertEqual(parse_rss(sample,"2026-11-14"),[])
if __name__=="__main__":unittest.main()
