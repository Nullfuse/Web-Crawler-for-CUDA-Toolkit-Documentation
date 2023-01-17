import re
import requests
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

prevEndingIndex = 0

print("Starting Crawler")

for URL in URLs:
  print("Crawling: " + URL)
  lastValue = len(function_value)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="contents")

  member_types = results.find_all(class_=["member_type", "member_long_type"])
  member_names = results.find_all(class_=["member_name", "member_name_long_type"])

  if len(member_types) != len(member_names):
    raise Exception("Size Mismatch")
    
  size = len(member_types)

  for i in range(size):
    member_type_str = member_types[i].text
    member_type_str = "".join(member_type_str.split()) # Remove unnecessary whitespaces
    member_type_str = re.sub(r"[\u200B-\u200D\uFEFF]", "", member_type_str) # Remove zero-width characters
    member_name_str = member_names[i].text
    member_name_str = " ".join(member_name_str.split()) # Remove unnecessary whitespaces
    member_name_str = re.sub(r"[\u200B-\u200D\uFEFF]", "", member_name_str) # Remove zero-width characters
    function_value.append(member_type_str + " " + member_name_str)
    function_completion.append(member_type_str + " " + member_names[i].a.text)
    function_id.append(member_names[i].a.text)
    if not function_value[i + prevEndingIndex].startswith("struct") and not function_value[i + prevEndingIndex].startswith("#define") and not function_value[i + prevEndingIndex].startswith("enum"):
      if re.search("\(", member_name_str):
        member_name_modifiedStr = " "
        for j in range(len(re.findall(r"(,)", member_name_str))): 
          member_name_modifiedStr = member_name_modifiedStr + ", "
        member_name_modifiedStr = "(" + member_name_modifiedStr + ")"
        function_completion[i + prevEndingIndex] = function_completion[i + prevEndingIndex] + " " + member_name_modifiedStr
      else:
        function_completion[i + prevEndingIndex] = function_value[i + prevEndingIndex]
    else:
      function_completion[i + prevEndingIndex] = function_value[i + prevEndingIndex]
    function_value[i + prevEndingIndex] = re.sub(r"_", "\\\\\_", function_value[i + prevEndingIndex])
  prevEndingIndex = prevEndingIndex + size;
print("Crawling Complete")

print("\n")

with open('cuda-functions.json', 'w') as f:
  print("Writing to: " + "cuda-functions.json")
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
  print("Writing to: " + "cuda-common.json")
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