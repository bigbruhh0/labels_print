import subprocess
import sys
def i(t):
	subprocess.check_call([sys.executable,'-m','pip','install',t])

i('Plyer')
i('aiohttp')
i('requests')
i('flask')
i('websockets')
i('reportlab')

