# Six Degrees of Separation - Wikipedia

![Example Gif](assets/wikiracer_demo.gif)

## Installation
```
git clone https://github.com/tyler-a-cox/degrees-of-wikipedia
cd degrees-of-wikipedia
python setup.py install
```

## Usage
`wikiracer "Michael Jordan" "Ficus lyrata"`

## Improvements
There are a couple of improvements I'd like to make:
- Store page information and links in the database and query database before making an http request
  - I haven't run a test yet but I think with the image metadata coming from the MediaWiki http request is slowing down those returns and a database query may be fast
- Run analysis on wikipedia queries to see what the average degree of separation between two wikipedia articles
