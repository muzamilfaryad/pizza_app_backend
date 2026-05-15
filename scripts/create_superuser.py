import argparse
import getpass
import os
import sys

from sqlalchemy.orm import Session

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.database import SessionLocal
from core.security import hash_password
from models.user import User


def create_or_promote_superuser(db: Session, username: str, email: str, password: str) -> None:
    existing_user = db.query(User).filter((User.email == email) | (User.username == username)).first()

    if existing_user:
        existing_user.username = username
        existing_user.email = email
        existing_user.password = hash_password(password)
        existing_user.is_superuser = True
        db.commit()
        print(f"Updated existing user '{existing_user.username}' to superuser.")
        return

    new_user = User(
        username=username,
        email=email,
        password=hash_password(password),
        is_superuser=True,
    )
    db.add(new_user)
    db.commit()
    print(f"Created superuser '{username}'.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or promote a superuser")
    parser.add_argument("--username", required=True, help="Superuser username")
    parser.add_argument("--email", required=True, help="Superuser email")
    parser.add_argument(
        "--password",
        required=False,
        help="Superuser password (if omitted, prompt securely)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    password = args.password or getpass.getpass("Password: ")

    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return 1

    db = SessionLocal()
    try:
        create_or_promote_superuser(db, args.username, args.email, password)
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
