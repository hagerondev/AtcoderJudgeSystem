import subprocess

cmd = "python atcoder.py"
stdin = "5 8\n"
#returncode = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True).communicate('1 2\n')[0]
stdout = subprocess.run(cmd, shell=True, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(stdout.stdout)