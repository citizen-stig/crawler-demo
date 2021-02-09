# Web crawler demo

## Prerequisites

* Python 3.8 or above
* [Pipenv](https://pipenv.pypa.io/en/latest/)

```
pipenv install
pipenv run python main.py https://project-plato.com/ output
```

# Functional Requirements

Implement recursive web-crawler of the site.

- ✅ crawler is command-line tool which accept starting url and destination directory
- ✅ crawler download the initial url and look to links inside original document (recursively)
- ✅ crawler does not walk to link outside initial url (if starting link is https://start.url/abc, then it goes to https://start.url/abc/123 and https://start.url/abc/456, but skip https://another.domain/ and https://start.url/def)
- ✅ crawler should correctly process Ctrl+C hotkey
- ✅ ✳️ crawler should be parallel.
- crawler should supports continue to load if destination directory already has loaded data (if we cancel download and than continue)


✳️ - Not entirely parallel since python GIL, but I/O operations are made in parallel. Also design is not ideal, separating fetching and storing threads can gain more performance


## Development

Run tests

```
make test
```

Run static analysis

```
make lint
```
