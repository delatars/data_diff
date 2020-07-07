from abc import ABCMeta, abstractmethod
from pandas import DataFrame
from typing import Tuple


__ALL__ = ("BaseLoader", "BaseGroupLoaders", )


class BaseLoader(metaclass=ABCMeta):
    """ Iterator object which should return Dataframes. """

    @property
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def schemes(cls) -> Tuple:
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def uri_example(cls) -> str:
        raise NotImplementedError

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self) -> DataFrame: ...

    def load(self) -> DataFrame:
        return self.__next__()

    @abstractmethod
    def delete(self, dataframe: DataFrame):
        """

        :type dataframe: pandas.DataFrame with additional column '_lineno'
        _lineno affixed to 'to_loader' before merge
        """

    @abstractmethod
    def update(self, dataframe: DataFrame):
        """

        :type dataframe: pandas.DataFrame with additional column '_lineno'
        _lineno always been NaN
        """

    @abstractmethod
    def close(self): ...


class BaseGroupLoaders(metaclass=ABCMeta):

    def __init__(self, uri):
        self.uri = uri

    @property
    @classmethod
    @abstractmethod
    def loaders(cls) -> Tuple:
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def schemes(cls) -> Tuple:
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def group_name(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_loader(self) -> BaseLoader: ...
