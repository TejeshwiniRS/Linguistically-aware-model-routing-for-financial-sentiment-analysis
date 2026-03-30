import argparse
from pathlib import Path
from typing import List

from huggingface_hub import HfApi, upload_folder


DEFAULT_IGNORE = [
    ".DS_Store",
    "**/.DS_Store",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Upload a local folder to a Hugging Face model repo. "
            "Both repo id and source folder are provided via command line."
        )
    )
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Hugging Face model repo id, e.g. username/my-model.",
    )
    parser.add_argument(
        "--source-dir",
        required=True,
        help="Local folder path to upload.",
    )
    parser.add_argument(
        "--path-in-repo",
        default=".",
        help="Destination path inside the HF repo (default: repository root).",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Create repo as private if it does not already exist.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate and print what would be uploaded without uploading.",
    )
    return parser.parse_args()


def validate_source_dir(source_dir: Path) -> List[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    files = [p for p in source_dir.rglob("*") if p.is_file()]
    if not files:
        raise ValueError(f"Source directory is empty: {source_dir}")
    return files


def print_check_summary(repo_id: str, source_dir: Path, path_in_repo: str, files: List[Path]) -> None:
    print("Validation successful.")
    print(f"Repo id:        {repo_id}")
    print(f"Source folder:  {source_dir}")
    print(f"Path in repo:   {path_in_repo}")
    print(f"File count:     {len(files)}")
    print("Sample files:")
    for file_path in files[:10]:
        print(f"  - {file_path.relative_to(source_dir)}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more")


def main() -> None:
    args = parse_args()

    repo_id = args.repo_id.strip()
    source_dir = Path(args.source_dir).expanduser().resolve()
    path_in_repo = args.path_in_repo.strip() or "."

    files = validate_source_dir(source_dir)
    print_check_summary(repo_id, source_dir, path_in_repo, files)

    if args.check_only:
        print("Check-only mode enabled. No upload performed.")
        return

    api = HfApi()
    api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        private=args.private,
        exist_ok=True,
    )

    upload_folder(
        repo_id=repo_id,
        repo_type="model",
        folder_path=str(source_dir),
        path_in_repo=path_in_repo,
        ignore_patterns=DEFAULT_IGNORE,
    )

    print("\nUpload complete.")
    print(f"Repo URL: https://huggingface.co/{repo_id}")


if __name__ == "__main__":
    main()
