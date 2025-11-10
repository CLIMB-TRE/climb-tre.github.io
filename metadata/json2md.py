#!/usr/bin/env python3

import csv
import sys
import json
from typing import Any
from enum import Enum
from argparse import ArgumentParser


class Commands(Enum):
    UPLOADER = "uploader"
    ANALYSIS = "analysis"
    TEMPLATE = "template"


def uploader_spec(
    fields: dict[str, Any], prefix: str = ""
) -> tuple[list[list[str]], dict[str, list[list[str]]], list[list[str]]]:
    required = []
    at_least_one_required = {}
    optional = []

    for field, info in fields.items():
        if "add" not in info["actions"]:
            continue

        restrictions = []
        at_least_one_required_keys = []

        if info.get("default") is not None:
            restrictions.append("• Default: " + f"`{info['default']}`")

        if info.get("restrictions"):
            for restriction in info["restrictions"]:
                condition, _, value = restriction.partition(": ")

                if "at least one required" in condition.lower():
                    at_least_one_required_keys.append(
                        tuple(
                            sorted(
                                [x.strip() for x in value.strip().split(",")],
                                key=str.lower,
                            )
                        )
                    )
                elif "required when" in condition.lower():
                    statement = condition.split()
                    statement[2] = f"`{statement[2]}`"
                    condition = " ".join(statement)
                    restrictions.append("• " + ": ".join([condition, f"`{value}`"]))
                elif "input formats" in condition.lower():
                    restrictions.append(
                        "• "
                        + ": ".join(
                            [
                                condition,
                                ", ".join(
                                    [f"`{val.strip()}`" for val in value.split(",")]
                                ),
                            ]
                        )
                    )
                else:
                    restrictions.append("• " + ": ".join([condition, f"`{value}`"]))

        if info.get("values"):
            if len(info["values"]) > 20:
                restrictions.append(
                    "• Choices: "
                    + ", ".join([f"`{val}`" for val in info["values"][:20]])
                    + ", ..."
                )
            else:
                restrictions.append(
                    "• Choices: " + ", ".join([f"`{val}`" for val in info["values"]])
                )

        row = [
            f"`{prefix}{field}`",
            f"`{info['type']}`",
            info["description"],
            "<br>".join(restrictions),
        ]

        if info["required"]:
            required.append(row)
        elif at_least_one_required_keys:
            for key in at_least_one_required_keys:
                at_least_one_required.setdefault(key, []).append(row)
        else:
            optional.append(row)

        if info["type"] == "relation":
            relation_required, relation_at_least_one_required, relation_optional = (
                uploader_spec(info["fields"], prefix=field + ".")
            )
            required.extend(relation_required)
            for k, v in relation_at_least_one_required.items():
                at_least_one_required.setdefault(k, []).extend(v)
            optional.extend(relation_optional)

    return required, at_least_one_required, optional


def analysis_spec(fields: dict[str, Any], prefix: str = "") -> list[list[str]]:
    spec = []

    for field, info in fields.items():
        restrictions = []

        if info.get("restrictions"):
            for restriction in info["restrictions"]:
                condition, _, value = restriction.partition(": ")
                if (
                    "output format" in condition.lower()
                    or "array type" in condition.lower()
                ):
                    restrictions.append("• " + ": ".join([condition, f"`{value}`"]))

        if info.get("values"):
            if len(info["values"]) > 20:
                restrictions.append(
                    "• Choices: "
                    + ", ".join([f"`{val}`" for val in info["values"][:20]])
                    + ", ..."
                )
            else:
                restrictions.append(
                    "• Choices: " + ", ".join([f"`{val}`" for val in info["values"]])
                )

        row = [
            f"`{prefix}{field}`",
            f"`{info['type']}`",
            str(info["description"]) if info.get("description") else "",
            "<br>".join(restrictions),
        ]

        spec.append(row)

        if info["type"] == "relation":
            relation_spec = analysis_spec(info["fields"], prefix=field + ".")
            spec.extend(relation_spec)

    return spec


def generate_table(columns: list[str], rows: list[list[str]]) -> str:
    table = [
        columns,
        ["-----"] * len(columns),
    ] + rows
    return "".join(["| " + " | ".join(row) + " |\n" for row in table])


