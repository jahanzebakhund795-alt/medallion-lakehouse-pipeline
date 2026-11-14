"""Medallion Lakehouse Pipeline. Synthetic portfolio demonstration."""
def run(data):
    silver, quarantine = {}, []
    for row in data['records']:
        try:
            clean = {'id':str(row['id']).strip(), 'region':row['region'].strip().upper(),
                     'cents':int(row['cents']), 'version':int(row['version'])}
            if not clean['id'] or not clean['region'] or clean['cents'] < 0 or clean['version'] < 1:
                raise ValueError('Invalid field value')
        except (KeyError,ValueError,TypeError,AttributeError) as error:
            quarantine.append({'record':row,'reason':str(error)})
            continue
        if clean['id'] not in silver or clean['version'] > silver[clean['id']]['version']:
            silver[clean['id']] = clean
    gold = {}
    for row in silver.values():
        gold[row['region']] = gold.get(row['region'],0) + row['cents']
    return {'bronze':data['records'],'silver':list(silver.values()),'gold':gold,'quarantine':quarantine}



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
