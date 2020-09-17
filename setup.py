import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='masstransitpython-byQ96',
     version='0.0.5',
     author="Michał Wieczorek",
     author_email="michal126@hotmail.com",
     description="Python RabbitMQ client for MassTransit Communication",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/byQ96/MassTransitPython",
     packages=['masstransitpython'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.7',
)