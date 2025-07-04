#!/usr/bin/env python3
"""
Document Analyzer Module

This module provides core text analysis functionality including:
- Sentiment analysis (positive/negative/neutral)
- Keyword extraction (top terms)
- Readability scoring
- Basic statistics (word count, sentences, etc.)
"""

import json
import os
import re
from collections import Counter
from textblob import TextBlob
import math

class DocumentAnalyzer:
    """
    Main document analyzer class that handles all text analysis operations.
    """
    
    def __init__(self, documents_dir="documents"):
        """
        Initialize the document analyzer.
        
        Args:
            documents_dir (str): Directory containing documents and metadata
        """
        self.documents_dir = documents_dir
        self.documents_file = os.path.join(documents_dir, "documents.json")
        self.content_dir = os.path.join(documents_dir, "content")
        
        # Create directories if they don't exist
        os.makedirs(self.documents_dir, exist_ok=True)
        os.makedirs(self.content_dir, exist_ok=True)
        
        # Load existing documents or create empty structure
        self.documents = self._load_documents()
    
    def _load_documents(self):
        """Load documents metadata from JSON file."""
        if os.path.exists(self.documents_file):
            with open(self.documents_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_documents(self):
        """Save documents metadata to JSON file."""
        with open(self.documents_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2, ensure_ascii=False)
    
    def _read_document_content(self, document_id):
        """Read the content of a document by ID."""
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")
        
        filename = self.documents[document_id]["filename"]
        filepath = os.path.join(self.content_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_sentiment(self, text):
        """
        Analyze sentiment of text using TextBlob.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment analysis results
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Convert polarity to categorical sentiment
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 3),
            "subjectivity": round(blob.sentiment.subjectivity, 3)
        }
    
    def extract_keywords(self, text, limit=10):
        """
        Extract top keywords from text using simple word frequency.
        
        Args:
            text (str): Text to analyze
            limit (int): Maximum number of keywords to return
            
        Returns:
            list: Top keywords with their frequencies
        """
        # Clean and tokenize text
        text = text.lower()
        # Remove punctuation and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        
        # Common stop words to filter out
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'is', 'was', 'are',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'a', 'an', 'as', 'if', 'each',
            'how', 'which', 'who', 'when', 'where', 'why', 'what'
        }
        
        # Filter out stop words
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Get top keywords
        top_keywords = word_freq.most_common(limit)
        
        return [{"keyword": word, "frequency": freq} for word, freq in top_keywords]
    
    def calculate_readability(self, text):
        """
        Calculate readability score using a simplified Flesch Reading Ease formula.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Readability metrics
        """
        # Count sentences, words, and syllables
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        # Simple syllable counting (vowel groups)
        syllable_count = 0
        for word in words:
            word = word.lower()
            syllables = len(re.findall(r'[aeiouAEIOU]', word))
            if syllables == 0:
                syllables = 1  # Every word has at least one syllable
            syllable_count += syllables
        
        if sentence_count == 0 or word_count == 0:
            return {
                "flesch_score": 0,
                "reading_level": "unreadable",
                "avg_sentence_length": 0,
                "avg_syllables_per_word": 0
            }
        
        # Calculate Flesch Reading Ease score
        avg_sentence_length = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Determine reading level
        if flesch_score >= 90:
            reading_level = "very easy"
        elif flesch_score >= 80:
            reading_level = "easy"
        elif flesch_score >= 70:
            reading_level = "fairly easy"
        elif flesch_score >= 60:
            reading_level = "standard"
        elif flesch_score >= 50:
            reading_level = "fairly difficult"
        elif flesch_score >= 30:
            reading_level = "difficult"
        else:
            reading_level = "very difficult"
        
        return {
            "flesch_score": round(flesch_score, 2),
            "reading_level": reading_level,
            "avg_sentence_length": round(avg_sentence_length, 2),
            "avg_syllables_per_word": round(avg_syllables_per_word, 2)
        }
    
    def get_basic_stats(self, text):
        """
        Calculate basic text statistics.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Basic statistics
        """
        # Count characters
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        # Count words
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        # Count sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Count paragraphs
        paragraphs = text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        paragraph_count = len(paragraphs)
        
        return {
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "avg_words_per_sentence": round(word_count / sentence_count, 2) if sentence_count > 0 else 0
        }
    
    def analyze_document(self, document_id):
        """
        Perform complete analysis of a document.
        
        Args:
            document_id (str): ID of the document to analyze
            
        Returns:
            dict: Complete analysis results
        """
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")
        
        # Read document content
        content = self._read_document_content(document_id)
        
        # Perform all analyses
        sentiment = self.get_sentiment(content)
        keywords = self.extract_keywords(content)
        readability = self.calculate_readability(content)
        stats = self.get_basic_stats(content)
        
        # Get document metadata
        metadata = self.documents[document_id]
        
        return {
            "document_id": document_id,
            "metadata": metadata,
            "sentiment": sentiment,
            "keywords": keywords,
            "readability": readability,
            "statistics": stats,
            "analysis_timestamp": "N/A"
        }
    
    def add_document(self, document_data):
        """
        Add a new document to the collection.
        
        Args:
            document_data (dict): Document data including content and metadata
            
        Returns:
            str: Document ID of the added document
        """
        # Generate document ID
        document_id = f"doc_{len(self.documents) + 1:03d}"
        
        # Extract content and metadata
        content = document_data.get("content", "")
        title = document_data.get("title", f"Document {document_id}")
        author = document_data.get("author", "Unknown")
        category = document_data.get("category", "General")
        
        # Create filename
        filename = f"{document_id}.txt"
        
        # Save content to file
        filepath = os.path.join(self.content_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add metadata
        self.documents[document_id] = {
            "title": title,
            "author": author,
            "category": category,
            "filename": filename,
            "created_date": "N/A",
            "word_count": len(content.split())
        }
        
        # Save metadata
        self._save_documents()
        
        return document_id
    
    def search_documents(self, query):
        """
        Search documents by content or metadata.
        
        Args:
            query (str): Search query
            
        Returns:
            list: List of matching document IDs with relevance scores
        """
        query = query.lower()
        results = []
        
        for doc_id, metadata in self.documents.items():
            score = 0
            
            # Search in title
            if query in metadata.get("title", "").lower():
                score += 3
            
            # Search in author
            if query in metadata.get("author", "").lower():
                score += 2
            
            # Search in category
            if query in metadata.get("category", "").lower():
                score += 2
            
            # Search in content
            try:
                content = self._read_document_content(doc_id).lower()
                if query in content:
                    score += 1
                    # Bonus for multiple occurrences
                    score += content.count(query) * 0.1
            except:
                pass
            
            if score > 0:
                results.append({
                    "document_id": doc_id,
                    "relevance_score": round(score, 2),
                    "title": metadata.get("title", ""),
                    "author": metadata.get("author", ""),
                    "category": metadata.get("category", "")
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return results
    
    def get_all_documents(self):
        """Get list of all documents with metadata."""
        return [
            {
                "document_id": doc_id,
                **metadata
            }
            for doc_id, metadata in self.documents.items()
        ] 