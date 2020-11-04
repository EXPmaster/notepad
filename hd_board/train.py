from __future__ import print_function
import argparse, os, sys
import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
from time import time
from .utils import train,test
from .utils import Load_lmdb
from .utils import Logger,TFLogger
from .utils import load_checkpoint,save_checkpoint
from .nets import SOAT



def mytrain(args):
    cudnn.enable = True
    args.cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)
    if args.cuda:
        torch.cuda.manual_seed(args.seed)

    train_loader, test_loader = Load_lmdb(args.training_data_dir, args.test_data_dir,
                                          input_size=[96, 96], batch_size=args.batch_size)

    model = SOAT(num_classes=3755)

    if args.cuda:
        model = nn.DataParallel(model).cuda()
    cudnn.benchmark = True
    if args.eval:
        checkpoint = load_checkpoint(os.path.join(args.logs_dir, 'model_best.pth.tar'))
        model.load_state_dict(checkpoint['state_dict'])
        test(model, test_loader)

    # Load from checkpoint
    start_epoch = args.start_epoch
    best_res = 0
    if args.restore:
        checkpoint = load_checkpoint(args.restore)
        model.load_state_dict(checkpoint['state_dict'])
        start_epoch = checkpoint['epoch']
        best_res = checkpoint['best_res']
        print("=> Start epoch {}  best res {:.2%}"
                .format(start_epoch, best_res))

    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[3, 7, 12, 16], gamma=0.1)

    train_tfLogger = TFLogger(os.path.join(args.logs_dir, 'train'))
    test_tfLogger = TFLogger(os.path.join(args.logs_dir, 'test'))
    sys.stdout = Logger(os.path.join(args.logs_dir, 'log.txt'))

    # start training
    for epoch in range(start_epoch, args.epochs):
        scheduler.step()
        since = time()
        train(model, epoch, train_loader, test_loader, optimizer, args.log_interval, tfLogger=train_tfLogger,
              use_cuda=args.cuda)
        iter = time() - since
        print("Spends {}s for last training epoch".format(iter))
        # Test while training
        step = len(train_loader) * (epoch + 1)
        res = test(model, test_loader, step=step, tfLogger=test_tfLogger, use_cuda=args.cuda)

        is_best = res > best_res
        best_res = max(res, best_res)
        save_checkpoint({
            'state_dict': model.state_dict(),
            'epoch': epoch + 1,
            'best_res': best_res,
        }, is_best, fpath=os.path.join(args.logs_dir, 'checkpoint.pth.tar'))

        print('\n * Finished epoch {:3d}  top1: {:5.2%}  best: {:5.2%}{}\n'.
              format(epoch + 1, res, best_res, ' *' if is_best else ''))

    # Final teset
    print('Test with the best model:')
    checkpoint = load_checkpoint(os.path.join(args.logs_dir, 'model_best.pth.tar'))
    model.load_state_dict(checkpoint['state_dict'])
    test(model, test_loader)

    # Close the tf logger
    train_tfLogger.close()
    test_tfLogger.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch Chinese OCR')
    parser.add_argument('--training_data_dir', type=str, default='./new_data/train_lmdb')
    parser.add_argument('--test_data_dir', type=str, default='./new_data/test_lmdb')
    parser.add_argument('--batch_size', type=int, default=256, metavar='N',
                        help='input batch size for training (default: 32)')
    parser.add_argument('--epochs', type=int, default=20, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.1, metavar='LR',
                        help='learning rate (default: 0.1)')
    parser.add_argument('--num_instances', type=int, default=8,
                        help='per_class number in a mini_batch')
    parser.add_argument('--momentum', type=float, default=0.9, metavar='M',
                        help='SGD momentum (default: 0.9)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--logs_dir', type=str, metavar='PATH',
                        default='./')
    parser.add_argument('--restore', type=str, default='', metavar='PATH')
    parser.add_argument('--start_epoch', type=int, default=0, metavar='N')
    parser.add_argument('--eval', action='store_true', default=False)

    args = parser.parse_args()

    mytrain(args)