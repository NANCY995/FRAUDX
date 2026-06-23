from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("config/requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="fraudx",
    version="2.0.0",
    author="Johnson Nancy",
    description="Système d'IA pour la détection de la fraude bancaire et mobile money au Togo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fraudx=fraudx.cli:main",
            "fraudx-train=train:main",
            "fraudx-api=src.api:main",
            "fraudx-simulate=simulate_stream:main",
        ],
    },
)
