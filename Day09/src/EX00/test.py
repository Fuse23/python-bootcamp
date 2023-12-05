from calculator import add, sub, mul, div


def main():
    print(f"{add(15, 22)=}")
    print(f"{add(1.23, 2)=}")

    print(f"{sub(15, 22)=}")
    print(f"{sub(15, 23.2)=}")

    print(f"{mul(15, 22)=}")
    print(f"{mul(1.5, 2.2)=}")

    print(f"{div(15, 22)=}")
    print(f"{div(15, 2.2)=}")
    print(f"{div(15, 0)=}")  # raise ZeroDivisoinError


if __name__ == "__main__":
    main()
