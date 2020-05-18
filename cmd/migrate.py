import os

def main():
	print("------------------------USER SERVICE-------------------------------------------")
	os.system("kubectl exec -it deployments/user-deployment python user/manage.py migrate")
	print("------------------------ORDER SERVICE------------------------------------------")
	os.system("kubectl exec -it deployments/order-deployment python order/manage.py migrate")
	print("------------------------LOGISTICS SERVICE--------------------------------------")
	os.system("kubectl exec -it deployments/logistics-deployment python logistics/manage.py migrate")

if __name__ == "__main__":
	main()