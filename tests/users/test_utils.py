import pytest

from funnyapi.users.utils import validate_password


@pytest.mark.parametrize(
    ("input", "expected"),
    (
        ("qweRTY$and4", "qweRTY$and4"),
        ("passWORD12#", "passWORD12#"),
        ("!@#SDF13zxc", "!@#SDF13zxc"),
    ),
)
def test_validate_password_good_passwords(input, expected):
    assert validate_password(input) == expected


@pytest.mark.parametrize(
    ("input",),
    (
        ("",),
        ("short",),
        ("loooooooooong",),
        ("upperLooooong",),
        ("UpperHasChars$%",),
        ("7128768176318263",),
        ("!@#!@@$@#$@#$@#",),
        ("AAAAAAAAAAAAA$AAA4",),
        ("aAAAAAAAAAAAA$AAA4",),
        ("aAAAAAAbcAAAAA$AAA4",),
    ),
)
def test_validate_password_bad_passwords(input):
    with pytest.raises(ValueError):
        validate_password(input)
