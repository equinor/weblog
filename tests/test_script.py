import os


def test_script():
    assert os.system("which wlog") == 0
    assert os.system("wlog -h") == 0
    assert os.system("wlog x") >> 8 == 1  # 16 bit error code
