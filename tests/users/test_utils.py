import pytest

from funnyapi.users.utils import get_password_hash, validate_password, verify_password


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


def test_get_password_hash():
    hash = get_password_hash("test_password_01")

    assert hash != "test_password_01"
    assert isinstance(hash, str)
    assert len(hash) > 80


def test_password_hash_flow():
    hash1 = get_password_hash("test_password_01")
    hash2 = get_password_hash("test_password_02")

    assert verify_password("test_password_01", hash1)
    assert not verify_password("test_password_01", hash2)
