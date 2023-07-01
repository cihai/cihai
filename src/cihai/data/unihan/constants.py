"""Constants for UNIHAN cihai dataset."""

from unihan_etl.options import Options

#: Mapping of files from unihan-etl (UNIHAN database)
UNIHAN_FILES = [
    "Unihan_DictionaryLikeData.txt",
    "Unihan_IRGSources.txt",
    "Unihan_NumericValues.txt",
    "Unihan_RadicalStrokeCounts.txt",
    "Unihan_Readings.txt",
    "Unihan_Variants.txt",
]


#: Mapping of field names from unihan-etl (UNIHAN database)
UNIHAN_FIELDS: list[str] = [
    "kAccountingNumeric",
    "kCangjie",
    "kCantonese",
    "kCheungBauer",
    "kCihaiT",
    "kCompatibilityVariant",
    "kDefinition",
    "kFenn",
    "kFourCornerCode",
    "kGradeLevel",
    "kHDZRadBreak",
    "kHKGlyph",
    "kHangul",
    "kHanyuPinlu",
    "kHanyuPinyin",
    "kJapaneseKun",
    "kJapaneseOn",
    "kKorean",
    "kMandarin",
    "kOtherNumeric",
    "kPhonetic",
    "kPrimaryNumeric",
    "kRSAdobe_Japan1_6",
    "kRSUnicode",
    "kSemanticVariant",
    "kSimplifiedVariant",
    "kSpecializedSemanticVariant",
    "kTang",
    "kTotalStrokes",
    "kTraditionalVariant",
    "kVietnamese",
    "kXHC1983",
    "kZVariant",
]


class UnihanEtlDefaultOptionsDict(t.TypedDict):
    """Default settings passed to unihan-etl."""

    input_files: t.List[str]
    fields: t.Sequence[str]
    format: t.Literal["json", "csv", "yaml", "python"]
    expand: bool


UNIHAN_ETL_DEFAULT_OPTIONS_DICT: UnihanEtlDefaultOptionsDict = {
    "input_files": UNIHAN_FILES,
    "fields": UNIHAN_FIELDS,
    "format": "python",
    "expand": False,
}
UNIHAN_ETL_DEFAULT_OPTIONS = Options(**UNIHAN_ETL_DEFAULT_OPTIONS_DICT)
