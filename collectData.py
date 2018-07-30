#Jason Ivey 2018
import time
import subprocess
import envoy

def readSMI():
	return subprocess.check_output(['nvidia-smi'])

def getTemp(smi):
	index = smi.index("C  ")
	return smi[(index - 4):(index)].strip() 

def getMemUse(smi):
	index = smi.index("MiB /  ")
	return smi[(index - 4):(index)].strip() 

def getPowerUse(smi):
	index = smi.index("/  N/A ")
	return smi[(index - 4):(index - 2)].strip() 

def getUtilization(smi):
	index = smi.index("     Default")
	return smi[(index - 4):(index-2)].strip() 

def getCPUUse():
	search = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
	r = envoy.run(search)
	return r.std_out.strip('\n')

def getRAMUse():
	search = "free -b | awk 'FNR == 2 {print $3/($3+$4)*100}'"
	r = envoy.run(search)
	temp =  '{0:.10f}'.format(int(float(r.std_out) * 67371708416 ))
	return temp[0:temp.index(".")]


tempText = "GPU TEMP,GPU MEMORY USE,GPU POWER USE,GPU CORE UTILIZATION,CPU USE PERCENTAGE,RAM USE IN BYTES\n"
count = 0
output = open("GPUinfo.txt", "a")
while True:
	try:
		smi = readSMI()
		tempText += getTemp(smi)+","+getMemUse(smi)+","+getPowerUse(smi)+","+getUtilization(smi)+","+getCPUUse()+","+getRAMUse()+"\n"
		count = count + 1
		print(getTemp(smi)+","+getMemUse(smi)+","+getPowerUse(smi)+","+getUtilization(smi)+","+getCPUUse() +","+getRAMUse() )
		if count % 1000 == 0 :
			output.write(tempText)
			tempText = ""
		time.sleep(.222)
	except KeyboardInterrupt:
		print("Saving info")
		output.write(tempText)
		exit(0)

