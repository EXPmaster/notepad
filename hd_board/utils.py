from __future__ import print_function
from time import time
import torch.nn.functional as F
from torch.autograd import Variable
from tqdm import tqdm
from torchvision import  transforms
import lmdb, six
from torch.utils import data
from PIL import Image
import os
import sys
import numpy as np
import tensorflow as tf
import scipy.misc
import os.path as osp
import shutil
import torch
import errno

try:
    from StringIO import StringIO  # Python 2.7
except ImportError:
    from io import BytesIO  # Python 3.x

def mkdir_if_missing(dir_path):
  try:
    os.makedirs(dir_path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

class Logger(object):
    def __init__(self, fpath=None):
        self.console = sys.stdout
        self.file = None
        if fpath is not None:
            mkdir_if_missing(os.path.dirname(fpath))
            self.file = open(fpath, 'w')

    def __del__(self):
        self.close()

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.close()

    def write(self, msg):
        self.console.write(msg)
        if self.file is not None:
            self.file.write(msg)

    def flush(self):
        self.console.flush()
        if self.file is not None:
            self.file.flush()
            os.fsync(self.file.fileno())

    def close(self):
        self.console.close()
        if self.file is not None:
            self.file.close()


class TFLogger(object):
    def __init__(self, log_dir=None):
        """Create a summary writer logging to log_dir."""
        if log_dir is not None:
            mkdir_if_missing(log_dir)
        self.writer = tf.summary.FileWriter(log_dir)

    def scalar_summary(self, tag, value, step):
        """Log a scalar variable."""
        summary = tf.Summary(value=[tf.Summary.Value(tag=tag, simple_value=value)])
        self.writer.add_summary(summary, step)
        self.writer.flush()

    def image_summary(self, tag, images, step):
        """Log a list of images."""

        img_summaries = []
        for i, img in enumerate(images):
            # Write the image to a string
            try:
                s = StringIO()
            except:
                s = BytesIO()
            scipy.misc.toimage(img).save(s, format="png")

            # Create an Image object
            img_sum = tf.Summary.Image(encoded_image_string=s.getvalue(),
                                       height=img.shape[0],
                                       width=img.shape[1])
            # Create a Summary value
            img_summaries.append(tf.Summary.Value(tag='%s/%d' % (tag, i), image=img_sum))

        # Create and write Summary
        summary = tf.Summary(value=img_summaries)
        self.writer.add_summary(summary, step)
        self.writer.flush()

    def histo_summary(self, tag, values, step, bins=1000):
        """Log a histogram of the tensor of values."""

        # Create a histogram using numpy
        counts, bin_edges = np.histogram(values, bins=bins)

        # Fill the fields of the histogram proto
        hist = tf.HistogramProto()
        hist.min = float(np.min(values))
        hist.max = float(np.max(values))
        hist.num = int(np.prod(values.shape))
        hist.sum = float(np.sum(values))
        hist.sum_squares = float(np.sum(values ** 2))

        # Drop the start of the first bin
        bin_edges = bin_edges[1:]

        # Add bin edges and counts
        for edge in bin_edges:
            hist.bucket_limit.append(edge)
        for c in counts:
            hist.bucket.append(c)

        # Create and write Summary
        summary = tf.Summary(value=[tf.Summary.Value(tag=tag, histo=hist)])
        self.writer.add_summary(summary, step)
        self.writer.flush()

    def close(self):
        self.writer.close()


def write_results(labels,preds,result_path):
    with open("/workspace/xqq/datasets/CCR/char_dict.txt", 'r') as f:
        lines = [i.strip() for i in f.readlines()]
        id2char = {}
        for idx, char in enumerate(lines):
            id2char[idx] = char
    with open(result_path, 'w') as fw:
        for i in range(len(labels)):
            fw.write('{} {}\n'.format(id2char[labels[i]],id2char[preds[i]]))
    print('Finished writing prediction results')

def test(model,test_loader,step=1,tfLogger=None, final_test=False,save_path=None,use_cuda=True):
    print('Start testing ...')
    start = time()
    model.eval()
    labels = []
    predictions = []
    test_loss = 0
    correct = 0
    for batch_idx, (data,target) in enumerate(tqdm(test_loader)):
        if use_cuda:
            data,target = data.cuda(), target.cuda()
        data,target = Variable(data), Variable(target)
        with torch.no_grad():
            logits = model(data)
            output = F.log_softmax(logits,dim=1)
        test_loss += F.nll_loss(output,target).item()
        pred = output.data.max(1,keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        predictions.append(torch.squeeze(pred.cpu()))
        labels.append(target.cpu())
    acc = correct.numpy()/len(test_loader.dataset)
    test_loss /= len(test_loader)
    print('Finished testing in {}s'.format(time()-start))
    print('\nTest set: test_loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset), 100. * acc))
    if tfLogger is not None:
        info = {
            # 'ce_loss':ce_loss / len(test_loader),
            # 'cf_loss':cf_loss / len(test_loader),
            'test_loss':test_loss,
            'accuracy': acc,
        }
        for tag, value in info.items():
            tfLogger.scalar_summary(tag,value,step)
    if final_test:
        write_results(np.concatenate(labels,0),np.concatenate(predictions,0),result_path=save_path)

    return acc


def train(model,epoch,train_loader, test_loader, optimizer,log_interval,tfLogger=None,use_cuda=True):
    model.train()
    for batch_idx,(data,target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)
        if use_cuda:
            data, target = data.cuda(), target.cuda()
        optimizer.zero_grad()
        logits = model(data)
        output = F.log_softmax(logits, dim=1)
        pred = output.data.max(1,keepdim=True)[1]
        loss = F.nll_loss(output,target)
        cf_loss = torch.tensor(0.).cuda()

        total_loss = loss # + cf_loss
        total_loss.backward()
        optimizer.step()
        correct = pred.eq(target.data.view_as(pred)).cpu().sum()
        batch_acc = correct.numpy() / len(target)
        step = epoch * len(train_loader) + (batch_idx+1)

        if (batch_idx+1) % log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.1f}%)]\tCE_Loss: {:.6f}\tCF_loss: {:.6f}\tTotal_loss: {:.6f}\tAcc:{:.2%}'.format(
                epoch+1, (batch_idx+1) * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item(), cf_loss.item(), total_loss.item(), batch_acc))
            if tfLogger is not None:
                for param_group in optimizer.param_groups:
                    lr = param_group['lr']
                info = {'ce_loss':loss.item(),
                        'cf_loss':cf_loss.item(),
                        'total_loss':total_loss.item(),
                        'accuracy':batch_acc,
                        'learning_rate':lr}
                for tag,value in info.items():
                    tfLogger.scalar_summary(tag,value,step)
        if step % 4000 == 0:
            acc = test(model, test_loader)
            model.train()


