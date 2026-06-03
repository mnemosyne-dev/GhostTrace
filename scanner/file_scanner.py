import os


SUPPORTED = (
    ".txt",
    ".pdf",
    ".csv",
    ".json",
    ".log"
)


def scan_directory(folder):

    found = []

    for root, dirs, files in os.walk(folder):

        for file in files:

            if file.lower().endswith(SUPPORTED):

                found.append(
                    os.path.join(root,file)
                )

    return found