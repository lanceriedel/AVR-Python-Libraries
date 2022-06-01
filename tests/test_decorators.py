import pytest

import bell.vrc.utils.decorators as decorators


def test_try_except_no_reraise() -> None:
    @decorators.try_except(reraise=False)
    def fail1() -> None:
        raise ValueError("Test")

    @decorators.try_except()
    def fail2() -> None:
        raise ValueError("Test")

    # make sure no exception gets raised
    fail1()

    # make sure no exception gets raised, as default
    fail2()


def test_try_except_reraise() -> None:
    @decorators.try_except(reraise=True)
    def fail() -> None:
        raise ValueError("Test")

    # make sure exception gets raised
    with pytest.raises(ValueError):
        fail()
