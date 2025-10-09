import tempfile
import subprocess
import sys


def show(image_bytes):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name

    if sys.platform == "darwin":
        subprocess.run(["open", tmp_path])
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", tmp_path])
    elif sys.platform.startswith("win"):
        subprocess.run(["start", tmp_path], shell=True)
    else:
        raise RuntimeError("Unsupported platform")
