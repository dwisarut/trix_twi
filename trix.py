import sys
from pathlib import Path
from scanner import Scanner

HAD_ERROR = False

def main(args: list[str]):
    try:
        if len(args) > 1:
            print("Usage: jTrix [script]")
            sys.exit(64)
        elif len(args) == 1:
            run_file(args[0])
        else:
            run_prompt()
    except Exception as e:
        print(e)

def run_file(path: str):
    global HAD_ERROR
    data = Path(path).read_text()
    
    run(data)
    
    if HAD_ERROR:
        sys.exit(65)


def run_prompt():
    global HAD_ERROR
    
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        
        run(line)
        HAD_ERROR = False


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    
    for token in tokens:
        print(token)


def error(line: int, msg: str):
    report(line, "", msg)


def report(line: int, where: str, msg: str):
    global HAD_ERROR
    
    print(f"[line {line}] Error {where}: {msg}")
    HAD_ERROR = True


if __name__ == "__main__":
    main(sys.argv[1:])