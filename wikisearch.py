import wikipedia
import sys
from main import speak

query = ' '.join(sys.argv[1:])
print(query)
speak("Searching wikipedia")
results = wikipedia.summary(query, sentences=2)
speak(f"According to wikipedia...{results}")
