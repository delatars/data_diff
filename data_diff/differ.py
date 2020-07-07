from pandas.errors import MergeError


class Differ:

    def __init__(self, from_loader, to_loader):
        self.from_loader = from_loader
        self.to_loader = to_loader
        self._differences = self._get_differences()

    def __del__(self):
        self.from_loader.close()
        self.to_loader.close()

    def manual_differences(self):

        from_l_name = self.from_loader.name
        to_l_name = self.to_loader.name

        print(f"Differences: {from_l_name} --> {to_l_name}")

        for index, data in enumerate(self._differences):

            append_rows = self._get_changes(data, 'left_only')
            delete_rows = self._get_changes(data, 'right_only')

            print(f"\n---- Data portion: {index+1} ----\n")

            if not append_rows.empty or not delete_rows.empty:
                if not append_rows.empty:
                    print(f"Will be appended to: {to_l_name}")
                    print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print(append_rows)
                    print("-----")

                if not delete_rows.empty:
                    print(f"Will be deleted from: {to_l_name}")
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<-")
                    print(delete_rows)

                while 1:
                    choice = input(f"Do you want to update: {to_l_name} (y/n)?\n$>")
                    if choice.lower() == "y":
                        if not delete_rows.empty:
                            self.to_loader.delete(delete_rows)
                        if not append_rows.empty:
                            self.to_loader.update(append_rows)
                        break
                    elif choice.lower() == "n":
                        break
                    else:
                        print("Wrong answer: ('y' or 'n')?")
                        continue
            else:
                print("->>> No differences <<<-")

    def auto_differences(self):

        for index, data in enumerate(self._differences):

            append_rows = self._get_changes(data, 'left_only')
            delete_rows = self._get_changes(data, 'right_only')

            if not delete_rows.empty:
                self.to_loader.delete(delete_rows)

            if not append_rows.empty:
                self.to_loader.update(append_rows)

    def _get_changes(self, data, merge):
        return data[data['_merge'] == merge].drop('_merge', axis=1)

    def _get_differences(self):
        for from_l, to_l in zip(self.from_loader, self.to_loader):
            # pass if headers not compared
            if not from_l.columns.symmetric_difference(to_l.columns).empty:
                continue
            try:
                # first line is headers, start from 2
                to_l["_lineno"] = [i for i in range(2, len(to_l)+2)]
                yield from_l.merge(to_l, indicator=True, how='outer')
            except MergeError:
                continue


if __name__ == '__main__':
    pass
