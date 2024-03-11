from gpt4all import GPT4All
import scratchattach as scratch3
import os

chars = [
    "", "", "", "", "", "", "", "", "", " ", "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
    "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "`",
    "~", "-", "=", ",", ".", "/", ";", "'", "[", "]", "\\", "|", "}", "{",
    "\"", ":", "?", ">", "<", "_", "+", ")", "(", "*", "&", "^", "%", "$", "#",
    "@", "!", "¶", "\r"
]
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")


def ask_gpt4all(prompt, model, mt):
  output = model.generate(prompt, temp=0, max_tokens=mt)
  print('Output: ' + output)
  return output


def encode(data, username):
  newData = ""
  for letter in username:
    newData = newData + str(chars.index(letter) + 1)
  newData = newData + "."
  for letter in data:
    try:
      newData = newData + str(chars.index(letter) + 1)
    except:
      print("error!!! " + letter)
  print('Encoded: ' + newData)
  return newData


def decode(data):
  newData = ""
  usernameHappened = False
  i = 0
  while i < len(data):
    if (i % 2 == 1
        and usernameHappened == False) or (i % 2 == 0
                                           and usernameHappened == True):
      fullNumber = str(data[i - 1]) + str(data[i])
      fullNumber = fullNumber.replace(" ", "")

      try:
        newData = newData + chars[int(fullNumber.replace(".", "")) - 1]
      except:
        print(f"ERROR: {int(fullNumber.replace('.', '')) - 1} doesn't work!")
    elif data[i] == ".":
      print("Username: " + newData)
      username = newData
      usernameHappened = True
      newData = ""
    i += 1

  print("Decoded result:", newData)
  return newData, username


def get_prompt():
  cloudVar = scratch3.get_var("967781599",
                              "Question")  # To get a cloud variable
  return cloudVar


def set_answer(data):
  conn.set_var("Response", data)
  print("Sent!")


def doTheStuff(prompt):
  decodedQuestion = decode(prompt)
  mt = (256 - (len(decodedQuestion[1]) * 2) + 1) // 10
  print('Max tokens: ' + str(mt))
  data = ask_gpt4all(decodedQuestion[0], model, mt)
  data = data.replace("\n", "¶")
  data = data.replace("\r", "¶")
  encodedData = encode(data.lower(), decodedQuestion[1].lower())
  set_answer(encodedData)


sID = os.environ['SESSIONID']
conn = scratch3.CloudConnection(project_id="967781599",
                                username="SupKittyMeow",
                                session_id=sID)
oldVar = get_prompt()
print('Ready!')
while True:
  prompt = get_prompt()
  if not oldVar == prompt and not prompt == None:
    oldVar = prompt
    doTheStuff(prompt)
