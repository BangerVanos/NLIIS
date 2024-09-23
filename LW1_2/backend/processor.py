from pathlib import Path


class Processor:

    def __init__(self, db_folders: list[str], query: str) -> None:
        self._files = None
        self._query = query
    
    

    