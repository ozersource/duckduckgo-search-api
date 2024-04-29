# DuckDuckGoSearchApi

Simple and direct interface for DuckDuckGo API. This library is designed to simplify searches and the analysis of results from DuckDuckGo.

## Instalation

To install run the following:

```python
pip install duckduckgo_search_api
```

## Available Methods

The `Duckduckgo` class offers the following main methods:

- `search(query)`: Accepts a query string and returns top **~20  search results** 


## Usage

**The use of proxies is recommended**

The proxy format should be: `ip:port@user:pass`.

Proxies can be loaded from a text file (.txt) adhering to the following format:
```
ip:port@user:pass
ip:port@user:pass
ip:port@user:pass
...
```

Alternatively, proxies can be specified directly using a Python dictionary as per the format shown above.

```python
from ddg import Duckduckgo

# Load proxies from a file
ddg_api = Duckduckgo(proxies="proxies.txt")
results = ddg_api.search("Google")
```

If the proxies parameter in the constructor is null, the search will proceed without using any proxies.

```python
from ddg import Duckduckgo

# No proxies used
ddg_api = Duckduckgo()
results = ddg_api.search("Google")
```

## Success request

Search results are returned as a Python dictionary. Each result contains the page title, URL, and a description

```json
{
  "success": true,
  "data": [
    {
      "title": "Page Title",
      "url": "https://www.example.com",
      "description": "Short description of the page"
    },
    
  ]
}
```

## Error request

In case of an error the returned object will contain the `success` field set to `false`

```json
{
  "success": false,
  "statusCode": 404,
  "message": "Failed to fetch data"
}
```

