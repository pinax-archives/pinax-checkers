from distutils.core import setup


setup(
    name="pinax.checkers",
    version="1.1",
    author="Pinax",
    author_email="development@eldarion.com",
    url="https://github.com/pinax/pinax-checkers",
    description="Style checker for Pinax and Eldarion OSS",
    license="BSD",
    packages=[
        "pinax",
        "pinax.checkers",
    ],
    install_requires=["pylint>=0.25.0"],
)
