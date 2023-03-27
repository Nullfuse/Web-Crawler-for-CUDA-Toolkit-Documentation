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
       "https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html", 
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TYPES.html#group__CUDA__TYPES",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__ERROR.html#group__CUDA__ERROR",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__INITIALIZE.html#group__CUDA__INITIALIZE",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__VERSION.html#group__CUDA__VERSION",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__DEVICE.html#group__CUDA__DEVICE",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__DEVICE__DEPRECATED.html#group__CUDA__DEVICE__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__PRIMARY__CTX.html#group__CUDA__PRIMARY__CTX",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__CTX.html#group__CUDA__CTX",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__CTX__DEPRECATED.html#group__CUDA__CTX__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MODULE.html#group__CUDA__MODULE",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MODULE__DEPRECATED.html#group__CUDA__MODULE__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__LIBRARY.html#group__CUDA__LIBRARY",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MEM.html#group__CUDA__MEM",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__VA.html#group__CUDA__VA",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MALLOC__ASYNC.html#group__CUDA__MALLOC__ASYNC",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__UNIFIED.html#group__CUDA__UNIFIED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__STREAM.html#group__CUDA__STREAM",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__EVENT.html#group__CUDA__EVENT",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__EXTRES__INTEROP.html#group__CUDA__EXTRES__INTEROP",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__MEMOP.html#group__CUDA__MEMOP",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__EXEC.html#group__CUDA__EXEC",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__EXEC__DEPRECATED.html#group__CUDA__EXEC__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__GRAPH.html#group__CUDA__GRAPH",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__OCCUPANCY.html#group__CUDA__OCCUPANCY",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TEXREF__DEPRECATED.html#group__CUDA__TEXREF__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__SURFREF__DEPRECATED.html#group__CUDA__SURFREF__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TEXOBJECT.html#group__CUDA__TEXOBJECT",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__SURFOBJECT.html#group__CUDA__SURFOBJECT",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__TENSOR__MEMORY.html#group__CUDA__TENSOR__MEMORY",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__PEER__ACCESS.html#group__CUDA__PEER__ACCESS",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__GRAPHICS.html#group__CUDA__GRAPHICS",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__DRIVER__ENTRY__POINT.html#group__CUDA__DRIVER__ENTRY__POINT",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__PROFILER__DEPRECATED.html#group__CUDA__PROFILER__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__PROFILER.html#group__CUDA__PROFILER",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__GL.html#group__CUDA__GL",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__GL__DEPRECATED.html#group__CUDA__GL__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D9.html#group__CUDA__D3D9",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D9__DEPRECATED.html#group__CUDA__D3D9__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D10.html#group__CUDA__D3D10",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D10__DEPRECATED.html#group__CUDA__D3D10__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D11.html#group__CUDA__D3D11",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__D3D11__DEPRECATED.html#group__CUDA__D3D11__DEPRECATED",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__VDPAU.html#group__CUDA__VDPAU",
       "https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__EGL.html#group__CUDA__EGL"]

