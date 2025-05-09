import glob
import json
import os
from typing import Dict, List, Union

import yaml


def load_jsonl(path: str) -> List[Dict[str, str]]:
    """
    Load a jsonl file.

    Args:
        path (str): path to the jsonl file

    Returns:
        List[Dict[str, str]]: the jsonl file
    """
    with open(path, "r", encoding="utf8") as f:
        return [json.loads(line) for line in f]


def load_txt(path: str) -> List[str]:
    """
    Load a txt file.

    Args:
        path (str): path to the txt file

    Returns:
        List[str]: the txt file
    """
    with open(path, "r", encoding="utf8") as f:
        return f.readlines()


def save_json(path: str, data: dict) -> None:
    """
    Save a json file.

    Args:
        path (str): path to the json file
        data (dict): data to save

    Returns:
        None
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(path: str) -> Union[Dict[str, str], List[Dict[str, str]]]:
    """
    Load a json file.

    Args:
        path (str): path to the json file

    Returns:
        Union[Dict[str, str], List[Dict[str, str]]]: the json file
    """
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def load_yaml(file_path):
    """
    Reads a YAML file and returns its content as a dictionary.

    Parameters:
    file_path (str): The path to the YAML file.

    Returns:
    dict: The content of the YAML file.

    Raises:
    Exception: If there is an error reading or parsing the YAML file.
    """
    with open(file_path, 'r') as file:
        content = yaml.safe_load(file)
        if content is None:
            raise ValueError(f"Error: YAML file {file_path} is empty or invalid")
        return content


def save_results(generated_dataset: Dict[str, str],
                 processed_data: Dict[str, List[str]],
                 skipped_data: List[str],
                 output_path: str) -> None:
    """
    Save the generated dataset, processed data, and skipped data to the output path.

    Args:
        generated_dataset (Dict[str, str]): the generated dataset
        processed_data (Dict[str, List[str]]): the processed data
        skipped_data (List[str]): the skipped data

    Returns:
        None
    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_json(os.path.join(output_path, "generated_dataset.json"), generated_dataset)
    save_json(os.path.join(output_path, "processed_data.json"), processed_data)
    save_json(os.path.join(output_path, "skipped_data.json"), skipped_data)

    temp_files = [i for i in glob.glob(f"{output_path}/*.json") if "_temp" in i]

    for temp_file in temp_files:
        os.remove(temp_file)


def aggregate_temp_files(output_path: str) -> None:
    """
    Aggregate the temp files into the processed data and skipped data.

    Args:
        output_path (str): the output path

    Returns:
        None
    """
    temp_files = [i for i in glob.glob(f"{output_path}/*.json") if "_temp" in i]

    temp_processed_data = []
    temp_skipped_data = []

    for temp_file in temp_files:
        data = load_json(temp_file)
        if "processed_data" in temp_file:
            temp_processed_data.extend(data)
        elif "skipped_data" in temp_file:
            temp_skipped_data.extend(temp_skipped_data)

        os.remove(temp_file)

    if len(temp_processed_data) > 0:
        save_json(os.path.join(output_path, "_temp_processed_data.json"), temp_processed_data)
        save_json(os.path.join(output_path, "_temp_skipped_data.json"), temp_skipped_data)
