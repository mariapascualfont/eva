from setuptools import setup, find_packages

setup(
    name="eva-bio",
    version="1.0.0",
    description="AI-powered shell command assistant for bioinformaticians (Gemini API backend)",
    author="Your Name",
    python_requires=">=3.8",
    py_modules=["eva", "eva_core", "eva_tools"],
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "eva=eva:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
