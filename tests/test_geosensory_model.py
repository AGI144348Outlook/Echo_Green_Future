import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from geosensory_model import usgs_model

class ModelTests(unittest.TestCase):
    def feed(self):
        return {'type':'FeatureCollection','metadata':{'generated':1000},'features':[{'id':'event','geometry':{'type':'Point','coordinates':[-94,29,8]},'properties':{'mag':0,'magType':'ml','time':100,'place':'Test fixture'}}]}
    def test_zero_and_event_age_are_preserved(self):
        model=usgs_model(self.feed(),'https://example.test/feed',1100)
        self.assertEqual(model['points'][0]['value'],0)
        self.assertEqual(model['freshness'],'fresh')
        self.assertEqual(model['points'][0]['information_kind'],'derived')
    def test_stale_missing_future(self):
        self.assertEqual(usgs_model(self.feed(),'x',2000,10)['freshness'],'stale')
        f=self.feed();f['metadata']={}
        self.assertEqual(usgs_model(f,'x',2000)['freshness'],'missing')
        self.assertEqual(usgs_model(self.feed(),'x',0)['freshness'],'future')
    def test_bad_coordinates_not_invented(self):
        f=self.feed();f['features'][0]['geometry']['coordinates']=[200,29,8]
        model=usgs_model(f,'x',1100)
        self.assertEqual(model['points'],[])
        self.assertEqual(len(model['rejected']),1)
    def test_null_magnitude_not_zero(self):
        f=self.feed();f['features'][0]['properties']['mag']=None
        self.assertIsNone(usgs_model(f,'x',1100)['points'][0]['value'])

if __name__=='__main__': unittest.main()
