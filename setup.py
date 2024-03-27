import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

__version__ = "0.0.3"

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

if __name__ == "__main__":
    setup(
        name="youscribe",
        author="Digital Observatory",
        author_email="digitalobservatory@qut.edu.au",
        version=__version__,
        description="Library to transcribe YouTube videos using Whisper model",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        packages=find_packages(where="src"),
        install_requires=[
            "faster-whisper >= 0.10.0",
            "beautifulsoup4 >= 4.12.2",
            "requests >= 2.31.0",
            "yt-dlp >= 2024.03.10",
        ],
        python_requires=">=3.10",
    )