def generate_tables(columns: list[str], rows: list[list[str]], depth: int = 1) -> str:
    markdown = ""

    fields = []
    relations = {}
    relation_fields = {}

    # Identify relations
    for row in rows:
        if row[1] == "`relation`":
            relations[row[0].strip("`")] = row
            relation_fields[row[0].strip("`")] = []

    # Group fields under their relations
    for row in rows:
        for relation in relations:
            if row[0].startswith(f"`{relation}."):
                relation_fields[relation].append(row)
                break
            elif row[0] == f"`{relation}`":
                # Skip the relation itself
                break
        else:
            fields.append(row)

    markdown += f"{'#' * depth}# Fields\n\n"
    markdown += generate_table(columns=columns, rows=fields) + "\n\n"

    if relations:
        markdown += f"{'#' * depth}# Relations\n\n"
        for relation, relation_fields in relation_fields.items():
            markdown += f"{'#' * depth}## `{relation}`\n\n"
            markdown += relations[relation][2] + "\n\n"

            markdown += generate_table(columns=columns, rows=relation_fields) + "\n\n"

    return markdown


def generate_section(row: list[str], depth: int = 1) -> str:
    lines = [f"{'#' * (depth)}# {row[0]}", row[2], f"**Type:** {row[1]}"]

    if row[3].strip():
        lines.extend(["**Restrictions:**", row[3]])

    return "\n\n".join(lines) + "\n\n"


def generate_sections(rows: list[list[str]], depth: int = 1) -> str:
    markdown = ""

    fields = []
    relations = {}
    relation_fields = {}

    # Identify relations
    for row in rows:
        if row[1] == "`relation`":
            relations[row[0].strip("`")] = row
            relation_fields[row[0].strip("`")] = []

    # Group fields under their relations
    for row in rows:
        for relation in relations:
            if row[0].startswith(f"`{relation}."):
                relation_fields[relation].append(row)
                break
            elif row[0] == f"`{relation}`":
                # Skip the relation itself
                break
        else:
            fields.append(row)

    for row in fields:
        markdown += generate_section(row, depth=depth)

    for relation, relation_fields in relation_fields.items():
        markdown += f"{'#' * depth}# `{relation}`\n\n"
        markdown += relations[relation][2] + "\n\n"

        for row in relation_fields:
            markdown += generate_section(row, depth=depth + 1)

    return markdown


def main():
    parser = ArgumentParser()
    command = parser.add_subparsers(dest="command", required=True)
    parser.add_argument(
        "-t",
        "--title",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=1,
        help="header depth of title (default=1)",
    )
    uploader_parser = command.add_parser(
        Commands.UPLOADER.value,
        help="Generate uploader field documentation in Markdown format",
    )
    uploader_parser.add_argument(
        "json_filename",
        type=str,
    )
    analysis_parser = command.add_parser(
        Commands.ANALYSIS.value,
        help="Generate analysis field documentation in Markdown format",
    )
    analysis_parser.add_argument(
        "json_filename",
        type=str,
    )
    template_parser = command.add_parser(
        Commands.TEMPLATE.value,
        help="Generate a CSV template for the uploader",
    )
    template_parser.add_argument(
        "json_filename",
        type=str,
    )

    args = parser.parse_args()

    with open(args.json_filename, "r") as f:
        j = json.load(f)

    if args.title:
        print("#" * args.depth + " " + args.title)
        print()

    if args.command == Commands.UPLOADER.value:
        columns = [
            "Field" + "&nbsp;" * 40,
            "Data type",
            "Description",
            "Restrictions",
        ]

        required, at_least_one_required, optional = uploader_spec(j["fields"])

        print("#" * args.depth + "# Required fields\n")
        print(generate_table(columns=columns, rows=required))

        for _, table in at_least_one_required.items():
            print("At least one of the following fields are required:\n")
            print(generate_table(columns=columns, rows=table))

        print("#" * args.depth + "# Optional fields\n")
        print(generate_table(columns=columns, rows=optional))

    elif args.command == Commands.ANALYSIS.value:
        columns = [
            "Field" + "&nbsp;" * 40,
            "Data type",
            "Description",
            "Restrictions",
        ]
        spec = analysis_spec(j["fields"])
        print(generate_tables(columns=columns, rows=spec, depth=args.depth))

    elif args.command == Commands.TEMPLATE.value:
        template_fields = [
            field for field in j["fields"] if "add" in j["fields"][field]["actions"]
        ]
        writer = csv.writer(sys.stdout)
        writer.writerow(template_fields)
        writer.writerow([])


if __name__ == "__main__":
    main()