class LmdbDataset(data.Dataset):
    def __init__(self, lmdb_path, transform):
        super(LmdbDataset, self).__init__()
        self.lmdb_path = lmdb_path
        self.transform = transform

        self.env = lmdb.open(lmdb_path, max_readers=32, readonly=True)
        assert self.env is not None, "cannot create lmdb obj from %s" % lmdb_path
        self.txn = self.env.begin()
        self.count = int(self.txn.get(b"count"))

    def __len__(self):
        return self.count

    def __getitem__(self, idx):
        image_key = b"image-%08d" % idx
        image_buf = self.txn.get(image_key)
        try:
            image = Image.open(six.BytesIO(image_buf))

        except Exception as e:
            print("Error image: ", image_key)
            return self[(idx + 1) % len(self)]
        if self.transform:
            image = self.transform(image)

        label_key = b"label-%08d" % idx
        label_buf = self.txn.get(label_key)
        target = np.frombuffer(label_buf, dtype=np.int32)

        return image, torch.LongTensor(target).squeeze(0)

def Load_lmdb(train_lmdb, test_lmdb, input_size, batch_size):
    kwargs = {'num_workers': 4, 'pin_memory': True}
    test_transforms = transforms.Compose([transforms.Resize(input_size), # transforms.Grayscale(),
                               transforms.ToTensor(), transforms.Normalize([0.86693, 0.86693, 8.86693], [0.2163, 0.2163, 0.2163])])
    test_data = LmdbDataset(test_lmdb, test_transforms)
    test_loader = data.DataLoader(test_data, batch_size=batch_size, shuffle=False, **kwargs)

    if train_lmdb:
        train_transforms = transforms.Compose([transforms.Resize(input_size),
                               transforms.ToTensor(), transforms.Normalize([0.86693, 0.86693, 8.86693], [0.2163, 0.2163, 0.2163])])
        train_data = LmdbDataset(train_lmdb, train_transforms)
        train_loader = data.DataLoader(train_data, batch_size, shuffle=True, **kwargs)
        print('Loaded {} train images, {} test images'.format(len(train_loader.dataset), len(test_loader.dataset)))
        return train_loader, test_loader
    print('Loaded {} test images'.format(len(test_loader.dataset)))
    return test_loader

def save_checkpoint(state, is_best, fpath='checkpoint.pth.tar'):
  mkdir_if_missing(osp.dirname(fpath))
  torch.save(state, fpath)
  if is_best:
    shutil.copy(fpath, osp.join(osp.dirname(fpath), 'model_best.pth.tar'))


def load_checkpoint(fpath):
  if osp.isfile(fpath):
    checkpoint = torch.load(fpath)
    print("=> Loaded checkpoint '{}'".format(fpath))
    return checkpoint
  else:
    raise ValueError("=> No checkpoint found at '{}'".format(fpath))