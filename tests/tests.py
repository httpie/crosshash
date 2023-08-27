import pytest

# noinspection PyProtectedMember
from crosshash import ERROR_UNSAFE_NUMBER, JSON
from .cases import generate_cases, CASES_OK, CASES_UNSAFE_NUMBERS
from .utils import assert_all_equal, assert_all_fail


@pytest.mark.parametrize('data', CASES_UNSAFE_NUMBERS)
def test_unsafe_numbers(data: JSON):
    assert_all_fail(
        data=data,
        output_format='--json',
        error_message=ERROR_UNSAFE_NUMBER,
    )


@pytest.mark.parametrize('data', CASES_OK)
def test_crossjson(data: JSON):
    assert_all_equal(data=data, output_format='--json')


@pytest.mark.parametrize('data', CASES_OK)
def test_crosshash(data: JSON):
    assert_all_equal(data=data, output_format='--hash')


@pytest.mark.parametrize('data', generate_cases())
def test_crossjson_generated(data: JSON):
    assert_all_equal(data=data, output_format='--json')


@pytest.mark.parametrize('data', generate_cases())
def test_crosshash_generated(data: JSON):
    assert_all_equal(data=data, output_format='--hash')
