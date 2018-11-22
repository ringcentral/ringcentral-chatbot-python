import setuptools
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("package.json", "r") as fh:
    js = fh.read()
    jss = json.loads(js)

setuptools.setup(
    name="ringcentral_bot_framework",
    version=jss['version'],
    author="Drake Zhao @ RingCentral",
    author_email="drake.zhao@ringcentral.com",
    description="RingCentral Chatbot Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zxdong262/ringcentral-chatbot-python",
    packages=setuptools.find_packages(),
    keywords=['ringcentral', 'bot', 'framework'],
    install_requires=[i.strip() for i in open('requirements.txt').readlines()],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)