import os
from collections import defaultdict

current_directory = os.path.dirname(__file__)
icon_dict = defaultdict(lambda: (current_directory + "/question_mark.png"))

for potential_file in os.scandir(current_directory):
    file_extension = potential_file.name[-3:]  # TODO - Will break if extension is different format
    if potential_file.is_file() and (file_extension == "png" or file_extension == "jpg"):
        image_name = potential_file.name[:-4]
        icon_dict[image_name] = potential_file.path
