import re
import nltk
import spacy
import numpy as np
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Load spaCy model for NLP
try:
    nlp = spacy.load(r"myenv\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.7.1")
except:
    import subprocess
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_md'])
    nlp = spacy.load('en_core_web_md')

class ResumeProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        # Comprehensive skills database
        self.skills_list = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift', 'kotlin'],
            'data_science': ['machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy'],
            'databases': ['sql', 'mongodb', 'postgresql', 'mysql', 'oracle', 'redis', 'cassandra', 'firebase'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd', 'terraform'],
            'web': ['react', 'angular', 'vue', 'django', 'flask', 'node.js', 'html', 'css', 'javascript'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'project management', 'agile', 'scrum']
        }
        
        self.all_skills = []
        for category in self.skills_list.values():
            self.all_skills.extend(category)
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF read error: {str(e)}")
    
    def advanced_nlp_clean(self, text):
        """Advanced NLP text cleaning with lemmatization"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Process with spaCy for better tokenization
        doc = nlp(text)
        
        # Lemmatization and remove stopwords
        cleaned_tokens = []
        for token in doc:
            if (not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2 and
                not token.is_space):
                cleaned_tokens.append(token.lemma_)
        
        return " ".join(cleaned_tokens)
    
    def extract_entities_nlp(self, text):
        """Extract named entities using spaCy"""
        doc = nlp(text)
        entities = {
            'skills': [],
            'education': [],
            'experience': [],
            'certifications': []
        }
        
        # Pattern matching for skills
        for skill in self.all_skills:
            if skill in text.lower():
                entities['skills'].append(skill.title())
        
        # Extract education entities
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'b.tech', 'm.tech', 'b.e', 'm.e', 'b.sc', 'm.sc']
        for sent in doc.sents:
            sent_text = sent.text.lower()
            for edu in education_keywords:
                if edu in sent_text:
                    entities['education'].append(sent.text)
                    break
        
        # Extract experience using regex
        exp_patterns = [
            r'(\d+)\+?\s*years? of experience',
            r'experience\s*:\s*(\d+)',
            r'(\d+)\s*\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text.lower())
            if match:
                entities['experience'].append(match.group(0))
        
        return entities
    
    def semantic_similarity(self, text1, text2):
        """Calculate semantic similarity using spaCy word vectors"""
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        
        if doc1.vector_norm == 0 or doc2.vector_norm == 0:
            return 0.0
        
        similarity = doc1.similarity(doc2)
        return similarity * 100
    
    def tfidf_similarity(self, text1, text2):
        """Calculate TF-IDF based similarity"""
        vectorizer = TfidfVectorizer(max_features=1000)
        try:
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity * 100
        except:
            return 0.0
    
    def extract_key_phrases(self, text):
        """Extract key phrases using TextBlob and spaCy"""
        doc = nlp(text)
        
        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 4]
        
        # Extract keywords using TextBlob
        blob = TextBlob(text)
        keywords = [word.lower() for word in blob.noun_phrases if len(word) > 3]
        
        # Combine and deduplicate
        all_phrases = list(set(noun_phrases + keywords))
        return all_phrases[:20]  # Return top 20
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of resume (positive/negative tone)"""
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if sentiment_score > 0.3:
            sentiment = "Very Positive"
        elif sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score > -0.3:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
        
        return {
            'sentiment': sentiment,
            'score': sentiment_score,
            'subjectivity': subjectivity
        }
    
    def calculate_match_score(self, resume_text, job_text):
        """Calculate match score using multiple NLP techniques"""
        
        # Clean texts with advanced NLP
        clean_resume = self.advanced_nlp_clean(resume_text)
        clean_job = self.advanced_nlp_clean(job_text)
        
        # 1. Semantic similarity (spaCy word vectors) - 40%
        semantic_score = self.semantic_similarity(clean_resume, clean_job)
        
        # 2. TF-IDF similarity - 30%
        tfidf_score = self.tfidf_similarity(clean_resume, clean_job)
        
        # 3. Keyword matching - 20%
        resume_words = set(clean_resume.split())
        job_words = set(clean_job.split())
        
        if job_words:
            common_words = resume_words.intersection(job_words)
            keyword_score = (len(common_words) / len(job_words)) * 100
        else:
            keyword_score = 0
        
        # 4. Entity matching (skills, education) - 10%
        resume_entities = self.extract_entities_nlp(resume_text)
        job_entities = self.extract_entities_nlp(job_text)
        
        entity_score = 0
        if job_entities['skills']:
            skill_matches = len([s for s in resume_entities['skills'] if s.lower() in [js.lower() for js in job_entities['skills']]])
            entity_score = (skill_matches / len(job_entities['skills'])) * 100
        
        # Weighted final score
        final_score = (
            semantic_score * 0.40 +
            tfidf_score * 0.30 +
            keyword_score * 0.20 +
            entity_score * 0.10
        )
        
        return round(final_score, 2)
    
    def extract_skills(self, text):
        """Extract skills using NLP"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.all_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Remove duplicates
        unique_skills = []
        for skill in found_skills:
            if skill not in unique_skills:
                unique_skills.append(skill)
        
        return unique_skills
    
    def generate_detailed_feedback(self, resume_text, job_text, score):
        """Generate detailed feedback using NLP analysis"""
        feedback = []
        
        # Sentiment analysis
        sentiment = self.analyze_sentiment(resume_text)
        feedback.append(f"📊 **Tone Analysis:** {sentiment['sentiment']} (Score: {sentiment['score']:.2f})")
        
        # Key phrases extraction
        key_phrases = self.extract_key_phrases(resume_text)
        top_phrases = key_phrases[:5]
        if top_phrases:
            feedback.append(f"💡 **Key Strengths:** {', '.join(top_phrases[:3])}")
        
        # Entity extraction
        entities = self.extract_entities_nlp(resume_text)
        if entities['education']:
            feedback.append(f"🎓 **Education:** {entities['education'][0][:100]}")
        
        if entities['experience']:
            feedback.append(f"💼 **Experience:** {entities['experience'][0]}")
        
        # Score-based recommendations
        if score >= 80:
            feedback.append("✅ **Excellent match! Strongly recommend for interview.**")
        elif score >= 65:
            feedback.append("👍 **Good match. Schedule for interview.**")
        elif score >= 50:
            feedback.append("📋 **Moderate match. Consider for further review.**")
        elif score >= 35:
            feedback.append("⚠️ **Low match. Keep in backup list.**")
        else:
            feedback.append("❌ **Poor match. Does not meet requirements.**")
        
        return feedback
    
    def analyze_resume(self, pdf_path, job_description):
        """Complete resume analysis with real NLP"""
        
        # Extract text
        resume_text = self.extract_text_from_pdf(pdf_path)
        
        if not resume_text:
            raise Exception("Could not extract text from PDF")
        
        # Extract skills
        skills_found = self.extract_skills(resume_text)
        
        # Calculate match score using NLP
        final_score = self.calculate_match_score(resume_text, job_description)
        
        # Extract entities for additional info
        entities = self.extract_entities_nlp(resume_text)
        
        # Generate detailed feedback
        feedback = self.generate_detailed_feedback(resume_text, job_description, final_score)
        
        # Classification
        if final_score >= 80:
            classification = "Outstanding Match", "excellent"
            recommendation = "Highly recommended for interview - Excellent alignment with requirements"
        elif final_score >= 65:
            classification = "Good Match", "good"
            recommendation = "Recommended for interview - Good skill alignment"
        elif final_score >= 50:
            classification = "Potential Match", "average"
            recommendation = "Consider for interview - Some skills match"
        elif final_score >= 35:
            classification = "Low Match", "below_average"
            recommendation = "Keep as backup - Limited skill alignment"
        else:
            classification = "Not Suitable", "poor"
            recommendation = "Does not meet requirements - Significant gaps detected"
        
        # Calculate individual scores for display
        clean_resume = self.advanced_nlp_clean(resume_text)
        clean_job = self.advanced_nlp_clean(job_description)
        semantic_score = self.semantic_similarity(clean_resume, clean_job)
        tfidf_score = self.tfidf_similarity(clean_resume, clean_job)
        
        return {
            'skills': skills_found,
            'skills_count': len(skills_found),
            'skills_text': ", ".join(skills_found) if skills_found else "No skills detected",
            'score': final_score,
            'semantic_score': round(semantic_score, 2),
            'tfidf_score': round(tfidf_score, 2),
            'classification': classification[0],
            'status': classification[1],
            'recommendation': recommendation,
            'feedback': feedback,
            'entities': entities,
            'sentiment': self.analyze_sentiment(resume_text),
            'key_phrases': self.extract_key_phrases(resume_text)[:10]
        }
