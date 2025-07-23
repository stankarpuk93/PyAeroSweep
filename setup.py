from setuptools import setup, find_packages

setup(
    name="PyAeroSweep",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=["numpy", "scipy", "matplotlib"],
    python_requires=">=3.8",
)

print("\nPyAeroSweep installed successfully!")