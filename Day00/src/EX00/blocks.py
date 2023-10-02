import sys


def test() -> None:
    assert check([
        "00000254b208c0f43409d8dc00439896",
        "000000434dd5469464f5cafd8ffe3609",
        "00000f31eaabadef948f28d1",
        "e7a1ee0b7de74786a2c0180bcdb632da",
        "0000085a34260d1c84e89865c210ceb4",
        "073f7873a75c457cbb3307d729501cb5",
        "b7c93ff4cc1c4e0486a8fc66605",
        "fe564b26f25e47c393d07e494021479e",
        "a5dff06057d14566b45caef813511738",
        "0000071f49cffeaea4184be3d507086v"
        ]) == [
        "00000254b208c0f43409d8dc00439896",
        "0000085a34260d1c84e89865c210ceb4",
        "0000071f49cffeaea4184be3d507086v"
        ]
    assert check([
        "00000",
        "000000",
        "00000000000000000000000000000000",
        "00000100000000000000000000000000",
        "1111010000132435vjieviw3gwn4otg7",
        "oooooaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "00",
        "0000017cohugy298onh2iwof2g88w7sh"
    ]) == [
        "00000100000000000000000000000000",
        "0000017cohugy298onh2iwof2g88w7sh"
    ]
    assert check([
        "00000254b208c0f43409d8dc00439896",
        "000000434dd5469464f5cafd8ffe3609",
        "00000f31eaabadef948f28d1",
        "e7a1ee0b7de74786a2c0180bcdb632da",
        "0000085a34260d1c84e89865c210ceb4",
        "073f7873a75c457cbb3307d729501cb5",
        "b7c93ff4cc1c4e0486a8fc66605",
        "fe564b26f25e47c393d07e494021479e",
        "a5dff06057d14566b45caef813511738",
        "0000071f49cffeaea4184be3d507086v",
        "0",
        "01",
        "023",
        "00000100000000000000000000000000"
    ]) == [
        "00000254b208c0f43409d8dc00439896",
        "0000085a34260d1c84e89865c210ceb4",
        "0000071f49cffeaea4184be3d507086v",
        "00000100000000000000000000000000"
    ]
    assert check([""]) == []
    assert check([]) == []
    print("Well done!!!")


def check(input_hashes: list[str]) -> list[str]:
    hashes: list[str] = [] # return this list for tests
    for hash in input_hashes:
        if len(hash) == 32 and hash.startswith("00000") and hash[5] != '0':
            # hashes.append(hash) # uncomment this line for tests
            print(hash)
    return hashes


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of args!")
        exit(-1)
    if not sys.argv[1].isnumeric():
        print("Args must be a number!")
        exit(-1)
    hashes: list[str] = []
    try:
        for _ in range(int(sys.argv[1])):
            hashes.append(sys.stdin.readline().strip())
        check(hashes)
    except EOFError:
        print("EOFError: EOF when reading a line")
        exit(-1)

    # test()
