import sys
from application import Application

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    app = Application()
    app.run(filename)

if __name__ == "__main__":
    main()
