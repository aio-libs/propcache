# TODO: Delete when there's a PyPI Cython release (3.1.0) that supports free-threaded Python 3.13.
FREE_THREADED_BUILD="$(python -c"import sysconfig; print(bool(sysconfig.get_config_var('Py_GIL_DISABLED')))")"
if [[ $FREE_THREADED_BUILD == "True" ]]; then
    python -m pip install -U pip
    python -m pip install --pre cython==3.1.0a1
    python -m pip install setuptools expandvars
fi
