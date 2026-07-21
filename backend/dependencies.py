from dotenv import load_dotenv
import os
from pathlib import Path
from pwdlib import PasswordHash
import jwt


script_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=script_dir / ".env")

Secret_key = os.environ.get("SECRET_KEY")


pass_hash = PasswordHash.recommended()
