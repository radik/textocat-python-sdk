[![Build Status](https://travis-ci.org/radik/textocat-python-sdk.svg?branch=master)]
(https://travis-ci.org/radik/textocat-python-sdk)

# Unofficial Textocat Python SDK

This is unofficial python sdk for [Textocat](http://textocat.com).

[Textocat API](http://docs.textocat.com/).

# Installation

```bash
pip install textocat
```

**NOTE:** package is compatible with Python 2 and 3.

# Usage

```python
from textocat.api import TextocatApi, Document

api = TextocatApi(YOUR_AUTH_TOKEN)

# Getting API status
status = api.status()

# Sending document for entity recognition
documents = [Document('Hello, World!', tag='greeting')]
batch_status = api.entity_queue(documents)
```

Other examples could be found in [examples](./examples).

# License

Copyright 2015 Radik Fattakhov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.