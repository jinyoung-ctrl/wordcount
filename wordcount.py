"""텍스트 파일의 단어 수를 세는 CLI.

사용법: python wordcount.py <파일경로>
"""
import sys
from datetime import datetime
from pathlib import Path


def count_words(text: str) -> int:
    return len(text.split())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("사용법: python wordcount.py <파일경로>", file=sys.stderr)
        return 1

    path = Path(argv[1])
    if not path.exists():
        print(f"오류: '{path}' 파일을 찾을 수 없습니다. 경로를 확인해 주세요.", file=sys.stderr)
        return 1
    if not path.is_file():
        print(f"오류: '{path}'은(는) 파일이 아닙니다.", file=sys.stderr)
        return 1

    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        print(f"오류: '{path}'을(를) UTF-8 텍스트로 읽을 수 없습니다.", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"오류: '{path}'을(를) 읽는 중 문제가 발생했습니다: {e}", file=sys.stderr)
        return 1

    run_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{path}: {count_words(text)} 단어 (실행: {run_at})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
