import csv

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        if brand and photo_file_name and carrying:
            self.brand = brand
            self.carrying = float(carrying)
            tmp = photo_file_name.split('.')
            if len(tmp) > 1:
                self.photo_file_name = tmp[-1]
            else:
                 raise RuntimeError    
        else:
            raise RuntimeError

    def get_photo_file_ext(self):
        return self.photo_file_name


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            whl = body_whl.split('x')
            self.body_width = float(whl[0])
            self.body_height = float(whl[1])
            self.body_length = float(whl[2])
        except:
            self.body_width = self.body_height = self.body_length = 0

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        if extra:
            self.extra = extra
        else:
            raise RuntimeError

def get_class(inf, car_list):
    try:
        tmp = None
        if inf[0] == 'car':
            tmp = Car(inf[1], inf[3], inf[5], inf[2])
        elif inf[0] == 'truck':
            tmp = Truck(inf[1], inf[3], inf[5], inf[4])
        elif inf[0] == 'spec_machine':
            tmp = SpecMachine(inf[1], inf[3], inf[5], inf[6])
    except:
        print("ENODATA")
    else:
        car_list.append(tmp)
        
def get_car_list(csv_filename):
    car_list = []
    try:
        with open(csv_filename) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                if len(row) == 7:
                    tmp = get_class(row, car_list)
    except:
        print("No file in the directory")
    return car_list


my = get_car_list('test.csv')


