import os 
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key = api_key)

def get_summary(text):
        prompt = """You are a professional writer tasked with summarizing a series of email for a weekly email report. The purpose of this task is to take all the emails
                    a user has received in the last week, and generate a summary of this content. These emails will be somewhat organized - each email will be delimited by a header called \"EMAIL:\" 
                    and that header will contain both the \"SUBJECT\" and the \"BODY\". Otherwise, however, these emails will be provided to you in raw text form, often containing HTML 
                    tags and other irrelevant data that you will need to parse. Moreover, these emails will cover various topics ranging from promotions to newspaper
                    digests to important communications. You should structure your summary with headers digesting the main threads / conversation topics, and then bullet points 
                    covering the important details. The headers should show up bolded when displayed in the email client - for this, you will need to use html <strong>text</strong> tags - this is a MUST HAVE.
                    You should limit the length of your response to a message that is readable within at most three minutes of skimming - so limit your response to 600 words.
                    
                    Here is some example structure that you can follow - this is exactly what will be sent to the users inbox following a week:
                    (example output starts here)
                    **Here is a summary of your emails from the last week**
                    [<strong>Email Thread #1</strong>]
                    [Summary]
                    [<strong>Email Thread #2</strong>]
                    [Summary]
                    ...
                    [<strong>Email Thread #n</strong>]
                    [Summary]
                    **That completes the summary of your inbox!**
                    (example output ends here)
                    Here are the emails that you will need to summarize (emails start here):"""
        
        prompt = prompt + text

        print("called \n")
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        
        return(response.text)

if __name__ == "__main__":

    """ 
    EMAIL:
    SUBJECT: Important meeting on Saturday
    BODY: There's an important meeting on Saturday!
    EMAIL:
    SUBJECT: Domino's Pizza
    BODY: Get 5$ of domino's pizza
    EMAIL:
    SUBJECT: IRS Audit
    BODY: You owe 5k$ in taxes
    EMAIL:
    SUBJECT: Important meeting on Friday
    BODY: There's an important meeting on Friday!
    """
    #get_summary(text)