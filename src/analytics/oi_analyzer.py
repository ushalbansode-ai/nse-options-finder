"""
Analyzes OI quality: fresh vs stale vs trapped positions
"""
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class OIQuality:
    strike: float
    option_type: str  # 'CE' or 'PE'
    oi_change: int
    price_change: float  # Option price %
    iv_change: float
    quality: str  # 'FRESH', 'STALE', 'TRAPPED', 'COVERING'
    confidence: float

class OIQualityAnalyzer:
    def __init__(self, lookback_minutes: int = 15):
        self.lookback = lookback_minutes
        self.history = []
        
    def analyze_quality(self, current_data: Dict, historical_data: List[Dict]) -> Dict:
        """Analyze OI quality across strikes"""
        quality_signals = {
            'fresh_build': [],  # Clean directional buildup
            'trapped_positions': [],  # Build against price move
            'covering': [],  # Unwinding with price move
            'stale_positions': []  # No recent activity
        }
        
        if not historical_data:
            return quality_signals
            
        # Get data from lookback period
        recent_data = self._get_recent_data(historical_data)
        
        for strike in current_data.keys():
            for option_type in ['CE', 'PE']:
                quality = self._assess_oi_quality(
                    strike, option_type, current_data, recent_data
                )
                
                if quality.quality == 'FRESH':
                    quality_signals['fresh_build'].append(quality)
                elif quality.quality == 'TRAPPED':
                    quality_signals['trapped_positions'].append(quality)
                elif quality.quality == 'COVERING':
                    quality_signals['covering'].append(quality)
                elif quality.quality == 'STALE':
                    quality_signals['stale_positions'].append(quality)
        
        return quality_signals
    
    def _assess_oi_quality(self, strike: float, option_type: str, 
                          current: Dict, historical: List[Dict]) -> OIQuality:
        """Assess if OI is fresh, stale, or trapped"""
        # Get current values
        current_opt = current[strike].get(option_type, {})
        current_oi = current_opt.get('open_interest', 0)
        current_price = current_opt.get('LTP', 0)
        current_iv = current_opt.get('IV', 0)
        spot_price = current['spot_price']
        
        # Calculate changes from historical
        oi_change = 0
        price_change_pct = 0
        iv_change = 0
        
        for hist in historical:
            if strike in hist and option_type in hist[strike]:
                hist_opt = hist[strike][option_type]
                hist_oi = hist_opt.get('open_interest', 0)
                hist_price = hist_opt.get('LTP', 0)
                hist_iv = hist_opt.get('IV', 0)
                hist_spot = hist['spot_price']
                
                # Calculate changes
                oi_change = current_oi - hist_oi
                price_change_pct = ((current_price - hist_price) / max(hist_price, 0.01)) * 100
                iv_change = current_iv - hist_iv
                spot_change_pct = ((spot_price - hist_spot) / hist_spot) * 100
                break
        
        # Determine quality
        if option_type == 'CE':
            # CE specific logic
            if oi_change > 1000 and price_change_pct > 1 and spot_change_pct > 0.1:
                # Fresh call buying with price up
                quality = 'FRESH'
                confidence = 0.8
            elif oi_change > 1000 and price_change_pct < 0 and spot_change_pct > 0.1:
                # Call writing against uptrend (possible trap)
                quality = 'TRAPPED'
                confidence = 0.6
            elif oi_change < -1000 and price_change_pct < -2 and spot_change_pct < -0.1:
                # Call covering in downtrend
                quality = 'COVERING'
                confidence = 0.7
            else:
                quality = 'STALE'
                confidence = 0.3
        else:  # PE
            if oi_change > 1000 and price_change_pct > 1 and spot_change_pct < -0.1:
                # Fresh put buying with price down
                quality = 'FRESH'
                confidence = 0.8
            elif oi_change > 1000 and price_change_pct < 0 and spot_change_pct < -0.1:
                # Put writing against downtrend
                quality = 'TRAPPED'
                confidence = 0.6
            elif oi_change < -1000 and price_change_pct < -2 and spot_change_pct > 0.1:
                # Put covering in uptrend
                quality = 'COVERING'
                confidence = 0.7
            else:
                quality = 'STALE'
                confidence = 0.3
        
        return OIQuality(
            strike=strike,
            option_type=option_type,
            oi_change=oi_change,
            price_change=price_change_pct,
            iv_change=iv_change,
            quality=quality,
            confidence=confidence
        )
    
    def _get_recent_data(self, historical_data: List[Dict]) -> List[Dict]:
        """Get data from lookback period"""
        current_time = datetime.now()
        recent = []
        
        for data_point in historical_data[-100:]:  # Last 100 data points
            if 'timestamp' in data_point:
                data_time = datetime.fromisoformat(data_point['timestamp'])
                if (current_time - data_time).seconds <= self.lookback * 60:
                    recent.append(data_point)
        
        return recent[-10:] if len(recent) > 10 else recent  # Last 10 data points
