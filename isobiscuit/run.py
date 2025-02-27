
def main():
    import sys
    from .runner import run


    biscuit = sys.argv[1]
    run(biscuit)
if __name__ == "__main__":
    main()