import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

def generate_text_summary_prompt(text, num_words, tone):
    return f"You are an experienced copywriter. Write a {num_words} words summary the the following text, using a {tone} tone: {text}"

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

segovia_aqueduct_text = """The Aqueduct of Segovia (Spanish: 
Acueducto de Segovia) is a Roman aqueduct in Segovia, Spain. 
It was built around the first century AD to channel water from 
springs in the mountains 17 kilometres (11 mi) away to the 
city's fountains, public baths and private houses, and was in 
use until 1973. 
Its elevated section, with its complete arcade of 167 arches, 
is one of the best-preserved Roman aqueduct bridges and the 
foremost symbol of Segovia, as evidenced by its presence on the 
city's coat of arms. 
The Old Town of Segovia and the aqueduct, were declared a UNESCO 
World Heritage Site in 1985. As the aqueduct lacks a legible 
inscription (one was apparently located in the structure's attic, 
or top portion[citation needed]), the date of construction cannot be 
definitively determined. The general date of the Aqueduct's 
construction was long a mystery, although it was thought to have 
been during the 1st century AD, during the reigns of the Emperors 
Domitian, Nerva, and Trajan. At the end of the 20th century, 
Géza Alföldy deciphered the text on the dedication plaque by 
studying the anchors that held the now missing bronze letters 
in place. He determined that Emperor Domitian (AD 81–96) ordered 
its construction[1] and the year 98 AD was proposed as the most 
likely date of completion.[2] However, in 2016 archeological 
evidence was published which points to a slightly later date, 
after 112 AD, during the government of Trajan or in the 
beginning of the government of emperor Hadrian, 
from 117 AD."""

input_prompt = generate_text_summary_prompt(
    text=segovia_aqueduct_text,
    num_words=20,
    tone="knowledgeable and engaging")

response = llm.invoke(input_prompt)
print(response.content)
