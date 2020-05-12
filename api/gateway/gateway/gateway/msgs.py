import os

TOKEN = "this_is_token"

# user_service = "http://127.0.0.1:8001/"
# logistic_service = "http://127.0.0.1:8002/"
# order_service = "http://127.0.0.1:8003/"

user_service_host = os.getenv("USER_SERVICE_SERVICE_HOST","127.0.0.1")
logistic_service_host = os.getenv("LOGISTIC_SERVICE_SERVICE_HOST" , "127.0.0.1")
order_service_host = os.getenv("ORDER_SERVICE_SERVICE_HOST" , "127.0.0.1")

user_service_port = os.getenv("USER_SERVICE_SERVICE_PORT" , "9000")
logistic_service_port = os.getenv("LOGISTIC_SERVICE_SERVICE_PORT" , "9000")
order_service_port = os.getenv("ORDER_SERVICE_SERVICE_PORT" , "9000")

user_service = user_service_host + ":" + user_service_port + "/"
logistic_service = logistic_service_host + ":" + logistic_service_port + "/"
order_service = order_service_host + ":" + order_service_port + "/"

token_error = "User is not authenticated"
