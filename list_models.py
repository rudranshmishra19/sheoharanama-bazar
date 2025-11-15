from google import genai

client = genai.Client(api_key="AIzaSyBFvwjjH7nFDJWF-gWIScS4O2IIsXHLx5M")

print("Listing models...\n")

pager = client.models.list()

for model in pager:
    print(model.name)
