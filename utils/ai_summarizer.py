import os
import json
from openai import OpenAI
from typing import Optional

class AISummarizer:
    """Generate AI-powered summaries explaining candidate fit for job roles"""
    
    def __init__(self):
        """Initialize the AI summarizer with OpenAI client"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.model = "gpt-4o"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        self.is_available = False
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.is_available = True
            except Exception:
                self.is_available = False
        else:
            self.is_available = False
    
    def generate_fit_summary(
        self, 
        job_description: str, 
        resume_content: str, 
        similarity_score: float
    ) -> str:
        """
        Generate an AI summary explaining why a candidate is a good fit
        
        Args:
            job_description: The job description text
            resume_content: The candidate's resume content
            similarity_score: The calculated similarity score
            
        Returns:
            str: AI-generated summary explaining the fit
            
        Raises:
            Exception: If summary generation fails
        """
        if not self.is_available:
            raise Exception("OpenAI API key not provided. Please add your OPENAI_API_KEY to enable AI summaries.")
        
        try:
            prompt = self._create_summary_prompt(
                job_description, 
                resume_content, 
                similarity_score
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR analyst and recruiter. Your job is to analyze how well a candidate matches a job description and provide clear, actionable insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate AI summary: {str(e)}")
    
    def _create_summary_prompt(
        self, 
        job_description: str, 
        resume_content: str, 
        similarity_score: float
    ) -> str:
        """Create the prompt for AI summary generation"""
        
        score_percentage = similarity_score * 100
        
        prompt = f"""
Analyze the match between this job description and candidate resume:

JOB DESCRIPTION:
{job_description[:2000]}  # Truncate to avoid token limits

CANDIDATE RESUME:
{resume_content[:2000]}  # Truncate to avoid token limits

SIMILARITY SCORE: {score_percentage:.1f}%

Please provide a concise analysis (2-3 paragraphs) covering:

1. **Key Strengths**: What makes this candidate a good fit? Identify specific skills, experience, or qualifications that align with the job requirements.

2. **Potential Concerns**: What might be missing or concerning? Are there any gaps in experience or skills?

3. **Overall Assessment**: Based on the {score_percentage:.1f}% similarity score, provide a brief recommendation about this candidate's suitability.

Keep your response professional, specific, and actionable for hiring managers. Focus on concrete evidence from the resume that supports your assessment.
"""
        
        return prompt
    
    def generate_batch_summaries(
        self, 
        job_description: str, 
        candidates_data: list
    ) -> list:
        """
        Generate summaries for multiple candidates in batch
        
        Args:
            job_description: The job description text
            candidates_data: List of candidate dictionaries with 'content' and 'similarity'
            
        Returns:
            list: List of generated summaries
        """
        summaries = []
        
        for candidate in candidates_data:
            try:
                summary = self.generate_fit_summary(
                    job_description,
                    candidate['content'],
                    candidate['similarity']
                )
                summaries.append(summary)
            except Exception as e:
                summaries.append(f"Could not generate summary: {str(e)}")
        
        return summaries
    
    def generate_comparison_summary(
        self, 
        job_description: str, 
        top_candidates: list
    ) -> str:
        """
        Generate a summary comparing multiple top candidates
        
        Args:
            job_description: The job description text
            top_candidates: List of top candidate data
            
        Returns:
            str: AI-generated comparison summary
        """
        try:
            candidates_summary = "\n".join([
                f"Candidate {i+1}: {candidate['name']} (Score: {candidate['similarity']:.1%})\n"
                f"Key highlights: {candidate['content'][:200]}...\n"
                for i, candidate in enumerate(top_candidates[:5])  # Limit to top 5
            ])
            
            prompt = f"""
Based on this job description and the top candidates, provide a brief comparison:

JOB DESCRIPTION:
{job_description[:1500]}

TOP CANDIDATES:
{candidates_summary}

Please provide a 2-3 paragraph summary that:
1. Compares the strengths of the top candidates
2. Identifies which candidate profiles are most suitable for different aspects of the role
3. Provides hiring recommendations

Keep it concise and actionable for hiring decisions.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR analyst specializing in candidate comparison and hiring recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Failed to generate comparison summary: {str(e)}")
    
    def check_api_availability(self) -> bool:
        """
        Check if OpenAI API is available and working
        
        Returns:
            bool: True if API is working, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False
