import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
res = openai.File.create(file=open("myfile_pia.jsonl"), purpose='answers')
print(res)