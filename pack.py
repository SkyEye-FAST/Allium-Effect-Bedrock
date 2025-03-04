"""Packaging script for Allium Effect Resource Pack (Bedrock)."""

import shutil
import time
import zipfile as zf
from pathlib import Path
from typing import Final

P: Final[Path] = Path(__file__).resolve().parent
PACK_NAME: Final[str] = "allium-effect-bedrock"
ZIP_FILE: Final[str] = f"{PACK_NAME}.zip"
MCPACK_FILE: Final[str] = f"{PACK_NAME}.mcpack"


def file_size(p: Path) -> str:
    """Calculate file size and return human-readable string.

    Args:
        p (Path): Path to the file to be calculated

    Returns:
        str: Formatted file size string

    Raises:
        FileNotFoundError: When file does not exist
    """
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    size_in_bytes = p.stat().st_size
    units = ["B", "KB", "MB", "GB"]
    size = size_in_bytes
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{round(size, 2)} {units[unit_index]}"


def create_resource_pack() -> tuple[str, float]:
    """Create the resource pack.

    Returns:
        Tuple[str, str, float]: (zip_size, time_cost)

    Raises:
        FileNotFoundError: When required files are missing
    """
    pack_path = P / ZIP_FILE
    mcpack_path = P / MCPACK_FILE
    required_files = [
        P / "manifest.json",
        P / "pack_icon.png",
        P / "data" / "credits" / "end.txt",
    ]

    for file in required_files:
        if not file.exists():
            raise FileNotFoundError(f"Required file not found: {file}")

    start_time = time.time()
    with zf.ZipFile(pack_path, "w", compression=zf.ZIP_DEFLATED, compresslevel=9) as z:
        for file in required_files:
            z.write(file, arcname=file.relative_to(P))
        textures_path = P / "textures"
        if textures_path.exists():
            for texture in textures_path.rglob("*.*"):
                z.write(texture, arcname=texture.relative_to(P).as_posix())
    shutil.copy2(pack_path, mcpack_path)
    end_time = time.time()

    return file_size(pack_path), end_time - start_time


if __name__ == "__main__":
    try:
        zip_size, zip_time = create_resource_pack()
        print("Resource packs created:")
        print(f"    - ZIP: {P / ZIP_FILE}")
        print(f"    - MCPACK: {P / MCPACK_FILE}")
        print(f"Packaging completed in {zip_time:.2f} s. Size: {zip_size}")
    except Exception as e:
        print(f"Packaging failed: {e}")
