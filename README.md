# Ask 15K LLMs the same question!
## As of 6-27-25 there are >14K Ollama servers open on TCP port 11434 accoring to Shodan: `https://www.shodan.io/search?query=port%3A11434+product%3A%22Ollama%22`
## Let's ask all of them a question!

* Create a file with your question, e.g. `echo "How many R's are in the word strawberry?" > query.txt`
* Create a file with a list of IPs with open Ollama servers that you got from Shodan or other, e.g. `ol.txt`\
* Run it! `python3 ollama-query.py --file ol.txt --query query.txt --output replies.txt --debug`
* Find out how many R's there REALLY are in strawberry!

