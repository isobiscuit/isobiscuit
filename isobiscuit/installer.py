





def main():
    from .installer import installFunc
    import sys
    installFunc(sys.argv[1], sys.argv[2])



if __name__ == "__main__":
    main()