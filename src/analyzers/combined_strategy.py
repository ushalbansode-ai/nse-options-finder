"""Combined Strategy Analyzer"""
import pandas as pd

class CombinedStrategyAnalyzer:
    def __init__(self, options_data, futures_data):
        self.options = options_data[options_data['INSTRUMENT'].isin(['OPTSTK', 'OPTIDX'])]
        self.futures = futures_data[futures_data['INSTRUMENT'].isin(['FUTSTK', 'FUTIDX'])]
    
    def find_divergence(self):
        opportunities = []
        
        for symbol in self.futures['SYMBOL'].unique():
            fut_data = self.futures[self.futures['SYMBOL'] == symbol]
            opt_data = self.options[self.options['SYMBOL'] == symbol]
            
            if fut_data.empty or opt_data.empty:
                continue
            
            fut_oi_change = fut_data['CHG_IN_OI'].sum()
            fut_price_change = fut_data['CHG'].sum()
            
            puts = opt_data[opt_data['OPTION_TYP'] == 'PE']
            calls = opt_data[opt_data['OPTION_TYP'] == 'CE']
            
            put_oi = puts['OPEN_INT'].sum()
            call_oi = calls['OPEN_INT'].sum()
            pcr = put_oi / call_oi if call_oi > 0 else 0
            
            if fut_oi_change > 0 and fut_price_change > 0 and pcr > 1.2:
                opportunities.append({
                    'symbol': symbol,
                    'signal': 'BULLISH',
                    'strategy': 'Long Futures or Buy Calls',
                    'pcr': pcr
                })
        
        return pd.DataFrame(opportunities)
