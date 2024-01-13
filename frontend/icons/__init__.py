import os
from collections import defaultdict
from typing import Dict

current_directory = os.path.dirname(__file__)
icon_dict: Dict[str, str] = defaultdict(lambda: (current_directory + "/question_mark.png"))


def map_all_icons(dir: str) -> None:
    for potential_file in os.scandir(dir):
        # TODO - Will break if extension is different format
        file_extension = potential_file.name[-3:]
        if not potential_file.is_file():
            map_all_icons(potential_file)
            continue
        if file_extension == "png" or file_extension == "jpg":
            image_name = potential_file.name[:-4]
            icon_dict[image_name] = potential_file.path


map_all_icons(current_directory)
