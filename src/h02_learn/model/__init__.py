from .lstm import LstmLM


def get_model_cls(model_type):
    if model_type in 'lstm':
        model_cls = LstmLM
    else:
        raise ValueError('Not implemented: %s' % model_type)

    return model_cls
