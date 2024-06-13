import asyncio
import pickle
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


class PicklerNotFoundDumpFile(Exception):
    pass


class Pickler:
    def __init__(self, base_temp_dir):
        self.base_temp_dir = Path(base_temp_dir)
        self.base_temp_dir.mkdir(parents=True, exist_ok=True)

    def cache(self, name, obj=None, *args, **kwargs):
        dump_file_path = self.base_temp_dir / f'{name}.pkl'
        if obj is None:
            if dump_file_path.exists():
                with open(dump_file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                raise PicklerNotFoundDumpFile(f'No dump file found for {name}')
        else:
            if dump_file_path.exists():
                with open(dump_file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                if callable(obj):
                    if asyncio.iscoroutinefunction(obj):
                        result = asyncio.run(obj(*args, **kwargs))
                    else:
                        with ThreadPoolExecutor() as executor:
                            result = executor.submit(obj, *args, **kwargs).result()
                else:
                    result = obj

                with open(dump_file_path, 'wb') as f:
                    pickle.dump(result, f)
                return result
