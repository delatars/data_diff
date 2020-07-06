from abc import ABCMeta, abstractmethod


class BaseLoader(metaclass=ABCMeta):

    @property
    @abstractmethod
    def schemes(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self): ...

    def load(self):
        return self.__next__()

    @abstractmethod
    def delete(self, dataframe): ...

    @abstractmethod
    def update(self, dataframe): ...

    @abstractmethod
    def close(self): ...


class BaseGroupLoaders(metaclass=ABCMeta):

    def __init__(self, uri):
        self.uri = uri

    @property
    @abstractmethod
    def loaders(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def schemes(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def group_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_loader(self): ...
