from IPython.display import display as ipy_display
from IPython.core.display import Image as IPyImage


def monkey_display(image):
    image_bytes = image.data  # Adjust as needed for your Image class
    import tempfile, sys, subprocess

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


def display(obj):
    if isinstance(obj, IPyImage):
        monkey_display(obj)
    else:
        ipy_display(obj)
