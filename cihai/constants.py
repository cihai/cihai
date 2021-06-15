#: Default configuration
DEFAULT_CONFIG = {
    "debug": False,
    "database": {"url": 'sqlite:///{user_data_dir}/cihai.db'},
    "dirs": {
        "cache": '{user_cache_dir}',
        "log": '{user_log_dir}',
        "data": '{user_data_dir}',
    },
}

#: User will be prompted to automatically configure their installation for UNIHAN
UNIHAN_CONFIG = {
    "datasets": {"unihan": "cihai.data.unihan.dataset.Unihan"},
    # Turn off by default for using as a plugin example in examples/
    # "plugins": {"unihan": {"variants": "cihai.data.unihan.dataset.UnihanVariants"}},
}
