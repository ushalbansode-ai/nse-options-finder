"""
Analyzes multi-timeframe consistency of OI structure
"""
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List

class MultiTimeframeAnalyzer:
    def __init__(self):
        self.historical_data = {
            'previous_day': None,
            'pre_open': None,
            'intraday': []
        }
    
    def analyze_consistency(self, current_data: Dict, 
                           historical_snapshots: Dict) -> Dict:
        """Analyze OI structure consistency across timeframes"""
        return {
            'structural_levels': self._identify_structural_levels(
                current_data, historical_snapshots
            ),
            'noise_levels': self._identify_noise_levels(
                current_data, historical_snapshots
            ),
            'regime_shift': self._detect_regime_shift(historical_snapshots),
            'institutional_interest': self._assess_institutional_interest(
                current_data, historical_snapshots
            ),
            'timeframe_alignment': self._calculate_alignment_score(
                current_data, historical_snapshots
            )
        }
    
    def _identify_structural_levels(self, current_data: Dict, 
                                   historical: Dict) -> List[Dict]:
        """Identify levels that persist across timeframes"""
        structural_levels = []
        current_strikes = sorted(current_data.keys())
        
        # Get OI from different timeframes
        previous_oi = historical.get('previous_day', {})
        pre_open_oi = historical.get('pre_open', {})
        
        for strike in current_strikes:
            if strike in current_data:
                current_ce_oi = current_data[strike].get('CE', {}).get('open_interest', 0)
                current_pe_oi = current_data[strike].get('PE', {}).get('open_interest', 0)
                current_total = current_ce_oi + current_pe_oi
                
                # Check persistence
                persistence_score = 0
                
                if strike in previous_oi:
                    prev_ce = previous_oi[strike].get('ce_oi', 0)
                    prev_pe = previous_oi[strike].get('pe_oi', 0)
                    prev_total = prev_ce + prev_pe
                    
                    if prev_total > current_total * 0.5:
                        persistence_score += 1
                
                if strike in pre_open_oi:
                    pre_ce = pre_open_oi[strike].get('ce_oi', 0)
                    pre_pe = pre_open_oi[strike].get('pe_oi', 0)
                    pre_total = pre_ce + pre_pe
                    
                    if pre_total > current_total * 0.7:
                        persistence_score += 1
                
                # Check if level is structural
                if persistence_score >= 1 and current_total > 1000000:
                    dominance = 'CE' if current_ce_oi > current_pe_oi * 1.5 else 'PE'
                    
                    structural_levels.append({
                        'strike': strike,
                        'persistence_score': persistence_score,
                        'current_total_oi': current_total,
                        'dominance': dominance,
                        'type': 'SUPPORT' if dominance == 'PE' else 'RESISTANCE',
                        'confidence': min(0.3 + persistence_score * 0.35, 1.0)
                    })
        
        return structural_levels
    
    def _identify_noise_levels(self, current_data: Dict, 
                              historical: Dict) -> List[Dict]:
        """Identify levels that only exist intraday (noise)"""
        noise_levels = []
        
        for strike in current_data.keys():
            current_total = (current_data[strike].get('CE', {}).get('open_interest', 0) +
                           current_data[strike].get('PE', {}).get('open_interest', 0))
            
            # Check if this level existed previously
            existed_previously = False
            
            if strike in historical.get('previous_day', {}):
                existed_previously = True
            
            if strike in historical.get('pre_open', {}):
                existed_previously = True
            
            if not existed_previously and current_total > 500000:
                noise_levels.append({
                    'strike': strike,
                    'current_oi': current_total,
                    'reason': 'Intraday only build',
                    'reliability': 0.3
                })
        
        return noise_levels
    
    def _detect_regime_shift(self, historical: Dict) -> Dict:
        """Detect if there's a regime shift in OI structure"""
        if 'previous_day' not in historical or 'pre_open' not in historical:
            return {'detected': False, 'strength': 0}
        
        prev_data = historical['previous_day']
        pre_open_data = historical['pre_open']
        
        # Calculate OI distribution shift
        prev_strikes = list(prev_data.keys())
        pre_open_strikes = list(pre_open_data.keys())
        
        # Check for migration of high OI strikes
        prev_high_oi_strikes = sorted(
            prev_strikes,
            key=lambda x: prev_data[x].get('ce_oi', 0) + prev_data[x].get('pe_oi', 0),
            reverse=True
        )[:5]
        
        pre_open_high_oi_strikes = sorted(
            pre_open_strikes,
            key=lambda x: pre_open_data[x].get('ce_oi', 0) + pre_open_data[x].get('pe_oi', 0),
            reverse=True
        )[:5]
        
        # Calculate overlap
        overlap = len(set(prev_high_oi_strikes) & set(pre_open_high_oi_strikes))
        shift_strength = 1 - (overlap / 5)
        
        if shift_strength > 0.6:
            direction = self._determine_shift_direction(
                prev_high_oi_strikes, pre_open_high_oi_strikes
            )
            return {
                'detected': True,
                'strength': shift_strength,
                'direction': direction,
                'message': f'OI structure shifted {direction} overnight'
            }
        
        return {'detected': False, 'strength': shift_strength}
    
    def _determine_shift_direction(self, prev_strikes: List, 
                                  current_strikes: List) -> str:
        """Determine direction of OI shift"""
        prev_avg = np.mean(prev_strikes) if prev_strikes else 0
        current_avg = np.mean(current_strikes) if current_strikes else 0
        
        if current_avg > prev_avg * 1.01:
            return 'UP'
        elif current_avg < prev_avg * 0.99:
            return 'DOWN'
        else:
            return 'SIDEWAYS'
    
    def _assess_institutional_interest(self, current_data: Dict, 
                                      historical: Dict) -> float:
        """Assess level of institutional interest"""
        # Institutions tend to build positions that persist
        structural_count = len(self._identify_structural_levels(current_data, historical))
        total_high_oi = len([s for s in current_data.keys() if 
                           (current_data[s].get('CE', {}).get('open_interest', 0) + 
                            current_data[s].get('PE', {}).get('open_interest', 0)) > 1000000])
        
        if total_high_oi > 0:
            institutional_score = structural_count / total_high_oi
        else:
            institutional_score = 0
        
        return institutional_score
    
    def _calculate_alignment_score(self, current_data: Dict, 
                                  historical: Dict) -> Dict:
        """Calculate alignment score across timeframes"""
        structural_levels = self._identify_structural_levels(current_data, historical)
        
        if not structural_levels:
            return {'score': 0, 'quality': 'POOR'}
        
        # Calculate average confidence
        avg_confidence = np.mean([l['confidence'] for l in structural_levels])
        
        # Assess quality
        if avg_confidence > 0.7:
            quality = 'EXCELLENT'
        elif avg_confidence > 0.5:
            quality = 'GOOD'
        elif avg_confidence > 0.3:
            quality = 'FAIR'
        else:
            quality = 'POOR'
        
        return {
            'score': avg_confidence,
            'quality': quality,
            'structural_level_count': len(structural_levels)
      }
