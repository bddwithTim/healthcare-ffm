import os
import copy
import pandas as pd

from typing import List
from enum import Enum
from pathlib import Path

root_dir = Path(__file__).parents[1]


class MergeStrategy(Enum):
    DeleteKey = 0


def deep_merge_dict(base: dict, addition: dict) -> dict:
    """
    Recursively merge dictionaries.

    Values in `addition` can be set to a variant of `MergeStrategy`
    to induce special behavior.
    """
    base = copy.deepcopy(base)

    for key, value in addition.items():
        if value == MergeStrategy.DeleteKey:
            base.pop(key, None)
        elif isinstance(value, dict) and key in base and isinstance(base[key], dict):
            base[key] = deep_merge_dict(base.get(key, {}), value)
        else:
            base[key] = addition[key]
    return base


def get_file_path(file_name):
    for root, dirs, files in os.walk(root_dir, topdown=True):
        for name in files:
            if name == file_name:
                return os.path.join(root, name)
    raise FileNotFoundError("File not found")


def read_xls(file_name: str, sheet_name: str = 'Sheet1', parse: bool = True):
    """
    Get excel data
    :param sheet_name:
    :param file_name:
    :param parse:
    :return parsed excel:
    """
    fp = get_file_path(file_name)
    xl = pd.read_excel(io=fp, sheet_name=sheet_name)
    df = pd.DataFrame(xl)

    if not parse:
        return df
    values = []
    for row in df.iterrows():
        row = list(row)
        row[1] = [str(item).strip() for item in row[1]]
        row[1] = [str(item).replace("/", "-") for item in row[1]]
        # row[1] = [str(item).replace("\t", "") for item in row[1]]
        row[1] = [str(item).replace(":", "") for item in row[1]]
        items = [n for n in row[1]]
        values.append(tuple(items))
    return values


def generate_excel_result(data: List, zip_code: str):
    # convert into dataframe
    df = pd.DataFrame(data=data)
    # convert into excel
    df.to_excel(f"{root_dir}/tests/results/healthcare-plans-{zip_code}.xlsx", index=False)


def generate_medicare_result(data: List, zip_code: str):
    # convert into dataframe
    df = pd.DataFrame(data=data)
    # convert into excel
    df.to_excel(f"{root_dir}/tests/results/medicare-plans-{zip_code}.xlsx", index=False)
