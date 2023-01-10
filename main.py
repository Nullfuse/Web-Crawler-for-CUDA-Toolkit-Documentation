import requests
import re
from bs4 import BeautifulSoup

URLs = ["https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html",
      "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__THREAD__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__ERROR.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXTRES__INTEROP.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EXECUTION.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__OCCUPANCY.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY__POOLS.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__UNIFIED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__PEER.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__OPENGL.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__OPENGL__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D9.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D9__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D10.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D10__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D11.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__D3D11__DEPRECATED.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__VDPAU.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EGL.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__INTEROP.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TEXTURE__OBJECT.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__SURFACE__OBJECT.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART____VERSION.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__GRAPH.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DRIVER__ENTRY__POINT.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__HIGHLEVEL.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DRIVER.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__PROFILER.html",
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html"]

function_id = []
function_value = []
function_completion = []

for URL in URLs:
  print(URL)
  lastValue = len(function_value)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="contents")

  member_types = results.find_all(class_=["member_type", "member_long_type"])
  member_names = results.find_all(class_=["member_name", "member_name_long_type"])
  #descs = results.find_all("dd", class_="shortdesc")

  for member_type in member_types:
    str = member_type.text
    str = "".join(str.split()) # Remove unnecessary whitespaces
    str = re.sub(r"[\u200B-\u200D\uFEFF]", "", str) # Remove zero-width characters
    function_value.append(str)
    function_completion.append(str)
  
  i = lastValue
  for member_name in member_names:
    function_id.append(member_name.a.text)
    str = member_name.text
    str = " ".join(str.split()) # Remove unnecessary whitespaces
    function_value[i] = function_value[i] + " " + str
    function_completion[i] = function_completion[i] + " " + member_name.a.text
    if not function_value[i].startswith("struct") and not function_value[i].startswith("#define") and not function_value[i].startswith("enum"):
      if re.search("\(", str):
        modifiedStr = " "
        for j in range(0, len(re.findall(r"(,)", str))): 
          modifiedStr = modifiedStr + ", "
        modifiedStr = "(" + modifiedStr + ")"
        function_completion[i] = function_completion[i] + " " + modifiedStr
      else:
        function_completion[i] = function_value[i]
    else:
      function_completion[i] = function_value[i]
    i += 1
  
for i in range(0, len(function_value)): 
  print(i)
  print(function_value[i])
  
for i in range(0, len(function_id)): 
  print(i)
  print(function_id[i])

for i in range(0, len(function_completion)): 
  print(i)
  print(function_completion[i])

with open('cuda-functions.json', 'w') as f:
  f.write("{")
  f.write("\n")
  for i in range(0, len(function_value)):
    f.write("\t" + "\"" + function_id[i] + "\"" + ":{" + "\n")
    f.write("\t" + "\t" + "\"" + "id" + "\"" + ":" + " " + "\"" + function_id[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "value" + "\"" + ":" + " " + "\"" + function_value[i] + "\"" + "\n")
    if i == len(function_value) - 1:
      f.write("\t" + "}" + "\n")
    else:
      f.write("\t" + "}," + "\n")
  f.write("}")
  f.close()

with open('cuda-common.json', 'w') as f:
  f.write("{")
  f.write("\n")
  for i in range(0, len(function_completion)):
    f.write("\t" + "\"" + function_id[i] + "\"" + ":{" + "\n")
    f.write("\t" + "\t" + "\"" + "id" + "\"" + ":" + " " + "\"" + function_id[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "value" + "\"" + ":" + " " + "\"" + function_completion[i] + "\"" + "\n")
    if i == len(function_completion) - 1:
      f.write("\t" + "}" + "\n")
    else:
      f.write("\t" + "}," + "\n")
  f.write("}")
  f.close()

#https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html
#https://www.skytowner.com/explore/beautiful_soup_find_all_method
#https://realpython.com/beautiful-soup-web-scraper-python/