import json

DATASET = 'nytmulti'

TRAIN_FILE = 'raw/train.json'
DEV_FILE = 'raw/dev.json'
TEST_FILE = 'raw/test.json'


class SPODetail:
    def __init__(self, spo):
        (self.ehs, self.ehe, self.eht, self.r, self.ets, self.ete, self.ett) = spo


def get_all_entity_types(examples):
    entity_types = set()
    for example in examples:
        spos = example['spo_details']
        for spo in spos:
            spod = SPODetail(spo)
            entity_types.add(spod.eht)
            entity_types.add(spod.ett)
    return entity_types


if __name__ == '__main__':
    with open(TRAIN_FILE) as f:
        train_data = json.load(f)
    with open(DEV_FILE) as f:
        dev_data = json.load(f)
    with open(TEST_FILE) as f:
        test_data = json.load(f)

    etypes = get_all_entity_types(train_data)
    etypes.update(get_all_entity_types(dev_data))
    etypes.update(get_all_entity_types(test_data))

    tag_to_id = {'O': 0}
    tag_id = 1
    for e in etypes:
        # add B I tags
        tag_to_id[f'B-{e}'] = tag_id
        tag_id += 1
        tag_to_id[f'I-{e}'] = tag_id
        tag_id += 1

    with open(f'{DATASET}_tag_to_id.json', 'w') as f:
        json.dump(tag_to_id, f)
