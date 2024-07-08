import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QIRT",
    version="1.0.0",
    author="HSIEH, LI-YU",
    author_email="lyhsieh.lou@gmail.com",
    description="A quantum information research toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Slope86/Quantum-Information-Research-Toolkit",
    packages=setuptools.find_packages(include=("QIRT", "QIRT.*")),
    package_data={"QIRT.config": ["default_config.ini"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["qiskit[visualization] == 1.1.0"],
    python_requires=">=3.10",
)
