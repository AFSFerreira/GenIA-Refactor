def write_file(file_path: str, content: str) -> None:
  with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)
