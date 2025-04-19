from setuptools import setup, find_packages

setup(
    name="image2webp",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "Pillow>=9.0.0",
    ],
    entry_points={
        'console_scripts': [
            'image2webp=main:main',
        ],
    },
    author="User",
    author_email="user@example.com",
    description="将图片转换为WebP格式的工具",
    keywords="image, webp, converter",
    python_requires=">=3.6",
)
