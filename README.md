# Jerome Translator

![example workflow](https://github.com/manosprom/jerome/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/manosprom/jerome/branch/master/graph/badge.svg?token=9USIPE55WW)](https://codecov.io/gh/manosprom/jerome)


A simple app that will translate a number a questions taken from trivia
using the transifex api.

# Flow

[![diagram](https://www.websequencediagrams.com/files/render?link=Y6iu140iVLcL1SfZq9Nlj1uZgCY2O7NW09Im4Og6jgVJOFbS2LjcE3hBPuReANud)]

## Trivia

- [Api Documentation](https://opentdb.com/api_config.php)



## Transifex

- [Api Documentation](https://transifex.github.io/openapi/index.html)

## Apis of Interest

- [Resources](https://transifex.github.io/openapi/index.html#tag/Resources)
    - [Create Resource](https://transifex.github.io/openapi/index.html#tag/Resources/paths/~1resources/post)
    - [List Resources](https://transifex.github.io/openapi/index.html#tag/Resources/paths/~1resources/get)
    - [Get Resource Details](https://transifex.github.io/openapi/index.html#tag/Resources/paths/~1resources~1{resource_id}/get)
    
- [Resource Strings](https://transifex.github.io/openapi/index.html#tag/Resource-Strings)
    - [Upload a new source file for a resource](https://transifex.github.io/openapi/index.html#tag/Resource-Strings/paths/~1resource_strings_async_uploads/post)
  
## Run the app.

### Arguments

| Arguments | Purpose | Default |
| --- | --- | --- |
| [--transifex-api-url TRANSIFEX_API_URL] | if required to specify a different transifex rest api url| https://rest.api.transifex.com |  
| [--trivia-api-url TRIVIA_API_URL] | if required to specify a different trivia api url | https://opentdb.com |
| [--questions-num QUESTIONS_NUM] | The amount of questions to retrieve per category on each run | 10 |
| --transifex-token TRANSIFEX_TOKEN | The transifex token that you got when you registered your account | Required |
| --transifex-organization TRANSIFEX_ORGANIZATION | The transifex organization that you have created from the dashboard | Required |
| --transifex-project TRANSIFEX_PROJECT | The transifex project that you have created from the dashboard | Required |
| -c --categories CATEGORIES [CATEGORIES ...]  | The trivia category ids | Required |
| --categories-index | View the id to title mapping from trivia | |

### Categories Index

To view the category ids that trivial supports.

```bash
python -m app --categories-index
```

```text
9 General Knowledge
10 Entertainment: Books
11 Entertainment: Film
12 Entertainment: Music
13 Entertainment: Musicals & Theatres
14 Entertainment: Television
15 Entertainment: Video Games
16 Entertainment: Board Games
17 Science & Nature
18 Science: Computers
19 Science: Mathematics
20 Mythology
21 Sports
22 Geography
23 History
24 Politics
25 Art
26 Celebrities
27 Animals
28 Vehicles
29 Entertainment: Comics
30 Science: Gadgets
31 Entertainment: Japanese Anime & Manga
32 Entertainment: Cartoon & Animations
```

### Run the app

1. Create and activate a virtual evniroment
```bash
python -m venv venv
. /venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Send questions for translation
```bash
python -m app --transifex-token the_token --transifex-organization the_organization --transifex-project the_project -c 16 17
```
