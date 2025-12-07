"""
Analyzes depth and stiffness beyond immediate support/resistance
"""
import numpy as np
from typing import Dict, List

class SupportDepthAnalyzer:
    def __init__(self, look_ahead_strikes: int = 5):
        self.look_ahead = look_ahead_strikes
    
    def analyze_depth(self, chain_data: Dict, spot_price: float, 
                     support_strikes: List[float], resistance_strikes: List[float]) -> Dict:
        """Analyze what lies beyond immediate S/R"""
        return {
            'below_support': self._analyze_below_support(chain_data, spot_price, support_strikes),
            'above_resistance': self._analyze_above_resistance(chain_data, spot_price, resistance_strikes),
            'stiffness_scores': self._calculate_stiffness_scores(chain_data, spot_price),
            'air_pockets': self._identify_air_pockets(chain_data, spot_price)
        }
    
    def _analyze_below_support(self, chain_data: Dict, spot_price: float, 
                              support_strikes: List[float]) -> Dict:
        """Analyze zone below support"""
        if not support_strikes:
            return {'has_depth': False, 'type': 'UNKNOWN'}
        
        nearest_support = min(support_strikes, key=lambda x: abs(x - spot_price))
        strikes = sorted(chain_data.keys())
        
        # Find support index
        try:
            support_idx = strikes.index(nearest_support)
        except ValueError:
            return {'has_depth': False, 'type': 'UNKNOWN'}
        
        # Look at next 3 strikes below support
        next_strikes = strikes[max(0, support_idx-3):support_idx]
        
        if not next_strikes:
            return {'has_depth': False, 'type': 'AIR_POCKET'}
        
        # Calculate OI density
        total_pe_oi = 0
        total_ce_oi = 0
        
        for strike in next_strikes:
            pe_oi = chain_data[strike].get('PE', {}).get('open_interest', 0)
            ce_oi = chain_data[strike].get('CE', {}).get('open_interest', 0)
            total_pe_oi += pe_oi
            total_ce_oi += ce_oi
        
        # Determine type
        if total_pe_oi > total_ce_oi * 2:
            depth_type = 'DEMAND_ZONE'  # Gradual support
            has_depth = True
        elif total_pe_oi + total_ce_oi < 100000:  # Low OI
            depth_type = 'AIR_POCKET'
            has_depth = False
        else:
            depth_type = 'NEUTRAL'
            has_depth = True
        
        return {
            'has_depth': has_depth,
            'type': depth_type,
            'nearest_support': nearest_support,
            'next_support': next_strikes[0] if next_strikes else None,
            'pe_oi_density': total_pe_oi / max(len(next_strikes), 1),
            'drop_potential': 100 if depth_type == 'AIR_POCKET' else 25  # Points potential
        }
    
    def _analyze_above_resistance(self, chain_data: Dict, spot_price: float,
                                 resistance_strikes: List[float]) -> Dict:
        """Analyze zone above resistance"""
        if not resistance_strikes:
            return {'has_depth': False, 'type': 'UNKNOWN'}
        
        nearest_resistance = min(resistance_strikes, key=lambda x: abs(x - spot_price))
        strikes = sorted(chain_data.keys())
        
        try:
            resistance_idx = strikes.index(nearest_resistance)
        except ValueError:
            return {'has_depth': False, 'type': 'UNKNOWN'}
        
        # Look at next 3 strikes above resistance
        next_strikes = strikes[resistance_idx+1:min(len(strikes), resistance_idx+4)]
        
        if not next_strikes:
            return {'has_depth': False, 'type': 'AIR_POCKET'}
        
        # Calculate OI density
        total_ce_oi = 0
        total_pe_oi = 0
        
        for strike in next_strikes:
            ce_oi = chain_data[strike].get('CE', {}).get('open_interest', 0)
            pe_oi = chain_data[strike].get('PE', {}).get('open_interest', 0)
            total_ce_oi += ce_oi
            total_pe_oi += pe_oi
        
        if total_ce_oi > total_pe_oi * 2:
            depth_type = 'SUPPLY_ZONE'
            has_depth = True
        elif total_ce_oi + total_pe_oi < 100000:
            depth_type = 'AIR_POCKET'
            has_depth = False
        else:
            depth_type = 'NEUTRAL'
            has_depth = True
        
        return {
            'has_depth': has_depth,
            'type': depth_type,
            'nearest_resistance': nearest_resistance,
            'next_resistance': next_strikes[-1] if next_strikes else None,
            'ce_oi_density': total_ce_oi / max(len(next_strikes), 1),
            'rise_potential': 100 if depth_type == 'AIR_POCKET' else 25
        }
    
    def _calculate_stiffness_scores(self, chain_data: Dict, spot_price: float) -> Dict:
        """Calculate stiffness scores for different zones"""
        strikes = sorted(chain_data.keys())
        current_idx = strikes.index(min(strikes, key=lambda x: abs(x - spot_price)))
        
        stiffness = {'above': [], 'below': []}
        
        # Check stiffness for next 5 strikes in each direction
        for offset in range(1, 6):
            # Above
            if current_idx + offset < len(strikes):
                strike = strikes[current_idx + offset]
                ce_oi = chain_data[strike].get('CE', {}).get('open_interest', 0)
                pe_oi = chain_data[strike].get('PE', {}).get('open_interest', 0)
                stiffness['above'].append({
                    'strike': strike,
                    'stiffness': (ce_oi + pe_oi) / 1000,  # Normalized
                    'ce_pe_ratio': ce_oi / max(pe_oi, 1)
                })
            
            # Below
            if current_idx - offset >= 0:
                strike = strikes[current_idx - offset]
                ce_oi = chain_data[strike].get('CE', {}).get('open_interest', 0)
                pe_oi = chain_data[strike].get('PE', {}).get('open_interest', 0)
                stiffness['below'].append({
                    'strike': strike,
                    'stiffness': (ce_oi + pe_oi) / 1000,
                    'ce_pe_ratio': ce_oi / max(pe_oi, 1)
                })
        
        return stiffness
    
    def _identify_air_pockets(self, chain_data: Dict, spot_price: float) -> List[Dict]:
        """Identify zones with very low OI (air pockets)"""
        air_pockets = []
        strikes = sorted(chain_data.keys())
        current_idx = strikes.index(min(strikes, key=lambda x: abs(x - spot_price)))
        
        # Look for consecutive low OI strikes
        window_size = 3
        
        for start_idx in range(max(0, current_idx-10), min(len(strikes)-window_size, current_idx+10)):
            window_strikes = strikes[start_idx:start_idx+window_size]
            
            total_oi = 0
            for strike in window_strikes:
                ce_oi = chain_data[strike].get('CE', {}).get('open_interest', 0)
                pe_oi = chain_data[strike].get('PE', {}).get('open_interest', 0)
                total_oi += ce_oi + pe_oi
            
            avg_oi = total_oi / window_size
            
            if avg_oi < 50000:  # Low OI threshold
                air_pockets.append({
                    'from_strike': window_strikes[0],
                    'to_strike': window_strikes[-1],
                    'avg_oi': avg_oi,
                    'distance_from_spot': abs(spot_price - window_strikes[0]),
                    'pocket_size': window_strikes[-1] - window_strikes[0]
                })
        
        return air_pockets
