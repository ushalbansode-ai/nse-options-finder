"""
Enhanced signal generator with all 10 advanced concepts
"""
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class EnhancedSignalGenerator:
    def __init__(self):
        self.composite_score = 0
        self.signal_history = []
    
    def generate_enhanced_signal(self, all_analyses: Dict) -> Dict:
        """Generate signal using all advanced analyses"""
        
        # Extract all analysis components
        basic_analysis = all_analyses.get('basic', {})
        oi_quality = all_analyses.get('oi_quality', {})
        iv_skew_enhanced = all_analyses.get('iv_skew_enhanced', {})
        time_decay = all_analyses.get('time_decay', {})
        max_pain = all_analyses.get('max_pain', {})
        support_depth = all_analyses.get('support_depth', {})
        elasticity = all_analyses.get('elasticity', {})
        multi_timeframe = all_analyses.get('multi_timeframe', {})
        oi_migration = all_analyses.get('oi_migration', {})
        zone_pcr = all_analyses.get('zone_pcr', {})
        expiry_alignment = all_analyses.get('expiry_alignment', {})
        
        spot_price = all_analyses.get('spot_price', 0)
        
        # Calculate composite score
        score_components = self._calculate_score_components(
            all_analyses
        )
        
        # Apply filters
        filters_passed = self._apply_advanced_filters(all_analyses)
        
        # Generate signal
        if filters_passed['all_passed'] and score_components['final_score'] > 75:
            signal = self._generate_final_signal(score_components, all_analyses)
        elif filters_passed['all_passed'] and score_components['final_score'] > 60:
            signal = self._generate_cautious_signal(score_components, all_analyses)
        else:
            signal = self._generate_no_trade_signal(all_analyses)
        
        # Add advanced context
        signal['advanced_context'] = self._generate_advanced_context(all_analyses)
        signal['quality_metrics'] = self._calculate_quality_metrics(all_analyses)
        
        return signal
    
    def _calculate_score_components(self, analyses: Dict) -> Dict:
        """Calculate score components from all analyses"""
        scores = {}
        
        # 1. OI Quality Score (Fresh vs Trapped)
        oi_quality = analyses.get('oi_quality', {})
        fresh_build_score = min(len(oi_quality.get('fresh_build', [])) * 10, 30)
        trapped_score = min(len(oi_quality.get('trapped_positions', [])) * -5, -15)
        scores['oi_quality_score'] = max(0, fresh_build_score + trapped_score)
        
        # 2. IV Skew Alignment Score
        iv_skew = analyses.get('iv_skew_enhanced', {})
        one_sided = iv_skew.get('one_sided_skew', {})
        fear_zones = iv_skew.get('fear_zones', {})
        
        # Check if IV skew aligns with OI analysis
        iv_alignment = 0
        for strike, data in one_sided.items():
            if data['skew_type'] in ['CE_FEAR', 'PE_FEAR']:
                iv_alignment += 10
        
        scores['iv_alignment_score'] = min(iv_alignment, 20)
        
        # 3. Time Decay Pressure Score
        time_decay = analyses.get('time_decay', {})
        time_phase = time_decay.get('time_phase', '')
        
        if time_phase == 'GAMMA_GAME_PHASE':
            time_score = 15
        elif time_phase == 'SELLER_COMFORT_WINDOW':
            time_score = 5
        else:
            time_score = 10
        
        scores['time_score'] = time_score
        
        # 4. Max Pain Shift Score
        max_pain = analyses.get('max_pain', {})
        shift_strength = abs(max_pain.get('shift', 0))
        shift_score = min(shift_strength * 100, 15)
        scores['max_pain_score'] = shift_score
        
        # 5. Support Depth Score
        support_depth = analyses.get('support_depth', {})
        below_depth = support_depth.get('below_support', {})
        above_depth = support_depth.get('above_resistance', {})
        
        depth_score = 0
        if below_depth.get('has_depth', False):
            depth_score += 5
        if above_depth.get('has_depth', False):
            depth_score += 5
        
        air_pockets = support_depth.get('air_pockets', [])
        if air_pockets:
            depth_score += 10  # Breakout potential
        
        scores['depth_score'] = depth_score
        
        # 6. Elasticity Score
        elasticity = analyses.get('elasticity', {})
        sticky_zones = elasticity.get('sticky_zones', [])
        elastic_zones = elasticity.get('elastic_zones', [])
        
        elasticity_score = 0
        if sticky_zones:
            elasticity_score += 10  # Good for fading
        if elastic_zones:
            elasticity_score += 5   # Caution needed
        
        scores['elasticity_score'] = elasticity_score
        
        # 7. Multi-timeframe Alignment Score
        multi_timeframe = analyses.get('multi_timeframe', {})
        alignment = multi_timeframe.get('timeframe_alignment', {})
        scores['mtf_score'] = alignment.get('score', 0) * 20
        
        # 8. OI Migration Score
        oi_migration = analyses.get('oi_migration', {})
        migration_trend = oi_migration.get('migration_trend', {})
        
        migration_score = 0
        if migration_trend.get('overall') in ['BULLISH', 'BEARISH']:
            migration_score = oi_migration.get('trend_strength', 0) * 15
        
        scores['migration_score'] = migration_score
        
        # 9. Zone PCR Score
        zone_pcr = analyses.get('zone_pcr', {})
        pcr_divergence = zone_pcr.get('pcr_divergence', {})
        
        pcr_score = 10  # Base score
        if pcr_divergence.get('trading_implication') == 'FADE_GLOBAL_PCR':
            pcr_score += 5  # Extra edge
        
        scores['pcr_score'] = pcr_score
        
        # 10. Expiry Alignment Score
        expiry_alignment = analyses.get('expiry_alignment', {})
        alignment_score = expiry_alignment.get('overall_alignment_score', 0) * 10
        scores['expiry_score'] = alignment_score
        
        # Calculate final score
        total_score = sum(scores.values())
        normalized_score = min(total_score, 100)
        
        scores['final_score'] = normalized_score
        scores['component_breakdown'] = scores.copy()
        
        return scores
    
    def _apply_advanced_filters(self, analyses: Dict) -> Dict:
        """Apply advanced filters to validate signal"""
        filters = {
            'oi_quality_filter': False,
            'iv_skew_filter': False,
            'time_filter': False,
            'depth_filter': False,
            'elasticity_filter': False,
            'mtf_filter': False,
            'all_passed': False
        }
        
        # 1. OI Quality Filter: Avoid trapped positions
        oi_quality = analyses.get('oi_quality', {})
        trapped_count = len(oi_quality.get('trapped_positions', []))
        fresh_count = len(oi_quality.get('fresh_build', []))
        
        if fresh_count > trapped_count * 2:
            filters['oi_quality_filter'] = True
        
        # 2. IV Skew Filter: Check for fear alignment
        iv_skew = analyses.get('iv_skew_enhanced', {})
        fear_zones = iv_skew.get('fear_zones', {})
        
        if fear_zones.get('above') or fear_zones.get('below'):
            filters['iv_skew_filter'] = True
        
        # 3. Time Filter: Avoid seller comfort window for breakouts
        time_decay = analyses.get('time_decay', {})
        time_phase = time_decay.get('time_phase', '')
        
        if time_phase != 'SELLER_COMFORT_WINDOW':
            filters['time_filter'] = True
        
        # 4. Depth Filter: Check for air pockets
        support_depth = analyses.get('support_depth', {})
        air_pockets = support_depth.get('air_pockets', [])
        
        if air_pockets:
            filters['depth_filter'] = True
        
        # 5. Elasticity Filter: Avoid super-elastic zones for fading
        elasticity = analyses.get('elasticity', {})
        gamma_risk = elasticity.get('gamma_risk', 0)
        
        if gamma_risk < 0.7:
            filters['elasticity_filter'] = True
        
        # 6. Multi-timeframe Filter: Require some structural levels
        multi_timeframe = analyses.get('multi_timeframe', {})
        structural_levels = multi_timeframe.get('structural_levels', [])
        
        if len(structural_levels) >= 2:
            filters['mtf_filter'] = True
        
        # Overall filter
        passed_filters = sum(filters.values()) - 1  # Subtract 'all_passed'
        if passed_filters >= 4:  # Pass at least 4 of 6 filters
            filters['all_passed'] = True
        
        return filters
    
    def _generate_final_signal(self, scores: Dict, analyses: Dict) -> Dict:
        """Generate final high-confidence signal"""
        # Determine direction based on strongest components
        bull_components = 0
        bear_components = 0
        
        # Check OI migration
        oi_migration = analyses.get('oi_migration', {})
        migration_trend = oi_migration.get('migration_trend', {})
        
        if migration_trend.get('overall') == 'BULLISH':
            bull_components += 2
        elif migration_trend.get('overall') == 'BEARISH':
            bear_components += 2
        
        # Check max pain shift
        max_pain = analyses.get('max_pain', {})
        if max_pain.get('direction') == 'UP':
            bull_components += 1
        elif max_pain.get('direction') == 'DOWN':
            bear_components += 1
        
        # Check IV skew
        iv_skew = analyses.get('iv_skew_enhanced', {})
        one_sided = iv_skew.get('one_sided_skew', {})
        
        for strike, data in one_sided.items():
            if data['skew_type'] == 'CE_FEAR':
                bull_components += 1
            elif data['skew_type'] == 'PE_FEAR':
                bear_components += 1
        
        # Determine final signal
        if bull_components > bear_components + 1:
            direction = 'BUY_CALL'
            confidence = min(scores['final_score'] + 10, 95)
            tags = ['HIGH_CONFIDENCE', 'MULTI_FACTOR_ALIGNED']
        elif bear_components > bull_components + 1:
            direction = 'BUY_PUT'
            confidence = min(scores['final_score'] + 10, 95)
            tags = ['HIGH_CONFIDENCE', 'MULTI_FACTOR_ALIGNED']
        else:
            direction = 'NO_TRADE'
            confidence = 0
            tags = ['MIXED_SIGNALS']
        
        return {
            'signal': direction,
            'confidence': confidence,
            'tags': tags,
            'score_breakdown': scores['component_breakdown'],
            'filters_passed': self._apply_advanced_filters(analyses)
        }
    
    def _generate_advanced_context(self, analyses: Dict) -> Dict:
        """Generate advanced context for the signal"""
        context = {
            'key_insights': [],
            'risk_factors': [],
            'opportunities': [],
            'time_context': analyses.get('time_decay', {}).get('time_phase', '')
        }
        
        # Add insights based on analyses
        support_depth = analyses.get('support_depth', {})
        if support_depth.get('air_pockets'):
            context['opportunities'].append('AIR_POCKET_BREAKOUT_POTENTIAL')
        
        elasticity = analyses.get('elasticity', {})
        if elasticity.get('sticky_zones'):
            context['insights'].append('STICKY_OPTIONS_GOOD_FOR_FADING')
        
        multi_timeframe = analyses.get('multi_timeframe', {})
        if multi_timeframe.get('regime_shift', {}).get('detected'):
            context['risk_factors'].append('REGIME_SHIFT_DETECTED')
        
        return context
