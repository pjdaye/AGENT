import pickle


class ReadWritePickles:
    """Reads and writes pickle files """
    def __init__(self):
        self.__base_path = ''

    @property
    def base_path(self):
        return self.__base_path

    @base_path.setter
    def base_path(self, value):
        self.__base_path = value

    def write(self, file, data):
        pickled_data = pickle.dumps(data)

        with open(f'{self.__base_path}/{file}', 'wb') as file:
            file.write(pickled_data)

    def read(self, file):
        with open(f'{self.__base_path}/{file}', 'rb') as file:
            return pickle.loads(file.read())
