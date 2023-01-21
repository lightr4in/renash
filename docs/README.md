# Deployment

To deploy renash to pypi.org, go to source directory (`cd src/`) and do the following steps.


## Build package

To build the package, run the following command:

```shell
python setup.py sdist bdist_wheel
```

This operation will create a `src/dist` folder.

## Install package

To try and install the package, run the following command with correct version:

```shell
pip install --user dist/renash-<version>-py3-none-any.whl  
```

### Publish

## Publish package to TestPyPi

To try and upload the package to TestPyPi, run the following command:

```shell
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

You will be prompted for username and password to authenticate.

## Publish package to PyPi

To publish the package to PyPi, run the following command:

```shell
twine upload --repository-url https://pypi.org/legacy/ dist/*
```

You will be prompted for username and password to authenticate.