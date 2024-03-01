# setup-python-uv-action

This composite action wraps [actions/setup-python](https://github.com/actions/setup-python) and additionally sets up the [uv package installer](https://github.com/astral-sh/uv). It creates and activates a new virtual environment. Caching is optionally available, wrapping [actions/cache](https://github.com/actions/cache).

## Basic Usage

```yaml
- name: Set up Python with uv
  uses: jayqi/setup-python-uv-action
  with:
    python-version: 3.12
```

Options: 

- **`python-version`** (string, optional): Version range or exact version of Python or PyPy to use, using SemVer's version range syntax. Reads from `.python-version` if unset. Passed directly to [actions/setup-python](https://github.com/actions/setup-python).
- **`cache`** (string, optional): If set to 'packages', will cache uv's cache directory. If set to 'venv', will cache the virtual environment. By default, no caching will happen.
- **`cache-dependency-path`** (string, optional): Specify dependency files to hash for cache key. Supports wildcards or a list of file names separated by spaces.

See [`action.yml`](./action.yml) for additional details and 

## Caching

This action supports two modes of caching: 

- `packages` will cache the uv package cache directory. This is where uv caches intermediate artifacts like downloaded wheels, downloaded sdists, and built wheels. 
- `venv` will cache the virtual environment, meaning the actual installed packages. 

Caching will use the following cache keys depending on the caching mode:

- `packages`: `setup-python-uv-action-venv-{runner.os}-python-{python-version}(-{dependency-checksum})`
- `venv`: `setup-python-uv-action-venv-{runner.os}-python-{python-version}(-{dependency-checksum})`

The `dependency-checksum` is optionally appended to the cache key depending on whether you've provided any dependency paths with the optional `cache-dependency-path` parameter. A common pattern used with [actions/setup-python](https://github.com/actions/setup-python) is to have the cache key depend on the contents of a requirements file, like `requirements.txt` or `pyproject.toml`. The `cache-dependency-path` parameter accepts one or many path patterns in a space-delimited list. All contents of all files will be hashed together into the checksum. (You can see [`checksum.py`](./checksum.py) for exactly how this is performed.) If you want to newlines to delimit your list for readability, use YAML's `>-` ["folded style" and "stripping"](https://yaml-multiline.info/) multiline string indicator to automatically replace all newlines with spaces.

```yaml
- name: Set up Python with uv (local source)
  uses: jayqi/setup-python-uv-action
  with:
    python-version: 3.12
    cache: packages
    cache-dependency-path: >-
      pyproject.toml
      requirements.txt
```