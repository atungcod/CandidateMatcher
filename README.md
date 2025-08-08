# Candidate Match Engine
This application recommends the best candidates for a job based on relevance.

- Accepts a job description (text input)

- Accept a list of candidate resumes (via file upload or text input)

- Generate embeddings

- Compute the cosine similarity between the job and each resume

- Display the top 5–10 most relevant candidates, including:

- Name or ID

- Similarity score

- AI-generated summary describing why this person is a great fit for this role.

## KEY ASPECTS
- AI-generated summaries for each candidate on the display page after matching.
- Various ways to input resumes on the home page.
- Errors show up if there were issues with uploads, generation, or matching.
- Question icons throughout the app provide additional help for the user on how to interact with it.
- Candidates are ranked on the display page from most to least qualified, showing their matching score. The app shows if they are an excellent, good, or fair candidate based on cosine similarity and score checking.
- User is able to download the rankings as a CSV file to share.
