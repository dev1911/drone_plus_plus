# Drone_plus_plus

Drone-based logistics is a very hot topic in research and has the potential to change the future of logistics and e-commerce. The project focuses on providing an interface through which a logistics operator can track the drones in motion. The proposed system is a Web App through which customers can place orders. Once an order is placed, the route planning algorithm will select a drone to service the needs based on factors like distance, battery level left, nearest charging station, etc. Through a map, the operator can track the real-time location of the drones in motion. The operator can see visualizations based on statistics of each drone, such as time spent flying. As an extra feature, we also intend to consider the altitude of obstacles in the path, like buildings, trees, etc. 

Features:
1. Optimizing the time required for an order to be serviced by graph theory algorithms.
2. Real-time tracking of drones.
3. Interactive visualizations of the status of drones.
4. Placing an order to be serviced by drones.


The application uses a microservice architecture with three main services:
* User :- Used for registering new users,authentication purposes,login,logout and getting user details.
* Order :- Used for creating new orders.
* Logistics :- Main Purpose of this service is scheduling of drones according to the location of order and warehouse.

For the purpose of communication between the frontend(client) and the services(server),we have an API Gateway.Since it's a microservice architecture the three services have independent databases.Websockets are used for real time updates to be shown from the server to the client.

The Technology Stack used in the application is:
1. Frontend : Angular 8
2. User,Order,Logistics Service and API Gateway : Django Rest Framework
3. Deployment : Kubernetes

Redis is used for showing real time tracking of drones to the frontend.

The code structure is as follows:
* api
  1. user (user service)
  2. order (order service)
  3. logistics (logistics service)
  4. gateway (API Gateway)
* frontend
    1. drone_plus_plus (frontend code)
* deployments
    1. user (user deployments)
    2. order (order deployments)
    3. logistics(logistics deployments)
    4. gateway (gateway deployments)
  
Databases:
* User Service : Postgres
* Order Service : MySQL
* Logistics Service : Postgres
 
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/architecture-diag.jpg" height="600" width="800">
