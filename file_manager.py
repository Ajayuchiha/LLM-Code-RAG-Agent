import os

class FileManager:

    @staticmethod
    def list_files(base="codebase"):
        out = []
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith((".py", ".json", ".txt", ".md")):
                    out.append(os.path.join(root, f))
        return out

    @staticmethod
    def read(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write(path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Updated {path}"

    @staticmethod
    def apply_diff(path, diff_text):
        """
        Simple unified diff. LLM-friendly.
        """
        original = FileManager.read(path)
        lines = original.splitlines(keepends=True)
        new_content = []

        for line in diff_text.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                new_content.append(line[1:] + "\n")
            elif not line.startswith("-"):
                new_content.append(line + "\n")

        FileManager.write(path, "".join(new_content))
        return f"Patched {path}"
