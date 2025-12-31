def test_sys_path():
    import sys
    print("\n\n=== PYTEST sys.path ===")
    for p in sys.path:
        print(p)
    print("=== END ===\n\n")
