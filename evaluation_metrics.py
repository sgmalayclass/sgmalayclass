#!/usr/bin/env python3
"""
Malay Chatbot Evaluation Metrics
Analyzes chatbot performance using feedback data and conversation logs.
"""

import pandas as pd
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns

class MalayChatbotEvaluator:
    """Evaluation system for Malay chatbot performance"""
    
    def __init__(self, feedback_file: str = "feedback_log.csv"):
        self.feedback_file = feedback_file
        self.metrics = {}
        
    def load_feedback_data(self) -> pd.DataFrame:
        """Load feedback data from CSV"""
        if not os.path.exists(self.feedback_file):
            print(f"❌ Feedback file not found: {self.feedback_file}")
            return pd.DataFrame()
        
        try:
            df = pd.read_csv(self.feedback_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            print(f"❌ Error loading feedback data: {e}")
            return pd.DataFrame()
    
    def calculate_context_retention_score(self, df: pd.DataFrame) -> float:
        """Calculate Context Retention Score (CRS)"""
        if df.empty:
            return 0.0
        
        # Group by session and calculate topic consistency
        session_scores = []
        for session_id in df['session_id'].unique():
            session_data = df[df['session_id'] == session_id]
            if len(session_data) < 2:
                continue
            
            # Calculate how often the conversation stays on topic
            # Higher score for fewer abrupt topic changes
            topic_changes = 0
            for i in range(1, len(session_data)):
                # Simple heuristic: if response source changes dramatically, topic might have changed
                prev_source = session_data.iloc[i-1]['response_source']
                curr_source = session_data.iloc[i]['response_source']
                if prev_source != curr_source and 'cultural' not in prev_source and 'cultural' not in curr_source:
                    topic_changes += 1
            
            session_score = max(0, 100 - (topic_changes / len(session_data) * 100))
            session_scores.append(session_score)
        
        return sum(session_scores) / len(session_scores) if session_scores else 0.0
    
    def calculate_malay_appropriateness_index(self, df: pd.DataFrame) -> float:
        """Calculate Malay Appropriateness Index (MAI)"""
        if df.empty:
            return 0.0
        
        # Score based on:
        # 1. Dialect adaptation usage
        # 2. Cultural context responses
        # 3. User satisfaction with Malay responses
        
        total_score = 0
        total_responses = len(df)
        
        # Dialect adaptation bonus
        dialect_responses = len(df[df['dialect'] != 'standard'])
        dialect_score = (dialect_responses / total_responses) * 20 if total_responses > 0 else 0
        
        # Cultural context bonus
        cultural_responses = len(df[(df['cultural_context'].notna()) & (df['cultural_context'] != '')])
        cultural_score = (cultural_responses / total_responses) * 30 if total_responses > 0 else 0
        
        # User satisfaction with ratings >= 4
        high_rated = len(df[df['rating'] >= 4])
        satisfaction_score = (high_rated / total_responses) * 50 if total_responses > 0 else 0
        
        return dialect_score + cultural_score + satisfaction_score
    
    def calculate_response_time_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate response time statistics"""
        # For this implementation, we'll simulate response times
        # In a real system, you'd measure actual response times
        response_times = []
        for _, row in df.iterrows():
            # Simulate response time based on response source
            if 'AI generation' in row['response_source']:
                response_times.append(2.5)  # AI responses typically slower
            elif 'retrieval' in row['response_source']:
                response_times.append(0.5)  # Retrieval faster
            else:
                response_times.append(0.3)  # Legacy system fastest
        
        if not response_times:
            return {"avg": 0, "min": 0, "max": 0, "std": 0}
        
        return {
            "avg": sum(response_times) / len(response_times),
            "min": min(response_times),
            "max": max(response_times),
            "std": pd.Series(response_times).std()
        }
    
    def evaluate_performance(self) -> Dict:
        """Run comprehensive evaluation"""
        df = self.load_feedback_data()
        
        if df.empty:
            print("⚠️  No feedback data available for evaluation")
            return {}
        
        print(f"📊 Evaluating performance from {len(df)} interactions...")
        
        # Calculate all metrics
        crs = self.calculate_context_retention_score(df)
        mai = self.calculate_malay_appropriateness_index(df)
        rt_metrics = self.calculate_response_time_metrics(df)
        
        # Basic statistics
        avg_rating = df['rating'].mean()
        total_interactions = len(df)
        unique_sessions = df['session_id'].nunique()
        
        # Response source distribution
        source_dist = df['response_source'].value_counts(normalize=True) * 100
        
        # Dialect usage
        dialect_dist = df['dialect'].value_counts()
        
        # Cultural context triggers
        cultural_triggers = len(df[(df['cultural_context'].notna()) & (df['cultural_context'] != '')])
        
        self.metrics = {
            "evaluation_date": datetime.now().isoformat(),
            "total_interactions": total_interactions,
            "unique_sessions": unique_sessions,
            "avg_rating": avg_rating,
            "context_retention_score": crs,
            "malay_appropriateness_index": mai,
            "response_time": rt_metrics,
            "response_source_distribution": source_dist.to_dict(),
            "dialect_distribution": dialect_dist.to_dict(),
            "cultural_context_triggers": cultural_triggers
        }
        
        return self.metrics
    
    def generate_report(self) -> str:
        """Generate human-readable evaluation report"""
        if not self.metrics:
            self.evaluate_performance()
        
        if not self.metrics:
            return "No evaluation data available."
        
        report = f"""
🤖 MALAY CHATBOT EVALUATION REPORT
{'='*50}

📊 Overview:
   • Total Interactions: {self.metrics['total_interactions']}
   • Unique Sessions: {self.metrics['unique_sessions']}
   • Average Rating: {self.metrics['avg_rating']:.2f}/5.0
   • Evaluation Date: {self.metrics['evaluation_date'][:10]}

🧠 Performance Metrics:
   • Context Retention Score (CRS): {self.metrics['context_retention_score']:.1f}%
   • Malay Appropriateness Index (MAI): {self.metrics['malay_appropriateness_index']:.1f}%
   • Avg Response Time: {self.metrics['response_time']['avg']:.2f}s

🤖 Response Sources:"""
        
        for source, percentage in self.metrics['response_source_distribution'].items():
            report += f"\n   • {source}: {percentage:.1f}%"
        
        report += f"\n\n🗣️  Dialect Usage:"
        for dialect, count in self.metrics['dialect_distribution'].items():
            report += f"\n   • {dialect}: {count} times"
        
        report += f"\n\n🎭 Cultural Context: {self.metrics['cultural_context_triggers']} triggers"
        
        # Performance assessment
        report += f"\n\n📈 Assessment:"
        if self.metrics['avg_rating'] >= 4.0:
            report += f"\n   ✅ User satisfaction: EXCELLENT"
        elif self.metrics['avg_rating'] >= 3.5:
            report += f"\n   👍 User satisfaction: GOOD"
        else:
            report += f"\n   ⚠️  User satisfaction: NEEDS IMPROVEMENT"
        
        if self.metrics['context_retention_score'] >= 80:
            report += f"\n   ✅ Context retention: EXCELLENT"
        elif self.metrics['context_retention_score'] >= 60:
            report += f"\n   👍 Context retention: GOOD"
        else:
            report += f"\n   ⚠️  Context retention: NEEDS IMPROVEMENT"
        
        if self.metrics['malay_appropriateness_index'] >= 70:
            report += f"\n   ✅ Malay appropriateness: EXCELLENT"
        elif self.metrics['malay_appropriateness_index'] >= 50:
            report += f"\n   👍 Malay appropriateness: GOOD"
        else:
            report += f"\n   ⚠️  Malay appropriateness: NEEDS IMPROVEMENT"
        
        return report
    
    def save_metrics(self, filename: str = "evaluation_results.json"):
        """Save evaluation metrics to JSON file"""
        if not self.metrics:
            self.evaluate_performance()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2, ensure_ascii=False)
            print(f"✅ Metrics saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving metrics: {e}")

def main():
    """Run evaluation and generate report"""
    evaluator = MalayChatbotEvaluator()
    
    print("🔍 Starting Malay Chatbot Evaluation...")
    report = evaluator.generate_report()
    print(report)
    
    # Save metrics
    evaluator.save_metrics()
    
    print(f"\n💾 Detailed metrics saved to evaluation_results.json")

if __name__ == "__main__":
    main() 