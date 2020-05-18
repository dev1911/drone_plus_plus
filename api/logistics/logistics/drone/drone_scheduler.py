from math import radians , sin , cos , acos
from .models import Drone
def distance(src_lat , src_long , dest_lat , dest_long):
	"""
	Returns distance between two cordinates in kms
	Parameters:
	src_lat   : float : Source latitude
	src_long  : float : Source longitude
	dest_lat  : float : Destination latitude
	dest_long : float : Destination longitude

	Returns:
	float : distance between two cordinates
	"""
	slat = radians(src_lat)
	slong = radians(src_long)
	dlat = radians(dest_lat)
	dlong = radians(dest_long)

	dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
	return dist

def check_battery(drone , dest_lat , dest_long):
	"""
	Checks whether drone has sufficient battery life to service an order
	Parameters:
	drone      : Type Drone : Drone object
	dest_lat   : float      : Latitude of the destination
	dest_long  : float      : Longitude of the destination

	Returns:
	boolean : True if the drone can reach the destination
			  False if the drone cannot reach the destination
	"""
	#Battery should be sufficient to cover twice the distance between warehouse and destination
	if drone.status == "Charging":
		if drone.battery * drone.rate > 2 * dist(drone.latitude,drone.longitude,dest_lat,dest_long):
			return True
		else:
			return False	
#Battery should be more than the sum of distance between current location and warehouse + 2 * distance betwenn warehouse and destination
	elif drone.status == "Returning":
		if drone.battery * drone.rate > 2 * dist(drone.warehouse.latitude,drone.warehouse.longitude,dest_lat,dest_long) 
										  + dist(drone.latitude , drone.longitude, drone.warehouse.latitude , drone.warehouse.longitude):
			return True
		else:
			return False	


def schedule(request , drones , orders):
	"""
	Schedules drones and assigns them to orders.
	drones : A list of all drone objects
	orders : A list of all order objects

	Returns a dictionary of order:drone
	"""
	ongoing_orders = [order for order in orders if order.status == "Ongoing"]
	orders_to_be_serviced = [order for order in orders if order.status == "Pending"]
	idle_drones = [drone for drone in drones if drone.status="Charging"]
	returning_drones = [drone for drone in drones if drone.status="Returning"]

	result = {}
	#for every unserviced order
	for order in orders_to_be_serviced:
		min_dist = 10000000000000000
		min_drone = ""
		
		# for each idle drone
		for idle_drone in idle_drones:
			if idle_drone.warehouse != None:
				dist = distance(idle_drone.warehouse.latitude , idle_drone.warehouse.longitude ,order.latitude , order.longitude)
			if dist < min_dist and check_battery(idle_drone , order.latitude , order.longitude):
				min_dist = dist
				min_drone = idle_drone.drone_id
		if min_drone!="":
			result[order] = min_drone

		# if no idle drone
		if min_drone == "":
			# for each returning drone
			for ret_drone in returning_drones:
				if ret_drone.warehouse != None:
					dist = distance(ret_drone.warehouse.latitude , ret_drone.warehouse.longitude ,order.latitude , order.longitude) + 
							distance(ret_drone.latitude , ret_drone.longitude , ret_drone.warehouse.latitude . ret_drone.warehouse.longitude)
				if dist < min_dist and check_battery(ret_drone , order.latitude , order.longitude):
					min_dist = dist
					min_drone = idle_drone.drone_id
			if min_drone!="":
				result[order] = min_drone
	return result			



# if __name__ == "__main__":
# 	warehouse = []
# 	drones = []
#	 drones.append(Drone(owner="Devansh" , battery=100 , ))