from pathlib import Path

file_dir = Path(__file__).parent.resolve()

UPLOAD_FOLDER = file_dir / "uploads"
STATIC_FOLDER = file_dir / "static"
CONFIG_FOLDER = file_dir / "config"
LOCAL_MODELS_FOLDER = file_dir / "local_models"
DATABASE_DIR = file_dir / "chroma_db"


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}
