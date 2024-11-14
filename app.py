import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound  # this YoutubeTranscriptApi is responsible for fetching the transcript from the yoututbe video url 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # # done with configuring the fetching the gemini ap_key

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """



def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]  # For any youtube url consist of unique id of video, we need to extract the unique id from the url after splitting the url 1st index have the id 
        

        # No transcripts were found for any of the requested language codes: ('en',) For this video  transcripts are available in the following languages: (MANUALLY CREATED) english, hindi all languages
        # Attempt to get English transcript first; if not available, fall back to Hindi.
        try:
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])  # # so this function get_transcript helps us to fetch the transcript from the youtube video when we pass the argument of respected unique id youtube video url 
        except NoTranscriptFound:
            # Attempt to get Hindi transcript if English is not found.
            transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        
        # Combine the transcript parts into a single string
        transcript = " ".join([i["text"] for i in transcript_text])
        
        return transcript

    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.error("No transcript available for this video in the specified languages.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):  # # this function is responsible for generating the content summarizer by utilizing the prompt and youtube video Transcript

    model=genai.GenerativeModel("gemini-pro")  # # once i get this gemini-pro model which is responsible for in working text
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:  # # As soons as we provideo the youtube link by this code it will show the youtube video thumbnail in the botton 
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)  # we are going to use st.image to display the youtube video thumbnail image, and this taken url is default url whenever we are going to upload the youtube video thumbnail image this is where its going to store by taking the unique value of youtube video

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)






