import argparse
import json
import os
import tempfile

# Создаём временное хранилище
storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

def get_map():
    """ Считываем данные из файла и возвращаем словарь """

    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as f:
        tmp = f.read()
        if tmp:
            return json.loads(tmp)
        return {}

def set_value(key, value):
    data = get_map()
    if key in data:
        data[key].append(value)
    else:
        data[key] = [value]

    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))

def print_value(key):
    data = get_map()
    if key in data:
        print(", ".join(data.get(key)))
    else:
        print(None)

if __name__ == '__main__':
    # Собираем параметры из строки
    parser = argparse.ArgumentParser(description='Save to dict')
    parser.add_argument('--key', type=str, default=None, help='Add or see value to the map')
    parser.add_argument('--val', type=str, default=None, help='Add value')
    args = parser.parse_args()

    if args.key and args.val:
        set_value(args.key, args.val)
    elif args.key and not args.val:
        print_value(args.key)
    elif not args.key and not args.val:
        print(None)
    else:
        print("Wrong command!")