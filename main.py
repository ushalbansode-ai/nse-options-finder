"""
Enhanced main file with all 10 advanced concepts
"""
import yaml
import json
from datetime import datetime
from typing import Dict

from src.analytics.oi_quality_analyzer import OIQualityAnalyzer
from src.analytics.iv_skew_enhanced import IVSkewEnhanced
from src.analytics.time_decay_analyzer import TimeDecayAnalyzer
from src.analytics.max_pain_analyzer import MaxPainAnalyzer
from src.analytics.support_depth_analyzer import SupportDepthAnalyzer
from src.analytics.option_elasticity_analyzer import OptionElasticityAnalyzer
from src.analytics.multi_timeframe_analyzer import MultiTimeframeAnalyzer
from src.analytics.oi_migration_analyzer import OIMigrationAnalyzer
from src.analytics.zone_pcr_analyzer import ZonePCRAnalyzer
from src.analytics.expiry_alignment_analyzer import ExpiryAlignmentAnalyzer

from src.signals.signal_generator_enhanced import EnhancedSignalGenerator

class EnhancedOptionChainSignalEngine:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize all analyzers
        self.oi_quality = OIQualityAnalyzer()
        self.iv_skew_enhanced = IVSkewEnhanced()
        self.time_decay = TimeDecayAnalyzer()
        self.max_pain = MaxPainAnalyzer()
        self.support_depth = SupportDepthAnalyzer()
        self.elasticity = OptionElasticityAnalyzer()
        self.multi_timeframe = MultiTimeframeAnalyzer()
        self.oi_migration = OIMigrationAnalyzer()
        self.zone_pcr = ZonePCRAnalyzer()
        self.expiry_alignment = ExpiryAlignmentAnalyzer()
        
        self.signal_generator = EnhancedSignalGenerator()
        
        self.historical_data = []
        
    def run_enhanced_cycle(self) -> Dict:
        """Run one enhanced analysis cycle"""
        try:
            # Fetch data (simplified - in practice, fetch from NSE)
            current_data = self._fetch_current_data()
            spot_price = current_data['spot_price']
            chain_data = current_data['chain_data']
            
            # Get key levels from basic analysis
            key_walls = self._get_key_walls(chain_data, spot_price)
            support_strikes = [w['strike'] for w in key_walls if w['dominance'] == 'PE']
            resistance_strikes = [w['strike'] for w in key_walls if w['dominance'] == 'CE']
            
            # Run all advanced analyses
            all_analyses = {
                'spot_price': spot_price,
                'timestamp': datetime.now().isoformat(),
                
                # Basic analysis
                'basic': {
                    'key_walls': key_walls,
                    'support_strikes': support_strikes,
                    'resistance_strikes': resistance_strikes
                },
                
                # Advanced analyses
                'oi_quality': self.oi_quality.analyze_quality(
                    current_data, self.historical_data
                ),
                
                'iv_skew_enhanced': self.iv_skew_enhanced.analyze_skew_pockets(
                    chain_data, spot_price, [w['strike'] for w in key_walls]
                ),
                
                'time_decay': self.time_decay.analyze_time_pressure(
                    chain_data, spot_price, datetime.now()
                ),
                
                'max_pain': self.max_pain.calculate_max_pain(chain_data),
                
                'support_depth': self.support_depth.analyze_depth(
                    chain_data, spot_price, support_strikes, resistance_strikes
                ),
                
                'elasticity': self.elasticity.analyze_elasticity(
                    chain_data, spot_price, 0.1, [w['strike'] for w in key_walls]
                ),
                
                'multi_timeframe': self.multi_timeframe.analyze_consistency(
                    chain_data, self._get_historical_snapshots()
                ),
                
                'oi_migration': self.oi_migration.analyze_migration(
                    chain_data, spot_price
                ),
                
                'zone_pcr': self.zone_pcr.analyze_zone_pcr(
                    chain_data, spot_price, key_walls
                ),
                
                'expiry_alignment': self.expiry_alignment.analyze_alignment(
                    chain_data, self._get_next_expiry_data()
                )
            }
            
            # Generate signal
            signal = self.signal_generator.generate_enhanced_signal(all_analyses)
            
            # Store historical data
            self.historical_data.append(current_data)
            if len(self.historical_data) > 100:
                self.historical_data.pop(0)
            
            return {
                **signal,
                'timestamp': datetime.now().isoformat(),
                'spot_price': spot_price,
                'analyses_summary': self._summarize_analyses(all_analyses)
            }
            
        except Exception as e:
            return {
                'signal': 'NO_TRADE',
                'confidence': 0,
                'tags': ['ERROR', str(e)],
                'timestamp': datetime.now().isoformat()
            }
    
    def _summarize_analyses(self, analyses: Dict) -> Dict:
        """Create a summary of all analyses"""
        summary = {}
        
        # Count key insights
        key_insights = []
        
        # Check each analysis for key insights
        if analyses.get('oi_quality', {}).get('fresh_build'):
            key_insights.append('FRESH_OI_BUILDUP')
        
        if analyses.get('iv_skew_enhanced', {}).get('fear_zones', {}).get('above'):
            key_insights.append('UPSIDE_FEAR_DETECTED')
        
        if analyses.get('support_depth', {}).get('air_pockets'):
            key_insights.append('AIR_POCKET_PRESENT')
        
        if analyses.get('time_decay', {}).get('time_phase') == 'GAMMA_GAME_PHASE':
            key_insights.append('HIGH_GAMMA_RISK')
        
        if analyses.get('multi_timeframe', {}).get('regime_shift', {}).get('detected'):
            key_insights.append('REGIME_SHIFT')
        
        summary['key_insights'] = key_insights
        summary['insight_count'] = len(key_insights)
        
        return summary

# Run the engine
if __name__ == "__main__":
    engine = EnhancedOptionChainSignalEngine()
    
    import time
    while True:
        result = engine.run_enhanced_cycle()
        
        print("\n" + "="*60)
        print(f"Time: {result['timestamp']}")
        print(f"Spot: {result.get('spot_price', 'N/A')}")
        print(f"Signal: {result['signal']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Tags: {', '.join(result['tags'])}")
        
        if 'advanced_context' in result:
            print(f"\nAdvanced Context:")
            for key, value in result['advanced_context'].items():
                if value:  # Only print non-empty values
                    print(f"  {key}: {value}")
        
        if result['signal'] != 'NO_TRADE':
            print("\n" + "🚨 TRADE SIGNAL GENERATED 🚨")
            print(f"Direction: {result['signal']}")
            print(f"Confidence: {result['confidence']}%")
        
        print("="*60 + "\n")
        
        time.sleep(300)  # 5 minutes
