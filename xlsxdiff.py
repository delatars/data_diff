import gspread
import pandas

from abc import ABCMeta, abstractmethod


class BaseLoader(metaclass=ABCMeta):

    @property
    @abstractmethod
    def sheet_names(self): ...

    @abstractmethod
    def load(self, page_name): ...

    @abstractmethod
    def delete(self, page_name, start_index, end_index=None): ...

    @abstractmethod
    def update(self, page_name, dataframe): ...

    @abstractmethod
    def close(self): ...


class Excell(BaseLoader):

    def __init__(self, filepath):
        self.filepath = filepath
        self.excel = pandas.ExcelFile(self.filepath)

    @property
    def sheet_names(self):
        return self.excel.sheet_names

    def load(self, page_name):
        return self.excel.parse(page_name)

    def delete(self, page_name, start_index, end_index=None):
        raise NotImplementedError

    def update(self, page_name, dataframe):
        raise NotImplementedError

    def close(self):
        self.excel.close()


class Gsheet(BaseLoader):

    def __init__(self, sheetname):
        gc = gspread.oauth()
        self.workbook = gc.open(sheetname)

    @property
    def sheet_names(self):
        return self.workbook.worksheets()

    def load(self, page_name):
        sheet = self.workbook.worksheet(page_name)
        return pandas.DataFrame(sheet.get_all_records())

    def delete(self, page_name, start_index, end_index=None):
        sheet = self.workbook.worksheet(page_name)
        sheet.delete_rows(start_index, end_index=end_index)

    def update(self, page_name, dataframe):
        sheet = self.workbook.worksheet(page_name)
        sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

    def close(self):
        pass


class FileDiff:

    def __init__(self, xls, gsheet, update_priority="cloud"):
        self.xls = xls
        self.gsheet = gsheet
        self.working_pages = self._check_pages()

        if update_priority not in ["cloud", "local"]:
            update_priority = "cloud"
        self.update_priority = update_priority

        self._differences = None

    def __del__(self):
        self.xls.close()
        self.gsheet.close()

    def get_update_rows(self, pagename):
        if self._differences is None:
            self._differences = self._get_differences(pagename)
        difs = self._differences[self._differences['_merge'] == 'left_only']
        difs.drop('_merge', axis=1)
        return difs

    def get_remove_rows(self, pagename):
        if self._differences is None:
            self._differences = self._get_differences(pagename)
        difs = self._differences[self._differences['_merge'] == 'right_only']
        difs.drop('_merge', axis=1)
        return difs

    def show_differences(self, pagename):
        print(f"Gh")
        print(self.get_update_rows(pagename))

    def _check_pages(self):
        working_pages = []
        for pagename in self.xls.sheet_names:
            if pagename in self.gsheet.sheet_names:
                working_pages.append(pagename)
        return working_pages

    def _get_differences(self, pagename):
        xls = self.xls.load(pagename)
        gsheet = self.gsheet.load(pagename)
        if self.update_priority == "cloud":
            return xls.merge(gsheet, indicator=True, how='outer')
        else:
            return gsheet.merge(xls, indicator=True, how='outer')


filediff = FileDiff(Excell("data.xlsx"), Gsheet("data2"))

