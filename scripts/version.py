from dataclasses import dataclass
import enum
import os
import sys
from typing import Generic, TypeVar, NoReturn


OkType = TypeVar("OkType")
ErrType = TypeVar("ErrType", bound=Exception)


class Ok(Generic[OkType]):
    def __init__(self, value: OkType) -> None:
        self._value = value

    def unwrap(self) -> OkType:
        return self._value


class Err(Generic[ErrType]):
    def __init__(self, exception: ErrType) -> None:
        self._exception = exception

    def unwrap(self) -> NoReturn:
        raise self._exception


Result = Ok[OkType] | Err[ErrType]


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def incr(self) -> None:
        self.patch += 1
        if self.patch > 9:
            self.patch = 0
            self.minor += 1
        if self.minor > 9:
            self.minor = 0
            self.major += 1


class FileType(enum.Enum):
    TOML= "toml"
    ENV= "env"


def read_version(path: str, ty: FileType = FileType.ENV) -> Version:
    with open(path, "r") as f:
        match ty:
            case FileType.TOML:
                temp = f.read().strip().split("=")[-1].strip().strip('"')
                major, minor, patch = temp.split(".")
                return Version(int(major), int(minor), int(patch))
            case FileType.ENV:
                temp = f.read().strip().split("$")[-1].strip("{").strip("}")
                major, minor, patch = temp.split(".")
                return Version(int(major), int(minor), int(patch))


def write_version(path: str, version: Version) -> None:
    with open(path, "w") as f:
        f.write(f'version = "{version}"')


def main() -> None:
    args: list[str] = sys.argv
    paths: list[str] = ["../.env", ".env"]
    # paths: list[str] = ["../version.toml", "version.toml"]
    versions: list[Result[tuple[str, Version]]] = [
        Ok((path, read_version(path))) for path in paths if os.path.exists(path)
    ]

    if len(versions) == 0:
        print("No version file found.")
        sys.exit(1)

    version: Version = versions[0].unwrap()[1]
    path: str = versions[0].unwrap()[0]

    if len(args) != 2:
        print("Usage: python3.10 version.py <action>")
        sys.exit(1)

    action: str = args[1]
    if action == "incr":
        version.incr()
        write_version(path, version)
    if action == "tag":
        os.system(f'git tag -a v{version} -m "Release v{version}"')
        os.system(f"git push --tags")
    if action == "get":
        os.system("export VERSION=v" + str(version) + "")


if __name__ == "__main__":
    main()
