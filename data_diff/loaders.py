import pandas
import gspread
from abc import ABCMeta, abstractmethod


__ALL__ = ("Excell", "Gsheet",)


class BaseLoader(metaclass=ABCMeta):

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


class Excell(BaseLoader):

    def __init__(self, filepath):
        self.filepath = filepath
        self.excel = pandas.ExcelFile(self.filepath)
        self.current_page = None
        self._current_page = iter(self.excel.sheet_names)

    def __next__(self):
        self.current_page = next(self._current_page)
        return self.excel.parse(self.current_page)

    def delete(self, dataframe):
        raise NotImplementedError

    def update(self, dataframe):
        raise NotImplementedError

    def close(self):
        self.excel.close()


class Gsheet(BaseLoader):

    def __init__(self, sheetname):
        gc = gspread.oauth()
        self.workbook = gc.open(sheetname)
        self.current_page = None
        self.current_page_len = None
        self._current_page = iter(self.workbook.worksheets())

    def __next__(self):
        self.current_page = next(self._current_page)
        dataframe = pandas.DataFrame(self.current_page.get_all_records())
        self.current_page_len = len(dataframe)+1
        return dataframe

    def delete(self, dataframe):
        for line in dataframe["_lineno"]:
            self.current_page.delete_rows(int(line))
            self.current_page_len -= 1

    def update(self, dataframe):
        dataframe.drop('_lineno', axis=1, inplace=True)
        self.current_page.update(f"A{self.current_page_len+1}", dataframe.values.tolist())
        self.current_page_len += len(dataframe)

    def close(self):
        pass
