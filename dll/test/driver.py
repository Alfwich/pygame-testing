from ctypes import cdll

TEST_DLL = cdll.LoadLibrary("test_dll.dll")

def main():
    if hasattr(TEST_DLL, "sum"):
        print(TEST_DLL.sum(100, 200))


if __name__ == "__main__":
    main()
