"""
LogisticSmart v2.0 - Setup Configuration
Sistema Inteligente de Análise de Entregas
"""

from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name="logistic-smart",
    version="2.0.0",
    description="Sistema Inteligente de Análise de Entregas",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NEO-SH1W4/LogisticSmart",
    author="NEO-SH1W4",
    author_email="",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "logistics", "delivery", "analysis", "streamlit", "dashboard", 
        "reporting", "excel", "csv", "data-processing"
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.31.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "plotly>=5.15.0",
        "altair>=5.0.0",
        "bcrypt>=4.0.0",
        "python-dotenv>=1.0.0",
        "python-docx>=0.8.11",
        "pdfkit>=1.0.0",
        "pywin32>=306;sys_platform=='win32'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.4.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "logistic-smart=logistic_smart.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "logistic_smart": [
            "templates/*.html",
            "static/*.css",
            "static/*.js",
            "config/*.toml",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/NEO-SH1W4/LogisticSmart/issues",
        "Source": "https://github.com/NEO-SH1W4/LogisticSmart",
        "Documentation": "https://github.com/NEO-SH1W4/LogisticSmart#readme",
        "Demo": "https://logisticsmartx33beta.streamlit.app/",
    },
)

