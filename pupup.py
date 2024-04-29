import subprocess
import sys
def i(t):
	subprocess.check_call([sys.executable,'-m','pip','install',t])
i('aiohttp')
i('websockets')
i('flask')
i('requests')
i('reportlab')
