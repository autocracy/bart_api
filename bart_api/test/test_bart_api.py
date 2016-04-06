import unittest
try:
  from unittest.mock import patch, Mock, MagicMock
except ImportError:
  from mock import patch, Mock

from bart_api import BartApi
from lxml import etree

class TestBartApi(unittest.TestCase):

  def setUp(self):
    self.bart = BartApi()
    self._cur_sched = None

  @property
  def cur_sched(self):
    if not self._cur_sched:
      self._cur_sched = self.bart.get_schedules()[-1]['id']
    return self._cur_sched

  def test_api_key(self):
    expected = "MW9S-E7SL-26DU-VV8V"
    actual = self.bart.api_key
    self.assertEqual(expected, actual)

  def test_number_of_trains(self):
    expected = 45
    actual = int(self.bart.number_of_trains())
    self.assertLess(expected, actual)

  def test_elevator_status(self):
    expected = 10
    actual = len(self.bart.elevator_status())
    self.assertLess(expected, actual)

  def test_get_stations(self):
    expected = "12th St. Oakland City Center"
    stations = self.bart.get_stations()
    actual = stations[0].get("name")
    self.assertEqual(expected, actual)

  def test_bsa_all(self):
    expected = 10
    actual = len(self.bart.bsa())
    self.assertLess(expected, actual)
  
  def test_bsa_specific(self):
    expected = 10
    actual = len(self.bart.bsa("WOAK"))
    self.assertLess(expected, actual)
  
  def test_station_info(self):
    expected = "94110"
    station_info = self.bart.station_info("24TH")
    actual = station_info.get("zipcode")
    self.assertEqual(expected, actual)
  
  def test_station_access(self):
    expected = "" 
    station_info = self.bart.station_access("12TH", "1")
    actual = station_info.get("car_share")
    self.assertEqual(expected, actual)

  def test_etd(self):
    expected = "2"
    station_info = self.bart.etd("RICH", "2", "s")
    actual = station_info[0].get("estimates")[0].get("platform")
    self.assertEqual(expected, actual)

  def test_routes(self):
    expected = "1"
    station_info = self.bart.routes(self.cur_sched)
    actual = station_info[0].get("number")
    self.assertEqual(expected, actual)
  
  def test_route_info(self):
    expected = "BALB"
    station_info = self.bart.route_info("6", self.cur_sched, "today")
    actual = station_info.get('config')[1]
    self.assertEqual(expected, actual)
  
  def test_get_holidays(self):
    expected = "Day"
    # They all in "Day"
    actual = self.bart.get_holidays()[1].get('name')[-3:]
    self.assertEqual(expected, actual)

  def test_get_special_schedules(self):
    expected = 5
    # Example: 'routes_affected': 'ROUTE 3, ROUTE 4, ROUTE 5, ROUTE 6'
    actual = len(self.bart.get_special_schedules().get('routes_affected'))
    self.assertLess(expected, actual)

  def test_get_station_schedule(self):
    expected = "ROUTE 7"
    actual = self.bart.get_station_schedule("12th")[0].get("line")
    self.assertEqual(expected, actual)

  def test_get_route_schedule(self):
    expected = "6:13 AM"
    actual = self.bart.get_route_schedule("6").get("1").get("DALY").get("orig_time")
    self.assertEqual(expected, actual)

  def test_get_fare(self):
    expected = "3.15"
    actual = self.bart.get_fare("12th", "embr").get("fare")
    self.assertLess(expected, actual)

if __name__ == '__main__':
  unittest.main()
