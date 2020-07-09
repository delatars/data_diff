from pandas import DataFrame
from typing import Iterable

from data_diff.bases import BaseLoader


class FakeLoader(BaseLoader):

    name = "Fake Loader"
    schemes = ("fake", )
    uri_example = "fake://{scheme}"

    def __init__(self, data: Iterable):
        self.current_frame = None
        self._frames = iter(data)

    def __next__(self) -> DataFrame:
        self.current_frame = next(self._frames)
        return DataFrame(self.current_frame)

    def delete(self, dataframe: DataFrame):
        for line in dataframe["_lineno"]:
            for col in self.current_frame.keys():
                del self.current_frame[col][int(line)-2]

    def update(self, dataframe: DataFrame):
        dataframe.drop('_lineno', axis=1, inplace=True)
        for col in dataframe.columns.values.tolist():
            for val in dataframe[col]:
                self.current_frame[col].append(val)

    def close(self):
        pass
