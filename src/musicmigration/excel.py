import pandas as pd
from types import TracebackType


class Excel:
    def __init__(self, input_path="./input.xlsx", output_path="./output.xlsx"):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    def __enter__(self):
        self.read()
        return self

    def __exit__(
            self,
            type_: type[BaseException] | None,
            value: BaseException | None,
            traceback: TracebackType | None,
    ) -> bool | None:
        # fancy annotation from https://stackoverflow.com/questions/58808055/what-are-the-python-builtin-exit-argument-types
        self.write()

    def read(self):
        """
        Reads input Excel file into pandas dataframe
        :return:
        """
        self.df = pd.read_excel(self.input_path, engine="calamine", dtype=str)

    def write(self):
        """
        Writes pandas dataframe to output Excel file
        :return:
        """
        if self.df is not None:
            self.df.to_excel(self.output_path, engine="xlsxwriter", index=False)
