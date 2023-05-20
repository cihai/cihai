import typing as t

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
UNIHAN_FIELDS: t.List[str] = [
    "kAccountingNumeric",
    "kCangjie",
    "kCantonese",
    "kCheungBauer",
    "kCihaiT",
    "kCompatibilityVariant",
    "kDefinition",
    "kFenn",
    "kFourCornerCode",
    "kFrequency",
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
    "kRSJapanese",
    "kRSKanWa",
    "kRSKangXi",
    "kRSKorean",
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

#: Default settings passed to unihan-etl
UNIHAN_ETL_DEFAULT_OPTIONS = {
    "input_files": UNIHAN_FILES,
    "fields": UNIHAN_FIELDS,
    "format": "python",
    "expand": False,
}
