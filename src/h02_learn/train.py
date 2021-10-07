import sys
import os
import math
import torch
import torch.optim as optim

sys.path.append('./src/')
from h02_learn.dataset import get_data_loaders
from h02_learn.model import get_model_cls
from h02_learn.train_info import TrainInfo
from util import argparser
from util import util
from util import constants


def get_args():
    # Data
    argparser.add_argument('--batch-size', type=int, default=64)
    # Model
    argparser.add_argument('--nlayers', type=int, default=2)
    argparser.add_argument('--embedding-size', type=int, default=64)
    argparser.add_argument('--hidden-size', type=int, default=128)
    argparser.add_argument('--dropout', type=float, default=.5)
    # Optimization
    argparser.add_argument('--eval-batches', type=int, default=100)
    argparser.add_argument('--wait-epochs', type=int, default=5)
    # Save
    argparser.add_argument('--checkpoints-path', type=str)

    args = argparser.parse_args()
    args.wait_iterations = args.wait_epochs * args.eval_batches

    args.model_path = os.path.join(args.checkpoints_path, args.model)
    return args


def get_model(alphabet, args):
    # pylint: disable=too-many-function-args,unexpected-keyword-arg

    model_cls = get_model_cls(args.model)
    model = model_cls(
        alphabet, args.embedding_size, args.hidden_size,
        nlayers=args.nlayers, dropout=args.dropout)

    return model.to(device=constants.device)


def train_batch(x, y, model, optimizer):
    optimizer.zero_grad()
    y_hat = model(x)
    loss = model.get_loss(y_hat, y)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
    optimizer.step()

    return loss.item()


def _evaluate(evalloader, model):
    dev_loss, n_instances = 0, 0
    for x, y in evalloader:
        y_hat = model(x)
        loss = model.get_loss(y_hat, y)

        batch_size = y.shape[0]
        dev_loss += (loss * batch_size)
        n_instances += batch_size

    return (dev_loss / n_instances).item()


def evaluate(evalloader, model):
    model.eval()
    with torch.no_grad():
        result = _evaluate(evalloader, model)
    model.train()
    return result

def get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps,
                                    num_cycles=0.5, last_epoch=-1):
    # This function was copied from HuggingFace's transformer in
    # https://github.com/huggingface/transformers/blob/master/src/transformers/optimization.py
    def lr_lambda(current_step):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        progress = (float(current_step - num_warmup_steps) /
                    float(max(1, num_training_steps - num_warmup_steps)))
        return max(0.0, 0.5 * (1.0 + math.cos(math.pi * float(num_cycles) * 2.0 * progress)))

    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda, last_epoch)


def get_optim_lr(optimizer):
    return (list(optimizer.param_groups))[0]['lr']


def train(trainloader, devloader, model, eval_batches, wait_iterations):
    params = util.add_weight_decay(model, weight_decay=1e-2)
    optimizer = optim.AdamW(params, weight_decay=0)
    scheduler = get_cosine_schedule_with_warmup(
        optimizer, num_warmup_steps=1000, num_training_steps=40000)
    train_info = TrainInfo(wait_iterations, eval_batches)

    while not train_info.finish:
        for x, y in trainloader:
            loss = train_batch(x, y, model, optimizer)
            train_info.new_batch(loss)
            scheduler.step()

            if train_info.eval:
                dev_loss = evaluate(devloader, model)

                if train_info.is_best(dev_loss):
                    model.set_best()
                elif train_info.finish:
                    break

                train_info.print_progress(dev_loss, get_optim_lr(optimizer))

    model.recover_best()


def eval_all(trainloader, devloader, testloader, model):
    train_loss = evaluate(trainloader, model)
    dev_loss = evaluate(devloader, model)
    test_loss = evaluate(testloader, model)

    print('Final Training loss: %.4f Dev loss: %.4f Test loss: %.4f' %
          (train_loss, dev_loss, test_loss))
    return (train_loss, dev_loss, test_loss)


def save_results(model, train_loss, dev_loss, test_loss, results_fname):
    args = model.get_args()
    del args['alphabet']
    results = [['name', 'train_loss', 'dev_loss', 'test_loss', 'alphabet_size'] +
               list(args.keys())]
    results += [[model.name, train_loss, dev_loss, test_loss, model.alphabet_size] +
                list(args.values())]
    util.write_csv(results_fname, results)


def save_checkpoints(model, train_loss, dev_loss, test_loss, model_path):
    model.save(model_path)
    results_fname = model_path + '/results.csv'
    save_results(model, train_loss, dev_loss, test_loss, results_fname)


def main():
    args = get_args()
    folds = [list(range(8)), [8], [9]]
    print(args)

    trainloader, devloader, testloader, alphabet = \
        get_data_loaders(args.data_file, folds, args.batch_size)
    print('Train size: %d Dev size: %d Test size: %d Alphabet size: %d' %
          (len(trainloader.dataset), len(devloader.dataset),
           len(testloader.dataset), len(alphabet)))

    model = get_model(alphabet, args)
    train(trainloader, devloader, model, args.eval_batches, args.wait_iterations)

    train_loss, dev_loss, test_loss = \
        eval_all(trainloader, devloader, testloader, model)

    save_checkpoints(model, train_loss, dev_loss, test_loss, args.model_path)


if __name__ == '__main__':
    main()
