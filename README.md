# Drone_plus_plus

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

Architecture Diagram
 
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/architecture.jpg" height="600" width="800">

Screenshots of the Application

<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/3.png" height="800" width="600">
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/4.png" height="800" width="600">
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/5.png" height="800" width="600">
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/7.png" height="800" width="600">
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/2.png" height="800" width="600">
<img src = "https://github.com/dev1911/drone_plus_plus/blob/documentation/docs/6.png" height="800" width="600">
