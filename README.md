# Candidate Match Engine
This application recommends the best candidates for a job based on relevance.

-Accepts a job description (text input)

-Accept a list of candidate resumes (via file upload or text input)

-Generate embeddings

-Compute the cosine similarity between the job and each resume

-Display the top 5–10 most relevant candidates, including:

-Name or ID

-Similarity score

-AI-generated summary describing why this person is a great fit for this role.

## PROCESS
1. Entered the basic prompt into Replit to create a framework to build off of. I took note of the UI/UX and identified areas of improvement. Understood the pages and inputs from the user.
2. Set up API key for GoogleAI to help with candidate summary generation based on their resume and the role description, used Cursor to help with debugging.
3. Asked the Replit agent and ChatGPT to make suggestions to the current UI, picked the aspects I wanted to include.
4. Prompted Replit agent to improve the UI to make the app stand out more while staying user-friendly. Created two separate pages (home screen for entering information and display page for information about top candidates). Adjusted the text on screen to be more descriptive.
5. Used ChatGPT to create sample resumes to test the inputs and matching system.

## KEY ASPECTS
- AI-generated summaries for each candidate on the display page after matching.
- Various ways to input resumes on the home page.
- Errors show up if there were issues with uploads, generation, or matching.
- Question icons throughout the app provide additional help for the user on how to interact with it.
- Candidates are ranked on the display page from most to least qualified, showing their matching score. The app shows if they are an excellent, good, or fair candidate based on cosine similarity and score checking.
