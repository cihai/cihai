from .conversion import parse_untagged, parse_vars


def mk_unihan(Base):
    class Unihan(Base):
        __tablename__ = 'unihan'

        def tagged_vars(self, col):
            """
            Return a variant column as an iterator of (char, tag) tuples.
            """
            return parse_vars(getattr(self, col))

        def untagged_vars(self, col):
            """
            Return a variant column as an iterator of chars.
            """
            return parse_untagged(getattr(self, col))

    return Unihan
