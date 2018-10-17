import os, time
import paramiko
import bz2
import csv
import datetime

now = datetime.datetime.now()

def sendFile(added):
  ssh = paramiko.SSHClient() 
  ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
  ssh.connect("192.168.5.254", username="root", password="lago")
  sftp = ssh.open_sftp()
  sftp.put(localpath, remotepath)
  sftp.close()
  ssh.close()

def cleanUp(file):
  bz_file = bz2.BZ2File("./" + file)
  line_list = bz_file.readlines()
  csv_lines = []
  temperature = ""
  pressure = ""
  altitude = ""
  computer = ""
  dateTime = ""
  place = "UNIVERSIDAD DEL VALLE CAMPUS CENTRAL"
  for line in line_list:
    line = line.decode()
    if line.find("# x s")!=-1:
      line_split = line.split(" ")
      temperature = line_split[3] + line_split[4]
      pressure = line_split[5] + line_split[6]
      altitude = line_split[7] + line_split[8].replace('\n', '')
    if line.find("# # This file was started on ")!=-1:
      line_split = line.split(" ")
      computer = line_split[7].replace('\n', '')
    if line.find("# x h")!=-1:
      line_split = line.split(" ")
      dateTime = line_split[5] + line_split[6]
    if line.find("#")==-1:
      line_split = line.split(" ")
      csv_lines.append([line_split[0],dateTime,temperature,pressure,altitude,computer,place,1])
  with open('./DATA/gtLago.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    csv.excel.delimiter='|'
    writer = csv.writer(outfile, dialect=csv.excel)
    for line in csv_lines:
      writer.writerow(line)
  outfile.close()
  bz_file.close()


path_to_watch = "D://UVG/MP/Services/LimpiezaDatos/"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (1)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added: 
    cleanUp(added[0])
    print ("Added: ", ", ".join (added))
  if removed: print("Removed: ", ", ".join (removed))
  before = after