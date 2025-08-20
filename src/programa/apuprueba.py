from google import genai
request=input("que quieres preguntar?")
client = genai.Client(api_key="AIzaSyA_7BCTj1dqnBmEEMTBi_FUq7qe8c03Dgk")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=request
)
print(response.text)
