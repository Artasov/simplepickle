# Introduction to `simplepickle`

`simplepickle` это простой пайтон пакет позволяющий
удобно получать загружать файлы dump от pickle.

## Dependencies

* Python 3.11 or higher

## Quick Start
* #### Install `simplepickle`
  ```sh
  pip install simplepickle
  ```
* ## Run the example twice to understand everything.
  ```python
  import asyncio
  import os
  from pathlib import Path
  from time import sleep
  
  from simplepickle import Pickler, PicklerNotFoundDumpFile
  
  # I advise you to define paths for storing temporary files
  BASE_DIR = Path(__file__).resolve().parent.parent
  BASE_TEMP_DIR = os.path.join(BASE_DIR, 'temp')
  
  pickler = Pickler(BASE_TEMP_DIR)
  
  # Caching a simple object.
  some_obj = pickler.cache('DumpFileNameSimpleObj', {'A': ['B', 3]})
  print(some_obj)
  
  # Using this method, it immediately checks whether 
  # there is such a dump file and loads it if available, 
  # and if not, it saves it.
  
  # Caching a synchronous function
  def work(arg1, arg2):
      sleep(2)
      return arg1 * arg2
  
  work_result = pickler.cache(name='DumpFileNameSyncFunction', obj=work, arg1=5, arg2=3)
  print(work_result)
  
  
  # Asynchronous function
  async def async_work(arg1, arg2):
      await asyncio.sleep(2)
      return arg1 * arg2
  
  async_work_result = pickler.cache(name='DumpFileNameAsyncFunction', obj=async_work, arg1=55, arg2=10)
  print(async_work_result)
  
  # Nobody bothers you to make it longer...
  try:
      result = pickler.cache('DumpFileNameSomethingFuncResult')
  except PicklerNotFoundDumpFile:
      result = work(30, 60)
      pickler.cache('DumpFileNameSomethingFuncResult', result)
  print(result)
  ```