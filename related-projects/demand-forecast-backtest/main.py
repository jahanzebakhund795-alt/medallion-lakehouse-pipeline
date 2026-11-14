"""Demand Forecast Backtest. Synthetic portfolio demonstration."""
def run(data):
    values,window,start = data['demand'],data['window'],data['test_start']
    if type(window) is not int or not 1 <= window <= start < len(values):
        raise ValueError('Require 1 <= window <= test_start < observations')
    if any(type(v) not in (int,float) or v < 0 for v in values):
        raise ValueError('Demand must be nonnegative numeric values')
    predictions = []
    for t in range(start,len(values)):
        prediction = sum(values[t-window:t])/window
        predictions.append({'period':t,'actual':values[t],'moving_average':prediction,'naive':values[t-1]})
    mae = lambda name: sum(abs(r['actual']-r[name]) for r in predictions)/len(predictions)
    return {'predictions':predictions,'moving_average_mae':mae('moving_average'),'naive_mae':mae('naive')}



if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('sample.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.input.read_text()))
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    if args.output:
        args.output.write_text(serialized + '\n')
    else:
        print(serialized)