function_id = []
function_value = []
function_completion = []
function_description = []
function_additional_information = []
function_URL = []

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
  member_descriptions = results.find_all("dd", class_="shortdesc")
  member_long_descriptions = results.find_all("dd", class_="description")
  
  if len(member_types) != len(member_names):
    raise Exception("Size Mismatch")
    
  size = len(member_types)
  
  extract_long_description = True;
  
  i = 0
  while i in range(size):
    # Removes irrelvant statements, prevents cases where descriptions get matched up to the wrong function
    if len(member_types) != len(member_long_descriptions):
      n = len(member_types) - len(member_long_descriptions)
      del member_types[:n]
      del member_names[:n]
      del member_descriptions[:n]
      size = size - n
    member_type_str = member_types[i].text
    member_type_str = "".join(member_type_str.split()) # Remove unnecessary whitespaces
    member_type_str = re.sub(r"[\u200B-\u200D\uFEFF]", "", member_type_str) # Remove zero-width characters
    member_name_str = member_names[i].text
    member_name_str = " ".join(member_name_str.split()) # Remove unnecessary whitespaces
    member_name_str = re.sub(r"[\u200B-\u200D\uFEFF]", "", member_name_str) # Remove zero-width characters
    #Get URL
    link_to_member = member_names[i].find("a").get("href")
    function_URL.append("<br>" + "<a href=\\\"" + URL + link_to_member + "\\\">Full Description</a>")
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
    function_value[i + prevEndingIndex] = "<p><b><code>" + function_value[i + prevEndingIndex] + "</code></b></p>" # Apply HTML Markup
    if member_descriptions[i].text:
      function_short_description = member_descriptions[i].text
      function_short_description = " ".join(function_short_description.split()) # Remove unnecessary whitespaces
      function_short_description = re.sub(r"[\u200B-\u200D\uFEFF]", "", function_short_description) # Remove zero-width characters
      function_description.append("<p>" + function_short_description + "</p>") # Apply HTML Markup
    else: 
      function_description.append("") 
    #------------------------------------------------------------------------------------------------------
    # Extract Description
    #------------------------------------------------------------------------------------------------------
    description_output = ""
    if extract_long_description:
      if member_long_descriptions[i].text:
        parameter_header = member_long_descriptions[i].find_all(class_=["parameter_header"])
        parameter_content = member_long_descriptions[i].find_all(class_=["table-display-params"])
        return_header = member_long_descriptions[i].find_all(class_=["return_header"])
        return_content = member_long_descriptions[i].find_all(class_=["return"])
        description_header = member_long_descriptions[i].find_all(class_=["description_header"])
        description_content = member_long_descriptions[i].find_all(class_=["section"])
        description_content = description_content[len(description_content) - 1]
        if parameter_header:
          # Get parameter header and content, remove excess whitespacing, and apply html markup
          description_output = description_output + "<p>" + "<b>" + " ".join(parameter_header[0].text.split()) + "</b>" + "<br>"
          parameter_content_keyword = parameter_content[0].find_all(class_=["keyword keyword apiItemName"])
          parameter_content_description = parameter_content[0].find_all("dd")
          for j in range(len(parameter_content_keyword)):
            description_output = description_output + "<code>" + " ".join(parameter_content_keyword[j].text.split()) + "</code>" + "<br>"
            if " ".join(parameter_content_description[j].text.split()):
              description_output = description_output + "&emsp;" + " ".join(parameter_content_description[j].text.split()) + "<br>"
          description_output = description_output + "</p>" 
        if return_header:
          # Get return header and content, remove excess whitespacing, and apply html markup
          description_output = description_output + "<p>" + "<b>" + " ".join(return_header[0].text.split()) + "</b>" + "<br>"
          for content in return_content:
            description_output = description_output + " ".join(content.text.split()) + "<br>"
          description_output = description_output + "</p>"
    function_additional_information.append(description_output)
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    i += 1
  prevEndingIndex = prevEndingIndex + size
print("Crawling Complete")

print("\n")

function_id_removedDuplicates = []
function_value_removedDuplicates = []
function_completion_removedDuplicates = []
function_description_removedDuplicates = []
function_additional_information_removedDuplicates = []
function_URL_removedDuplicates = []

for i in range(0, len(function_id)):
  if function_id[i] not in function_id_removedDuplicates:
    function_id_removedDuplicates.append(function_id[i])
    function_value_removedDuplicates.append(function_value[i])
    function_completion_removedDuplicates.append(function_completion[i])
    function_description_removedDuplicates.append(function_description[i])
    function_additional_information_removedDuplicates.append(function_additional_information[i])
    function_URL_removedDuplicates.append(function_URL[i])

with open('cuda-functions.json', 'w') as f:
  print("Writing to: " + "cuda-functions.json")
  f.write("{")
  f.write("\n")
  for i in range(0, len(function_value_removedDuplicates)):
    f.write("\t" + "\"" + function_id_removedDuplicates[i] + "\"" + ":{" + "\n")
    f.write("\t" + "\t" + "\"" + "id" + "\"" + ":" + " " + "\"" + function_id_removedDuplicates[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "value" + "\"" + ":" + " " + "\"" + function_value_removedDuplicates[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "description" + "\"" + ":" + " " + "\"" + function_description_removedDuplicates[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "additional_information" + "\"" + ":" + " " + "\"" + function_additional_information_removedDuplicates[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "url" + "\"" + ":" + " " + "\"" + function_URL_removedDuplicates[i] + "\"" + "\n")
    if i == len(function_value_removedDuplicates) - 1:
      f.write("\t" + "}" + "\n")
    else:
      f.write("\t" + "}," + "\n")
  f.write("}")
  f.close()
  print("Writing to " + "cuda-functions.json" + " Complete")

with open('cuda-common.json', 'w') as f:
  print("Writing to: " + "cuda-common.json")
  f.write("{")
  f.write("\n")
  for i in range(0, len(function_completion_removedDuplicates)):
    f.write("\t" + "\"" + function_id_removedDuplicates[i] + "\"" + ":{" + "\n")
    f.write("\t" + "\t" + "\"" + "id" + "\"" + ":" + " " + "\"" + function_id_removedDuplicates[i] + "\"" + "," + "\n")
    f.write("\t" + "\t" + "\"" + "value" + "\"" + ":" + " " + "\"" + function_completion_removedDuplicates[i] + "\"" + "\n")
    if i == len(function_completion_removedDuplicates) - 1:
      f.write("\t" + "}" + "\n")
    else:
      f.write("\t" + "}," + "\n")
  f.write("}")
  f.close()
  print("Writing to " + "cuda-common.json" + " Complete")

print("\nProgram Complete")
