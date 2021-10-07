from .vox import VoxUnitran, VoxEpitran, VoxWikipron


def get_dataset_cls(dataset_name):
    datasets = {
        'unitran': VoxUnitran,
        'epitran': VoxEpitran,
        'wikipron': VoxWikipron,
    }

    return datasets[dataset_name]


def get_languages(dataset_name):
    dataset_cls = get_dataset_cls(dataset_name)
    return dataset_cls.get_languages()
