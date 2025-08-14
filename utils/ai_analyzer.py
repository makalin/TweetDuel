"""
AI analysis utilities for TweetDuel
"""

import json
import ollama
from typing import Dict, List, Optional, Any
from datetime import datetime

class AIAnalyzer:
    """AI analysis utility class"""
    
    def __init__(self, model: str = 'llama3.2', temperature: float = 0.8, max_tokens: int = 500):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = ollama.Client()
    
    def analyze_arguments(self, content: str) -> Dict[str, Any]:
        """Analyze arguments in text content"""
        prompt = f"""
        Analyze the following text and identify:
        1. Main arguments/claims
        2. Logical fallacies
        3. Weak points
        4. Emotional appeals
        5. Evidence used
        
        Text: {content}
        
        Provide a structured analysis in JSON format with these keys:
        - main_arguments: list of main claims
        - logical_fallacies: list of logical errors
        - weak_points: list of vulnerable arguments
        - emotional_appeals: list of emotional manipulation
        - evidence: list of evidence provided
        - overall_strength: rating 1-10
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response['response'])
            except json.JSONDecodeError:
                # If not valid JSON, return structured text
                return {
                    'analysis': response['response'],
                    'timestamp': datetime.now().isoformat(),
                    'parse_error': True
                }
                
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def generate_counter_response(self, original_content: str, analysis: Dict, persona: str = 'socrates') -> Dict[str, Any]:
        """Generate counter-response using specified persona"""
        personas = {
            'socrates': {
                'style': "You are Socrates. Use Socratic questioning to challenge assumptions. Ask probing questions that expose logical gaps.",
                'approach': "question-based, philosophical, challenging assumptions"
            },
            'machiavelli': {
                'style': "You are Machiavelli. Be strategic and provocative. Use psychological manipulation and strategic thinking.",
                'approach': "strategic, provocative, psychologically manipulative"
            },
            'chomsky': {
                'style': "You are Noam Chomsky. Be academic and evidence-based. Focus on systemic analysis and factual accuracy.",
                'approach': "academic, evidence-based, systemic analysis"
            },
            'tate': {
                'style': "You are Andrew Tate. Be aggressive and dominant. Use strong language and challenge authority.",
                'approach': "aggressive, dominant, challenging authority"
            },
            'neutral': {
                'style': "You are a neutral analyst. Be balanced and factual. Present counter-arguments respectfully.",
                'approach': "balanced, factual, respectful"
            }
        }
        
        persona_info = personas.get(persona, personas['neutral'])
        
        prompt = f"""
        {persona_info['style']}
        
        Original content: {original_content}
        
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate a powerful counter-response that:
        1. Addresses the main arguments
        2. Exploits logical weaknesses
        3. Adds viral engagement hooks
        4. Maintains the {persona} style ({persona_info['approach']})
        
        Structure your response with:
        - A compelling opening hook
        - Main counter-argument
        - Supporting points
        - Engagement question
        - Strong closing statement
        
        Make it engaging and shareable.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            return {
                'persona': persona,
                'response': response['response'],
                'timestamp': datetime.now().isoformat(),
                'model': self.model,
                'style': persona_info['approach']
            }
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def generate_multiple_counters(self, original_content: str, analysis: Dict, personas: List[str] = None) -> List[Dict[str, Any]]:
        """Generate counter-responses using multiple personas"""
        if not personas:
            personas = ['socrates', 'machiavelli', 'neutral']
        
        counters = []
        for persona in personas:
            counter = self.generate_counter_response(original_content, analysis, persona)
            counters.append(counter)
        
        return counters
    
    def analyze_conversation_tree(self, tweet: Dict, replies: List[Dict]) -> Dict[str, Any]:
        """Analyze the overall conversation structure"""
        prompt = f"""
        Analyze this Twitter conversation and identify:
        1. Main discussion themes
        2. Argument patterns
        3. Engagement hotspots
        4. Potential viral elements
        5. Strategic response opportunities
        
        Original tweet: {tweet['content']}
        
        Replies: {json.dumps([r['content'] for r in replies], indent=2)}
        
        Provide analysis in JSON format.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            try:
                return json.loads(response['response'])
            except json.JSONDecodeError:
                return {
                    'analysis': response['response'],
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def optimize_for_viral(self, content: str, target_audience: str = 'general') -> Dict[str, Any]:
        """Optimize content for viral engagement"""
        prompt = f"""
        Optimize this content for viral engagement on Twitter:
        
        Original: {content}
        
        Target audience: {target_audience}
        
        Make it:
        1. More engaging and shareable
        2. Add viral hooks
        3. Include relevant hashtags
        4. Optimize for engagement
        5. Keep it authentic to the original message
        
        Provide the optimized version and explain the changes.
        """
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            
            return {
                'original': content,
                'optimized': response['response'],
                'timestamp': datetime.now().isoformat(),
                'model': self.model
            }
            
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
