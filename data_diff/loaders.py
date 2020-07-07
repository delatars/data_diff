import pandas
import gspread
import shutil
from urllib.parse import urlparse
from pathlib import Path
from data_diff.bases import BaseLoader, BaseGroupLoaders


__ALL__ = ("DetermineLoader", )


class Excell(BaseLoader):

    name = "Excell"
    schemes = (".xls", ".xlsx")
    uri_example = "file://file{scheme} or ~/file{scheme}"

    def __init__(self, filepath):
        self.filepath = filepath
        self.excel = pandas.ExcelFile(self.filepath)
        self.current_page = None
        self._current_page = iter(self.excel.sheet_names)

    def __next__(self):
        self.current_page = next(self._current_page)
        dataframe = self.excel.parse(self.current_page)
        dataframe = dataframe.astype("object")
        return dataframe

    def delete(self, dataframe):
        raise NotImplementedError

    def update(self, dataframe):
        raise NotImplementedError

    def close(self):
        self.excel.close()


class Gsheet(BaseLoader):

    name = "Google Sheet"
    schemes = ("docs.google.com",)
    uri_example = "https://{scheme}/spreadsheet/ccc?key=0Bm...FE&hl"

    sa_path = Path("~/.config/gspread/service_account.json")
    oauth_path = Path("~/.config/gspread/credentials.json")

    def __init__(self, url):
        gc = self._auth()
        self.workbook = gc.open_by_url(url)
        self.current_page = None
        self.current_page_len = None
        self._current_page = iter(self.workbook.worksheets())

    def _auth(self):
        if self.sa_path.expanduser().exists():
            auth = gspread.service_account()
            return auth
        elif self.oauth_path.expanduser().exists():
            auth = gspread.oauth()
            return auth
        else:
            path = base_path = Path("")
            while 1:
                choice = input(f"{self.name} choose authentication type:\n 1) oauth\n 2) system account\n$>")
                if choice == "1":
                    path = base_path = self.oauth_path
                    break
                elif choice == "2":
                    path = base_path = self.sa_path
                    break
                else:
                    print("Wrong answer: (1 or 2)?")
                    continue
            while 1:
                if path.expanduser().exists():
                    break
                else:
                    print(f"Can't access: {path}")
                    path = Path(input(f"Enter path to: {base_path.name}\n$>"))
            shutil.copy(str(path.expanduser()), str(base_path.expanduser()))
            self._auth()

    def __next__(self):
        self.current_page = next(self._current_page)
        dataframe = pandas.DataFrame(self.current_page.get_all_records())
        dataframe = dataframe.astype("object")
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


class FileGroupLoaders(BaseGroupLoaders):
    schemes = ("file", "")
    group_name = "File Loaders"
    loaders = (
        Excell,
    )

    def get_loader(self):
        path = Path(self.uri.path)
        loader = None
        for _loader in self.loaders:
            if path.suffix in _loader.schemes:
                loader = _loader
                break
        if loader is None:
            raise NotImplementedError(f"Loader not implemented for extension: {path.suffix}")
        return loader(self.uri.path)


class WebGroupLoaders(BaseGroupLoaders, ):
    schemes = ("https", "http")
    group_name = "Web Loaders"
    loaders = (
        Gsheet,
    )

    def get_loader(self):
        loader = None
        for _loader in self.loaders:
            if self.uri.netloc in _loader.schemes:
                loader = _loader
                break
        if loader is None:
            raise NotImplementedError(f"Loader not implemented for network location: {self.uri.netloc}")
        return loader(self.uri.geturl())


class DetermineLoader:

    LOADER_GROUPS = (
        FileGroupLoaders,
        WebGroupLoaders,
    )

    def __init__(self, uri):
        self.uri = urlparse(uri)

    def get_loader(self):
        group_loader = None
        for l_group in self.LOADER_GROUPS:
            if self.uri.scheme in l_group.schemes:
                group_loader = l_group
                break
        if group_loader is None:
            raise NotImplementedError(f"Loader's group not implemented for scheme: {self.uri.scheme}")

        return group_loader(self.uri).get_loader()
