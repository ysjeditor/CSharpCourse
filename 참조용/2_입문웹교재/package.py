"""배포용 ZIP 생성: python package.py (캐시와 로그 제외)."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
archive = root.parent / '입문웹교재-배포.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if not path.is_file() or any(part.startswith('.') or part == '__pycache__' for part in relative.parts):
            continue
        if path.suffix.lower() in ('.pyc', '.log', '.zip'):
            continue
        bundle.write(path, Path(root.name) / relative)
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
print(archive)
