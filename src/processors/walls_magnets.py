

def identify_walls_magnets(df, spot, top_n=5):
result = {"put_walls": [], "call_walls": [], "magnets": []}
if df is None or df.empty:
return result


put_walls = df.sort_values("PE_OI", ascending=False).head(top_n)
call_walls = df.sort_values("CE_OI", ascending=False).head(top_n)
magnets = df.sort_values("total_OI", ascending=False).head(top_n)


result['put_walls'] = [int(x) for x in put_walls['strike'].tolist()]
result['call_walls'] = [int(x) for x in call_walls['strike'].tolist()]
result['magnets'] = [int(x) for x in magnets['strike'].tolist()]


# nearest walls
below_puts = [s for s in result['put_walls'] if s < spot]
above_calls = [s for s in result['call_walls'] if s > spot]
result['nearest_put_wall'] = int(below_puts[0]) if below_puts else None
result['nearest_call_wall'] = int(above_calls[0]) if above_calls else None


return result
