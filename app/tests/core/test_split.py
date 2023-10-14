from app.core.mainSTT import split

def test_split_empty_array():
    res = split([], 10)
    assert res == []

def test_split_null_array():
    res = split(None, 10)
    assert res == []

def test_split_zero_size():
    res = split([1,2,3,5,7,8,2],0)
    assert res == []

def test_split_null_size():
    res = split([1,2,3,5,7,8,2],None)
    assert res == []

def test_split_size_bigger_than_array():
    res = split([1,2,3,4,5,6], 7)
    assert res == [[1,2,3,4,5,6]]

def test_split_different_sizes():
    res = split([1,2,3,4,5,6,7], 3)
    assert res == [
        [1,2,3],
        [4,5,6],
        [7]
    ]
