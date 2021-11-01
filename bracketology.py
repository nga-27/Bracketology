"""bracketology.py

    AI/ML BRACKET GENERATOR - Main file to create autogenerated NCAA Tournament Bracket
"""
from pathlib import Path
import argparse

from libs.bracket.data_framer import (
    dataframe_importer, heuristic_dataframe_importer, import_configuration
)
from libs.bracket.json_converter import convert_from_json_to_bracket_list, generate_json_bracket
from libs.bracket.bracket_builder import build_dag, flat_bracket_creator
from libs.engine.engine import populate_bracket


def bracketology(config_input_path: str):
    """bracketology

    Main function that runs the team picking for the bracket bot

    Args:
        config_input_path (str): path for the user-defined custom picking algorithms, etc.
    """
    print("\r\nStarting...\r\n")

    # Import the user-defined configuration.
    config_path = Path(config_input_path).resolve()
    config_data = import_configuration(config_path)

    attribute_dict = dataframe_importer(config_data)
    heuristic_dict = heuristic_dataframe_importer(config_data)

    # Generate the bracket JSON file with optional attributes
    json_file = generate_json_bracket(
        "bracket_1.csv",
        "bracket_schema.json",
        attribute_dict,
        heuristic_dict
    )

    # Bracket conversion and building
    bracket = convert_from_json_to_bracket_list(json_file)
    flat_bracket = flat_bracket_creator(bracket)
    filled_bracket = populate_bracket(flat_bracket, json_file, config_data)

    # Output the DAG bracket
    build_dag(filled_bracket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Configuration of Bracketology")
    parser.add_argument("--config_input_path", "-c", required=False,
                        default="config/custom/config.json")
    args = parser.parse_args()

    bracketology(**vars(args))
