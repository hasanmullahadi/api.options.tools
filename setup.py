from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="options-tools",
    version="1.0.0",
    author="Hasan Mohammad",
    author_email="contact@options.tools",
    description="Professional options and market analysis API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasanmullahadi/api.options.tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.26.0",
        "pydantic>=2.5.0",
        "websocket-client>=1.7.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "mcp": ["anthropic-mcp>=0.1.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "black>=23.12.0",
            "mypy>=1.8.0",
        ]
    },
    keywords="options trading finance api stocks derivatives sec filings market-data",
    project_urls={
        "Documentation": "https://docs.options.tools",
        "API Reference": "https://api.options.tools/docs",
        "Bug Reports": "https://github.com/hasanmullahadi/api.options.tools/issues",
        "Source": "https://github.com/hasanmullahadi/api.options.tools",
    },
)