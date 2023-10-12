import sys


def find_m_pattern(image: list[str]) -> bool:
    return True if (
            image[0][0] == image[0][-1] == "*" and image[0][1] != "*" and image[0][2] != "*"
            and image[1][0] == image[1][1] == image[1][3] == image[1][4] == "*"
            and image[1][2] != "*" and image[2][0] == image[2][2] == image[2][4] == "*"
            and image[2][1] != "*" and image[2][3] != "*" and image[0][3] != "*"
        ) else False


def test() -> None:
    assert find_m_pattern([
        "*d&t*",
        "**h**",
        "*l*!*"
    ]) == True, "\n*d&t*\n**h**\n*l*!*"
    assert find_m_pattern([
        "*****",
        "*****",
        "*****"
    ]) == False, "\n*****\n*****\n*****"
    assert find_m_pattern([
        "*s*f*",
        "**f**",
        "*a***"
    ]) == False, "\n*s*f*\n**f**\n*a***"
    assert find_m_pattern([
        "*s*f*",
        "**f**",
        "*****"
    ]) == False, "\n*s*f*\n**f**\n*****"
    assert find_m_pattern([
        "*s*f*",
        "**f**",
        "*g*s*"
    ]) == False, "\n*s*f*\n**f**\n*g*s*"
    assert find_m_pattern([
        "*123*",
        "**4**",
        "*5*6*"
    ]) == True
    print("Well done!!!")


if __name__ == "__main__":
    try:
        image: list[str] = sys.stdin.readlines()
        for i in range(len(image)):
            image[i] = image[i].strip()
            assert len(image[i]) == 5
            assert i <= 3
        print(find_m_pattern(image))
    except:
        print("Error")
        exit(-1)

    # test()
