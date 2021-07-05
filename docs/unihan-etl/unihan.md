(unihan)=

# About UNIHAN

:::{seealso}

- [Wikipedia article](https://en.wikipedia.org/wiki/Han_unification)
- [UNIHAN database documentation][unihan database documentation]

:::

## Languages, Computers, and You

There are many languages and writing systems around the world. Computers
internally use numbers to represent characters in writing systems. As
computers became more prominent, hundreds of encoding systems were
developed to handle writing systems from different regions.

No single encoding system covered all languages. Adding to the complexity,
encodings conflicted with each other on the numbers assigned to
characters. Any data decoded with the wrong standard would turn up as
gibberish.

[Unicode][unicode] is a standard devised to provide a unique number for every
character.

This entails pulling together minds from around the world to assign codepoints.

The _Unicode Consortium_ is a non-profit organization founded to develop,
extend and promote use of the Unicode Standard.

## What is UNIHAN?

UNIHAN, short for [Han unification][han unification], is the effort of the consortium
assign codepoints to CJK characters. Any single {}`han character` can
multiple historical or regional variants to account for, hence "unification".

```{image} _static/img/sword_variants.png
:width: 300px
:align: center

```

To do this, various sources of information are pulled together and cross-referenced
to detail characteristics of the glyphs, and vet them through a thorough
proofreading process. It's an international effort, hallmarked by between
researchers and groups like the [Ideographic Rapporteur Group][ideographic rapporteur group]. Glyphs
once only noted in dictionaries and antiquity are set in stone with
their own codepoints, carefully cross-referenced with information from,
often multiple, distinct sources.

The advantage that UNIHAN provides to east asian researchers, including
sinologists and japanologists, linguists, anaylsts, language learners, and
hobbyists cannot be understated. Unbeknownst to users, its used under the hood
in many applications and websites.

The resulting standard has industrial ramifications downstream to
software developers and computer users. When a version of Unicode is
released, it is then incorporated downstream in software projects.

## The database

UNIHAN provides a database of its information, which is the culmination
of CJK information that has been vetted and proofed painstakingly over years.

You can view the [UNIHAN Database documentation][unihan database documentation] to see where information
on each field of information is derived from. For instance:

- [kCantonese](http://www.unicode.org/reports/tr38/#kCantonese):
  The Cantonese pronunciation(s) for this character using the
  [jyutping romanization][jyutping romanization].

  Bibliography:

  1. Casey, G. Hugh, S.J. Ten Thousand Characters: An Analytic Dictionary. Hong Kong: Kelley and Walsh,1980 (kPhonetic).
  2. Cheung Kwan-hin and Robert S. Bauer, The Representation of Cantonese with Chinese Characters, Journal of Chinese Linguistics Monograph Series Number 18, 2002.
  3. Roy T. Cowles, A Pocket Dictionary of Cantonese, Hong Kong: University Press, 1999 (kCowles).
  4. Sidney Lau, A Practical Cantonese-English Dictionary, Hong Kong: Government Printer, 1977 (kLau).
  5. Bernard F. Meyer and Theodore F. Wempe, Student’s Cantonese-English Dictionary, Maryknoll, New York: Catholic Foreign Mission Society of America, 1947 (kMeyerWempe).
  6. 饒秉才, ed. 廣州音字典, Hong Kong: Joint Publishing (H.K.) Co., Ltd., 1989.
  7. 中華新字典, Hong Kong:中華書局, 1987.
  8. 黃港生, ed. 商務新詞典, Hong Kong: The Commercial Press, 1991.
  9. 朗文初級中文詞典, Hong Kong: Longman, 2001.

- [kHanYu](http://www.unicode.org/reports/tr38/#kHanYu): The position of this
  character in the Hanyu Da Zidian (HDZ) Chinese character dictionary.

  Bibliography:

  1. <Hanyu Da Zidian> [‘Great Chinese Character Dictionary’ (in 8 Volumes)]. XU Zhongshu (Editor in Chief). Wuhan, Hubei Province (PRC): Hubei and Sichuan Dictionary Publishing Collectives, 1986-1990. ISBN: 7-5403-0030-2/H.16.

- [kHanyuPinyin](http://www.unicode.org/reports/tr38/#kHanyuPinyin):
  The 漢語拼音 Hànyǔ Pīnyīn reading(s) appearing in the edition of 《漢語大字典
  [Hànyǔ Dà Zìdiǎn][hànyǔ dà zìdiǎn] (HDZ) specified in the “kHanYu” property description (q.v.).

  Bibliography:

  - This data was originally input by 井作恆 Jǐng Zuòhéng
  - proofed by 聃媽歌 Dān Māgē (Magda Danish, using software donated by 文林 Wénlín Institute, Inc. and tables prepared by 曲理查 Qū Lǐchá),
  - and proofed again and prepared for the Unicode Consortium by 曲理查 Qū Lǐchá (2008-01-14).

Han Unification is a global effort. And it's available free to the world.

[unicode]: https://en.wikipedia.org/wiki/Unicode
[han unification]: https://en.wikipedia.org/wiki/Han_unification
[ideographic rapporteur group]: https://en.wikipedia.org/wiki/Ideographic_Rapporteur_Group
[han character]: https://en.wikipedia.org/wiki/Chinese_characters
[unihan database documentation]: http://www.unicode.org/reports/tr38/
[jyutping romanization]: https://en.wikipedia.org/wiki/Jyutping
[hànyǔ dà zìdiǎn]: https://en.wikipedia.org/wiki/Hanyu_Da_Zidian

## The problem

It's difficult to readily take advantage of UNIHAN database in its
raw form.

UNIHAN comprises over 20 MB of character information, separated
across multiple files. Within these files is _90_ fields, spanning 8
general categories of data. Within some of fields, there are specific
considerations to take account of to use the data correctly, for instance:

UNIHAN's values place references to its own codepoints, such as
_kDefinition_:

```
U+3400       kDefinition     (same as U+4E18 丘) hillock or mound
```

And also by spaces, such as in _kCantonese_:

```
U+342B       kCantonese      gun3 hung1 zung1
```

And by spaces which specify different sources, like _kMandarin_, "When
there are two values, then the first is preferred for zh-Hans (CN) and the
second is preferred for zh-Hant (TW). When there is only one value, it is
appropriate for both.":

```
U+7E43        kMandarin       běng bēng
```

Another, values are delimited in various ways, for instance, by rules,
like _kDefinition_, "Major definitions are separated by semicolons, and minor
definitions by commas.":

```
U+3402       kDefinition     (J) non-standard form of U+559C 喜, to like, love, enjoy; a joyful thing
```

More complicated yet, _kHanyuPinyin_: "multiple locations for a given
pīnyīn reading are separated by “,” (comma). The list of locations is
followed by “:” (colon), followed by a comma-separated list of one or more
pīnyīn readings. Where multiple pīnyīn readings are associated with a
given mapping, these are ordered as in HDZ (for the most part reflecting
relative commonality). The following are representative records.":

```
U+3FCE  kHanyuPinyin    42699.050:fèn,fén
U+34D8  kHanyuPinyin    10278.080,10278.090:sù
U+5364  kHanyuPinyin    10093.130:xī,lǔ 74609.020:lǔ,xī
U+5EFE  kHanyuPinyin    10513.110,10514.010,10514.020:gǒng
```

Data could be exported to a CSV, but users wouldn't be able to
handle delimited values and structured information held within.

Since CSV does not support structured information, another format that
supports needs to be found.

Even then, users may not want an export that expands the structured
output of fields. So if a tool exists, exports should be configurable. Users
could then export a field with `gun3 hung1 zung1` pristinely without
turning it into list form.
