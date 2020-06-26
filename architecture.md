<div class="topnav">
  <a href="index.html">Home</a>
  <a href="demo.html">Demo of Application</a>
  <a href="developers.html">Developers</a>
</div>

## Architecture
The application uses a microservice architecture with three main services:
* User :- Used for registering new users,authentication purposes,login,logout and getting user details.
* Order :- Used for creating new orders.
* Logistics :- Main Purpose of this service is scheduling of drones according to the location of order and warehouse.

For the purpose of communication between the frontend(client) and the services(server),we have an API Gateway.Since it's a microservice architecture the three services have independent databases.Websockets are used for real time updates to be shown from the server to the client.
![Image Description](https://github.com/dev1911/drone_plus_plus/blob/gh-pages/docs/architecture-diag.jpg?raw=True)
