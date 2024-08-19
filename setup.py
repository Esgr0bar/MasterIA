
from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai_audio_mixing_tool",
    version="0.1.0",
    author="Esgr0bar",
    description="A machine learning tool for automated audio mixing and mastering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Esgr0bar/ai_audio_mixing_tool",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scikit-learn",
        "joblib",
        "librosa",  # For audio processing
        "soundfile",  # For handling audio files
        "jupyter",  # For running notebooks
        "pytest",  # For testing
        "mkdocs",  # For documentation
        "matplotlib",  # For any visualizations
    ],
    extras_require={
        "dev": ["pytest", "flake8", "black"],
    },
    entry_points={
        "console_scripts": [
            "train_model=train_model:main",
            "run_inference=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)
