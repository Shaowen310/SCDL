import json

DATASET = 'nytmulti'

TRAIN_FILE = 'raw/train.json'
DEV_FILE = 'raw/dev.json'
TEST_FILE = 'raw/test.json'


class SPODetail:
    def __init__(self, spo):
        (self.ehs, self.ehe, self.eht, self.r, self.ets, self.ete, self.ett) = spo


def get_tags_for_entity(es, ee, et, tag_to_id):
    tags_span = [tag_to_id[f'B-{et}']]
    tags_span.extend([tag_to_id[f'I-{et}']] * (ee - es - 1))
    return tags_span


def convert_example(example, tag_to_id):
    converted = {}
    converted['str_words'] = example['tokens']
    tags = [tag_to_id['O']] * len(converted['str_words'])
    spos = example['spo_details']
    for spo in spos:
        spod = SPODetail(spo)
        tags_span = get_tags_for_entity(spod.ehs, spod.ehe, spod.eht, tag_to_id)
        tags[spod.ehs:spod.ehe] = tags_span
        tags_span = get_tags_for_entity(spod.ets, spod.ete, spod.ett, tag_to_id)
        tags[spod.ets:spod.ete] = tags_span
    converted['str_words'] = example['tokens']
    converted['tags'] = tags
    return converted


def convert_examples(examples, tag_to_id):
    converted = []
    for e in examples:
        converted.append(convert_example(e, tag_to_id))
    return converted


if __name__ == '__main__':
    with open(TRAIN_FILE) as f:
        train_data = json.load(f)
    with open(DEV_FILE) as f:
        dev_data = json.load(f)
    with open(TEST_FILE) as f:
        test_data = json.load(f)

    with open(f'{DATASET}_tag_to_id.json') as f:
        tag_to_id = json.load(f)

    with open(f'{DATASET}_train.json', 'w') as f:
        train_converted = convert_examples(train_data, tag_to_id)
        json.dump(train_converted, f)
    with open(f'{DATASET}_dev.json', 'w') as f:
        dev_converted = convert_examples(dev_data, tag_to_id)
        json.dump(dev_converted, f)
    with open(f'{DATASET}_test.json', 'w') as f:
        test_converted = convert_examples(test_data, tag_to_id)
        json.dump(test_converted, f)
