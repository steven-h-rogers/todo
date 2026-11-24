import pytest
from core.security import hash_password, verify_hash

@pytest.mark.security
@pytest.mark.parametrize(
        "password",
        [
            "password",
            "sb#8fj(0dl)",
            "🤘😔🍑❤️",
            "          "
        ]
)
def test_hash_password(password: str):
    hashed_password = hash_password(password)
    assert hashed_password is not None

