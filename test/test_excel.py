# run with 'uv run --env-file local.env pytest'
# or for coverage 'uv run --env-file local.env coverage run -m pytest' then 'uv run coverage report -m'
import pytest
import os
from musicmigration import excel

class TestExcel:
    def test_context_manager_works(self, tmpdir ):
        t = tmpdir.join("done.xlsx")
        with excel.Excel("./test/data/input.xlsx", t):
            pass