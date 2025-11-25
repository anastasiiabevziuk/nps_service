from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, Any, Optional


def get_exif_data(file_path: str) -> Dict[str, Optional[str]]:
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data is None:
            return {}

        exif_info = {}

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "Make":
                exif_info["camera"] = str(value).strip()
            elif tag == "Model":

                if "camera" not in exif_info:
                    exif_info["camera"] = str(value).strip()
                else:
                    exif_info["camera"] += f" ({str(value).strip()})"
            elif tag == "ISOSpeedRatings":
                exif_info["iso"] = str(value)

        exif_info["file_path"] = file_path

        return exif_info

    except Exception as e:
        print(f"Error reading EXIF data: {e}")
        return {}
