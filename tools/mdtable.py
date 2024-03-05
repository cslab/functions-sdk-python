import logging
from importlib import import_module

from csfunctions.objects.base import BaseObject

logging.basicConfig(level=logging.INFO)


def clean_docstring(docstring: str):
    if docstring is None:
        return ""

    lines = docstring.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    cleaned_docstring = "\n".join(cleaned_lines)
    return cleaned_docstring


def create_object_section(object_path: str) -> str:
    logging.info("Generating section for %s", object_path)
    module_name = ".".join(object_path.split(".")[:-1])  # csfunctions.object
    class_name = object_path.split(".")[-1]  # Document

    try:
        module = import_module(module_name)
        object_class = getattr(module, class_name)
    except ImportError:
        logging.warning("Could not find object class %s!", object_path)

    # write object header
    section_content = "\n## " + object_path.split(".")[-1] + "\n"
    section_content += f"`{object_path}`\n\n"

    # add class docstring if one exists
    if object_class.__doc__:
        section_content += clean_docstring(object_class.__doc__) + "\n\n"

    # write table header
    section_content += "|Attribute|Type|Description|\n"
    section_content += "|-|-|-|\n"
    for fieldname, field in object_class.model_fields.items():
        if fieldname == "object_type":
            continue
        annotation = str(field.annotation).replace("<class '", "").replace("'>", "").replace("|", "\\|")
        section_content += f"|{fieldname}|{annotation}|{field.description or ''}|\n"

    return section_content


def get_short_object_paths() -> list[str]:
    """
    Returns a list import paths of all objects.
    Assumes that all objects can be imported from the csfunctions.objects module
    """
    object_paths = []
    object_classes = BaseObject.__subclasses__()
    object_classes = sorted(object_classes, key=lambda x: x.__name__)
    for object_class in object_classes:
        # we want the shortest path, which is csfunctions.objects
        class_name = object_class.__name__
        path = "csfunctions.objects." + class_name

        object_paths.append(path)

    return object_paths


def get_long_object_paths() -> list[str]:
    object_paths = []
    object_classes = BaseObject.__subclasses__()
    for object_class in object_classes:
        object_paths.append(object_class.__module__ + "." + object_class.__name__)

    return object_paths


def generate_object_page():
    page_content = ""  # pylint: disable=C0103
    for short_path in get_short_object_paths():
        page_content += create_object_section(short_path)

    for long_path in get_long_object_paths():
        # the remaining long paths e.g. "csfunctions.objects.briefcase.Briefcase" should only occur as types
        # we replace them with the classname, to take up less space, and add links to the class
        class_name = long_path.split(".")[-1]
        link = f"[{class_name}](objects.md#{class_name.lower()})"
        page_content = page_content.replace(long_path, link)

    # shorten a few more class names in types
    page_content = page_content.replace("datetime.datetime", "datetime").replace("datetime.date", "date")

    with open("docs/reference/objects.md", "w", encoding="utf-8") as f:
        f.write(page_content)


if __name__ == "__main__":
    generate_object_page()
