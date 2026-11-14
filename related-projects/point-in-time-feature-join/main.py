"""Point In Time Feature Join. Synthetic portfolio demonstration."""
def run(data):
    for feature in data['features']:
        if feature['available_at'] < feature['event_at']:
            raise ValueError('Availability cannot precede the event')
    joined = []
    for label in data['labels']:
        eligible = [f for f in data['features'] if f['entity']==label['entity']
                    and f['event_at'] <= label['at'] and f['available_at'] <= label['at']]
        feature = max(eligible,key=lambda f:(f['event_at'],f['available_at'])) if eligible else None
        joined.append(dict(label,feature_value=feature['value'] if feature else None))
    return {'training_rows':joined,'missing_features':sum(r['feature_value'] is None for r in joined)}



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
