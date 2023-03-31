from multiply import MultiplyNumbers


def test_multiply():
    first_number = 5
    second_number = 6
    assert MultiplyNumbers().multiply(first_number, second_number) == 30
