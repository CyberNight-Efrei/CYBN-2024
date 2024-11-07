import base64
import io
import typing


class User:
    _default_nickname: str = "johndoe"
    _default_first_name: str = "john"
    _default_last_name: str = "doe"
    _default_role: typing.Literal["user", "admin"] = "user"

    def __init__(
        self,
        nickname: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        role: typing.Literal["user", "admin"] | None = None,
    ) -> None:
        self.nickname = nickname or self._default_nickname
        self.first_name = first_name or self._default_first_name
        self.last_name = last_name or self._default_last_name
        self.role = role or self._default_role

    # ===================== SECRET EXPORT METHOD ==============================
    # =========================================================================

    def export(self) -> io.BytesIO:
        from pathlib import Path
        import zipfile

        with Path(__file__).open() as f:
            to_export = (
                f.read()
                .replace('= "johndoe"', f"= {repr(self.nickname)}")
                .replace('= "john"', f"= {repr(self.first_name)}")
                .replace('= "doe"', f"= {repr(self.last_name)}")
                .replace('= "user"', f"= {repr(self.role)}")
                .split(f"# {'=' * 21} SECRET EXPORT METHOD {'=' * 30}")[0]
            )

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer, "w", zipfile.ZIP_DEFLATED
        ) as zip_file:
            zip_file.writestr("user.py", to_export)

        zip_buffer.seek(0)

        return zip_buffer

    # =========================================================================

    @classmethod
    def from_b64(
        cls: typing.Type["User"], b64: bytes
    ) -> typing.Optional["User"]:
        from pathlib import Path
        import random
        import string

        session_dir = Path("sessions")
        session_dir.mkdir(exist_ok=True)

        random_name = "".join(random.choices(string.ascii_letters, k=16))

        try:
            from zipimport import zipimporter

            if not cls.is_safe(b64):
                return None

            zip_buffer = io.BytesIO(base64.b64decode(b64))

            with (session_dir / random_name).open("wb") as f:
                f.write(zip_buffer.read())

            importer = zipimporter(str(session_dir / random_name))
            u = importer.load_module("user")

            user = u.User()

            (session_dir / random_name).unlink(missing_ok=True)

            return user

        except Exception as e:
            print("from_b64", e)
            (session_dir / random_name).unlink(missing_ok=True)
            return None

    # =========================================================================

    @staticmethod
    def is_safe(b64: bytes) -> bool:
        try:
            from pathlib import Path
            import zipfile

            zip_buffer = io.BytesIO(base64.b64decode(b64))

            with zipfile.ZipFile(
                zip_buffer, "r", zipfile.ZIP_DEFLATED
            ) as zip_file:
                data = zip_file.read("user.py").decode().strip()

            if len(splitted := data.split("\n")) != 22:
                print("is_safe", "line count missmatch")
                return False

            with Path(__file__).open() as f:
                must_be = (
                    f.read()
                    .split(f"# {'=' * 21} SECRET EXPORT METHOD {'=' * 30}")[0]
                    .strip()
                )

            sensible_lines = (6, 7, 8, 9)

            for i, l in enumerate(must_be.split("\n")):
                if i in sensible_lines:
                    continue

                if l != splitted[i]:
                    print("is_safe", "safe line missmatch")
                    return False

            for i in sensible_lines:
                safe = must_be.split("\n")[i].split("=")[0]
                user = splitted[i].split("=")[0]

                if safe != user:
                    print("is_safe", "line changed", safe, user)
                    return False

            return True
        except Exception as e:
            print("is_safe", e)
            return False
