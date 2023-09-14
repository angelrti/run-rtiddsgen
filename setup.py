################################################################################
# (c) 2023 Copyright, Real-Time Innovations, Inc. (RTI)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
import setuptools

with open("README.md", "r") as readme_f:
    readme_contents = readme_f.read()

setuptools.setup(
    name="run_rtiddsgen",
    version="0.1.0",
    author="Angel Martinez",
    author_email="angel@rti.com",
    description="Run rtiddsgen for a specific set of files.",
    license="License :: OSI Approved :: Apache Software License",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    url="https://github.com/angelrti/run-rtiddsgen.git",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'run-rtiddsgen=run_rtiddsgen:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows"
    ],
    install_requires=[
        "argcomplete"
    ],
    python_requires='>=3.8, <4',
)
