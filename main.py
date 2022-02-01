import requests
from bs4 import BeautifulSoup as bs
import os
import subprocess
import sys
sys.path.append("C:/Users/yutak/program/module")
import time
import twitter
import json

#attach color
from termcolor import colored, cprint
import colorama
colorama.init()

parent = "C:/Users/yutak/program/AtcoderJudgeSystem/"
url = "https://atcoder.jp/contests/"

def getNoPro():
	d = sys.argv
	if len(d)==3:
		no,pro = d[1],d[2]
		with open(parent+"Samples/history.txt", mode="w") as f:
			f.write(no+" "+pro)
		return no,pro
	elif len(d)==2:
		pro = d[1]
		with open(parent+"Samples/history.txt", mode="r") as f:
			l = f.read()
		with open(parent+"Samples/history.txt", mode="w") as f:
			no = l.split()[0]
			f.write(no+" "+pro)
		return no,pro
	elif len(d)==1:
		with open(parent+"Samples/history.txt", mode="r") as f:
			l = f.read()
			no,pro = l.split()
		return no,pro
	else:
		print("Error: Too many argument")
		exit(1)

def setURL(no,pro):
	global url
	url = url + no + "/tasks/" + no + "_" + pro

def gotSample(no,pro):
	print(parent+"Samples/"+no+"/"+pro+".txt")
	if os.path.exists(parent+"Samples/"+no+"/"+pro+".txt"):
		return 1
	else:
		return 0

def getSample():
	res = requests.get(url)
	soup = bs(res.text, "html.parser")
	sampleIn = []
	sampleOut = []
	for i in soup.find_all("div", class_="part"):
		if "入力例" in i.text:# or "Sample Input" in i.text:
			sampleIn.append(i.find("pre").text[:-2].split("\r\n"))
		if "出力例" in i.text:# or "Sample Output" in i.text:
			sampleOut.append(i.find("pre").text[:-2].split("\r\n"))
	return sampleIn,sampleOut

def writeSample(s,no,pro):
	if not os.path.exists(parent+"Samples/"+no):
		os.makedirs(parent+"Samples/"+no, exist_ok=True)

	sampleIn = s[0]
	sampleOut = s[1]
	#c = "(['"+"','".join(sampleIn)+"'],['"+"','".join(sampleOut)+"'])"
	c = "([["
	for i in sampleIn:
		for j in i:
			c = c + "'" + j + "',"
		c = c[:-1]+"],["
	c = c[:-2]+"],[["
	for i in sampleOut:
		for j in i:
			c = c + "'" + j + "',"
		c = c[:-1]+"],["
	c = c[:-2]+"])"

	with open(parent+"Samples/"+no+"/"+pro+".txt", mode="w") as f:
		#f.write(c)
		f.write(json.dumps(sampleIn)+"\n"+json.dumps(sampleOut))
	return 0

def readSample(no,pro):
	with open(parent+"Samples/"+no+"/"+pro+".txt", mode="r") as f:
		sampleIn = json.loads(f.readline())
		sampleOut = json.loads(f.readline())
	return (sampleIn, sampleOut)

def judgeSample(sample):
	boo = 1
	cmd = "python atcoder.py"
	for i in range(len(sample[0])):
		sample[0][i].append("\n")
	for i in range(len(sample[0])):
		stdin = "\n".join(sample[0][i])+"\n"
		start = time.time()
		stdout = subprocess.run(cmd, shell=True, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		dotime = str(round((time.time()-start)*1000)-60)
		if int(dotime)>3500:
			boo = 0
			print("TestCase"+str(i+1)+" :",colored(" TLE ","white","on_red",attrs=["bold"]),dotime+"ms")
		else:
			if "\n".join(sample[1][i])+"\n"==stdout.stdout:
				print("TestCase"+str(i+1)+" :",colored(" AC ","white","on_green",attrs=["bold"]),dotime+"ms")
			else:
				print("TestCase"+str(i+1)+" :",colored(" WA ","white","on_red",attrs=["bold"]),dotime+"ms")
				print("  <Your Output>")
				ssp = stdout.stdout.split("\n")
				if stdout.stderr!="":
					print(stdout.stderr)
				for j in range(len(ssp)-1):
					print(">>",ssp[j])
				print("  <Correct Answer>")
				for j in sample[1][i]:
					print(">>",j)

				#for submit boo
				boo = 0
		print()
	return boo

def submit(no,pro):
	print(url)
	cmd = "python " + parent+"submit.py " + url
	#print(cmd)
	stdout = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	res = stdout.stdout
	if "AC" in res:
		print(no.upper(),pro.upper(),":",colored(" AC ","white","on_green",attrs=["bold"]))
		twitter.post("[AJS developed by hageron]\n"+no.upper()+"の"+pro.upper()+"問題をACしました！\n#ajs_hageron\n"+url)
	else:
		print(no.upper(),pro.upper(),":",colored(" {0} ".format(res[:-1]),"white","on_red",attrs=["bold"]))

def main():
	no,pro = getNoPro()
	setURL(no,pro)

	s = -1
	#sampleを取得していなかったら取得する
	if not gotSample(no,pro):
		s = getSample()
		writeSample(s,no,pro)
		#print(s)

	#sampleをフォルダから読み込む
	samples = readSample(no,pro)
	#print(arr)

	#sampleをジャッジする
	res = judgeSample(samples)

	#submit
	if res==1:
		print('SUBMIT...')
		submit(no,pro)
		#print("SUBMITED") -> submit.py
	else:
		print("TRY AGAIN")

def test(sample):
	cmd = "python atcoder.py"
	for i in range(len(sample[0])):
		stdin = "\n".join(sample[0][i])+"\n"
		start = time.time()
		stdout = subprocess.run(cmd, shell=True, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		dotime = str(round((time.time()-start)*1000)-60)
		if "\n".join(sample[1][i])+"\n"==stdout.stdout:
			print("TestCase"+str(i+1)+" :","AC",dotime+"ms")
		else:
			print("TestCase"+str(i+1)+" :","WA",dotime+"ms")
			print("  <Your Output>")
			ssp = stdout.stdout.split("\n")
			if stdout.stderr!="":
				print(stdout.stderr)
			for i in range(len(ssp)-1):
				print(">>",ssp[i])
			print("  <Correct Answer>")
			for i in sample[1][i]:
				print(">>",i)

main()
exit()