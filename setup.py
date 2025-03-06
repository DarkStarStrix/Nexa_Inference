from setuptools import setup, find_packages

setup(
    name="helixsynth",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "requests>=2.26.0",
        "prometheus-client>=0.11.0",
    ],
    author="Allan",
    author_email="allanw.mk@gmail.com",
    description="Protein Secondary Structure Prediction API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/helixsynth",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.10",
)
