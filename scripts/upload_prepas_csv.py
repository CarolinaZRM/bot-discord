"""
//  bot-discord/scripts/upload_prepas_csv.py
//  py-bot-uprm
//
//  Created by Gabriel S Santiago on 2022/08/10
//
//  Last Modified: Wednesday, 10th August 2022 10:47:22 am
//  Modified By: Gabriel S Santiago (gabriel.santiago16@upr.edu)
//
//  Copyright © 2022 agSant01. All rights reserved.
//  Copyright © 2022 teamMADE. All rights reserved.


Este es un script creado para upload la información
de los prepas para el signin al bot y no tener la info de nombres
y correos electrónicos en el repositorio.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Collection, Dict, List, Literal

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# import after so the config can use the top level project directory
import config  # noqa: E402


def build_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--file",
        help="CSV File para subir a la DB establecida en .env",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "-c",
        "--collection",
        type=str,
        default="prepas",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        choices=["csv", "json"],
        nargs="+",
        help="Formato que desea exportar el input",
    )

    parser.add_argument(
        "--production",
        action="store_true",
        help="Procesa file, pero no envía a db. Default es FALSO",
    )

    return parser.parse_args(args)


def create_out_files(
    out_formats: Literal["json", "csv"],
    prepas_dict_list: List[Dict[str, str]],
    fieldnames: Collection,
):
    print("\n> Exported files...")
    if "json" in out_formats:
        with open("inserted-data.json", "w") as prepas_json:
            json.dump(prepas_dict_list, prepas_json)
        print(f"> JSON: {Path(prepas_json.name).absolute()}")
    if "csv" in out_formats:
        with open("inserted-data.csv", "w") as prepas_csv:
            writer = csv.DictWriter(
                prepas_csv,
                fieldnames=fieldnames,
            )
            writer.writeheader()
            writer.writerows(prepas_dict_list)
        print(f"> CSV: {Path(prepas_csv.name).absolute()}")


def insert_into_db(
    database_collection: str,
    prepas_dict_list: List[Dict[str, str]],
):
    from db import close_db, get_database

    try:
        collection = get_database().get_collection(database_collection)

        # for prepa in prepas_dict:
        collection.insert_many(prepas_dict_list)
    except Exception as e:
        print(e)
    finally:
        close_db()


def main():
    arguments = build_args()

    input_file: Path = arguments.file

    if input_file.suffix != ".csv":
        raise Exception("Input file must be a CSV file.")

    print(f'\n> Connection string:\n\n>>"{config.MONGO_CONNECTION_STRING}"<<\n')

    with open(input_file.absolute()) as prepa_file:
        prepas_csv_rows = csv.DictReader(prepa_file.readlines())
    prepas_dict_list = list(prepas_csv_rows)

    print(
        f'> DB: Database "{config.MONGO_DB}" | Collection: "{arguments.collection}"...'
    )
    if arguments.production is True:
        print(f"> DB: Connecting to: {config.MONGO_CONNECTION_STRING}...")
        print("> DB: Uploading prepa info...")
        insert_into_db(arguments.collection, prepas_dict_list)
        print("> DB: Success uploading prepa info...")
    else:
        print("> DB: DEBUG Mode. Not connecting to DB")

    if arguments.out:
        create_out_files(
            out_formats=arguments.out,
            prepas_dict_list=prepas_dict_list,
            fieldnames=prepas_csv_rows.fieldnames,
        )

    print("Exit: 0")


if __name__ == "__main__":
    main()
