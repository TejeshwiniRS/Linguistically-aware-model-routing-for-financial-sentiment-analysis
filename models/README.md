# Model Upload Utility

Use `upload_to_hf.py` to upload any local model folder to a Hugging Face Hub model repo.

## Prerequisites

- Python packages:
  - `huggingface_hub`
- Logged in to Hugging Face:

```bash
huggingface-cli login
```

## Script

`upload_to_hf.py`

Required CLI inputs:

- `--repo-id`: destination HF model repo id (`username/repo-name`)
- `--source-dir`: local folder to upload

Optional:

- `--path-in-repo`: destination subfolder inside the repo (default: `.`)
- `--private`: create repo as private if it does not exist
- `--check-only`: validate and preview files without uploading

## Usage

### 1) Validate only (no upload)

```bash
python upload_to_hf.py \
  --repo-id username/my-private-model \
  --source-dir "finetuned_distilbert_baseline/with PhraseBank dataset" \
  --check-only
```

### 2) Upload to repo root

```bash
python upload_to_hf.py \
  --repo-id username/my-private-model \
  --source-dir "finetuned_distilbert_baseline/with PhraseBank dataset" \
  --private
```

### 3) Upload into a subfolder in the repo

```bash
python upload_to_hf.py \
  --repo-id username/my-private-model \
  --source-dir "finetuned_distilbert_baseline/with PhraseBank dataset" \
  --path-in-repo "phase1/baseline"
```

## Notes

- The script checks that the source directory exists and is not empty before upload.
- `.DS_Store` files are ignored.
- If the repo already exists, the script reuses it (`exist_ok=True`).
