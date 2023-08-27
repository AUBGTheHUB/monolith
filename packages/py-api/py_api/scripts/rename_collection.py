#!/usr/bin/env python
from py_api.database import db


def rename_collection() -> None:
    col_name = input(
        "What's the current name of the collection you want to rename: ",
    )
    new_col_name = input("What do you want to rename the collection to: ")

    try:
        col = db[col_name]
        col.rename(new_col_name)
    except:
        print("\nNo such collection was found!")

    print("\nRenaming was successful!")


if __name__ == "__main__":
    rename_collection()
