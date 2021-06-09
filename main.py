from car_manager import CarManager

if __name__ == '__main__':
    # car_manager = CarManager(socket_host='192.168.1.104', debug=True)
    car_manager = CarManager(socket_host='172.18.22.12', debug=True)
    car_manager.run()
