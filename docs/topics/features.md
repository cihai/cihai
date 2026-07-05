(features)=

# Features

- Handling {term}`CJK` variants

  cihai builds upon the {doc}`UNIHAN dataset <../datasets/unihan>`: "thousands of years worth of
  writing have produced thousands of pairs which can be used more-or-less interchangeably." For more
  information, see "Unification Rules" on page 679 of _The Unicode Standard_
  ([.pdf](http://www.unicode.org/versions/Unicode9.0.0/ch18.pdf)).

- Extensibie

  cihai will be able to pull remote {term}`CJK` datasets.

  In addition, the handling of variants will create new ways to discover and interpret CJK
  characters while using these datasets.

- Python API and CLI application

  {class}`cihai.core.Cihai` can be used as a Python {ref}`API <api>` as well as a command line
  application via `$ cihai`.

- Asian encoding swiss army knife

  Functions under the hood such as {mod}`cihai.conversion` are tested across
  python implementations to handle a growing assortment of Asian encodings.

[variants]: http://www.unicode.org/reports/tr38/tr38-21.html#N10211
