from pathlib import Path


def main() -> None:
    target = Path("data/uploads")
    target.mkdir(parents=True, exist_ok=True)
    (target / "README.md").write_text("Place demo voice notes, screenshots, and support documents here.\n", encoding="utf-8")


if __name__ == "__main__":
    main()
