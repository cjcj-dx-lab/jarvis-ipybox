import importlib
from dataclasses import dataclass
from inspect import getfile, getsource
from pathlib import Path, PurePath, PurePosixPath
from typing import List


@dataclass
class ModuleInfo:
    name: str
    relpath: PurePath
    source: str


def print_module_sources(module_names: List[str]):
    module_info_strings = []
    for module_name in module_names:
        module_info = get_module_info(module_name)
        module_info_str = f"```python\n# Module: {module_info.name}\n\n{module_info.source}\n```"
        module_info_strings.append(module_info_str)
    print("\n\n".join(module_info_strings))


def get_module_info(module_name: str) -> ModuleInfo:
    module = importlib.import_module(module_name)
    module_path = Path(getfile(module))

    relscope = PurePosixPath(module_name.replace(".", "/"))

    if module_path.name == "__init__.py":
        relpath = relscope / "__init__.py"
    else:
        relpath = relscope.with_suffix(".py")

    try:
        code = getsource(module)
    except OSError:
        code = ""

    return ModuleInfo(name=module.__name__, relpath=relpath, source=code)
