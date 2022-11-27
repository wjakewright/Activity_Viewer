from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="Activity_Viewer",
    version="0.0.77",
    description="GUI to extract fluorescence for nerual activity videos",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/wjakewright/Activity_Viewer",
    author="William (Jake) Wright",
    liscence="",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pyqtgraph",
        "PyQt5",
        "numba",
        "cmapy",
        "scikit-image",
        "opencv-python",
        "dataclasses",
        "scipy",
        "shapely",
    ],
    entry_points={
        "console_scripts": [
            "Activity_Viewer = Activity_Viewer.Activity_Viewer_pyqt:main",
        ]
    },
)

