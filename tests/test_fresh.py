import unittest
import fresh


class TestFresh(unittest.TestCase):
    def test_extract_track_url_if_present(self):
        search_result = {
            'tracks': {
                'items': [
                    {
                        'external_urls': {
                            'spotify': 'https://open.spotify.com/track/1TlPpvXcPX8xlD2CiOsds7'
                        }
                    }
                ]
            }
        }

        url = fresh.extract_track_url(search_result)

        self.assertEqual(url, 'https://open.spotify.com/track/1TlPpvXcPX8xlD2CiOsds7')

    def test_extract_track_url_none_if_no_tracks_present(self):
        search_result = {
            'tracks': {
                'items': []
            }
        }

        url = fresh.extract_track_url(search_result)

        self.assertEqual(url, None)