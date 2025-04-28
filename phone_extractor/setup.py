from setuptools import setup, find_packages

setup(
    name="phone_extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "loguru>=0.7.0",
        "click>=8.1.3",
        "six>=1.16.0",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "phone-extractor=phone_extractor:main",
        ],
    },
    author="Developer",
    author_email="developer@example.com",
    description="Утилита для извлечения телефонных номеров из текстовых файлов",
    keywords="phone, extraction, regex",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
    ],
) 