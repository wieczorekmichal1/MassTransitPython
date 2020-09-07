import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='masstransitpython',
     version='0.0.1',
     py_modules=['RabbitMQReceiver', 'RabbitMQSender', 'RabbitMQConfiguration'],
     package_dir={'': 'src'},
     author="Michał Wieczorek",
     author_email="michal126@hotmail.com",
     description="Python RabbitMQ client for MassTransit Communication",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/byQ96/MassTransitPython",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )