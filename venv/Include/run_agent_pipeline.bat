%
@ECHO OFF
cls
REM set your own python interpreter path
set python_interpreter_path=C:\Users\hadu01\AppData\Local\Continuum\Anaconda3\envs\py35\python.exe
start %python_interpreter_path% run_agent.py -port 195.154.161.119:4399
start %python_interpreter_path% run_agent.py -port 195.154.161.119:4398