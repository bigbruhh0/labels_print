import subprocess
import sys
def i(t):
	subprocess.check_call([sys.executable,'-m','pip','install',t])

i('win32printing')
