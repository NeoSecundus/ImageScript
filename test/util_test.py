import pytest

from imagescript._utils import bytes_to_image_data, _bytes_to_vector3


@pytest.mark.parametrize(
    ["example_data", "expected"],
    [(b"af13c876af", [(97, 102, 49), (51, 99, 56), (55, 54, 97), (102, 0, 0)])]
)
def test_bytes_to_vector3(example_data: bytes, expected: list[tuple[int, int, int]]):
    res = _bytes_to_vector3(example_data)
    assert res == expected


@pytest.mark.parametrize(
    ["example_data", "ratio_x", "ratio_y", "expected_dimensions"],
    [
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 3, 2, (12, 8, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 5, 2, (15, 6, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 11, 2, (22, 4, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 5, 3, (15, 9, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 2, 1, (12, 6, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 6, 3, (12, 6, 3)),
        (b"af13c876af13c876af13c876af13c876af13c876af13c876af13c876af13c876"*3, 1, 1, (8, 8, 3)),
    ]
)
def test_bytes_to_image_data(example_data: bytes, ratio_x: int, ratio_y: int, expected_dimensions: tuple[int, int]):
    res = bytes_to_image_data(example_data, ratio_x, ratio_y)
    assert res.shape == expected_dimensions
