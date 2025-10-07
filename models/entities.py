
# Flight class - update to match database schema
class FlightInfo:

  def __init__(self):
    self.flightID = 0
    self.flightOrigin = ''
    self.flightDestination = ''
    self.status = ''

  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_origin(self, flightOrigin):
    self.flight_origin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flight_destination = flightDestination

  def set_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flight_origin(self):
    return self.flightOrigin

  def get_flight_destination(self):
    return self.flightDestination

  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)

# Pilot class 

# Destination class
