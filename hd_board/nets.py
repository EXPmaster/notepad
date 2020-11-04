import torch
import torch.nn as nn

class SEModule(nn.Module):
    def __init__(self, channels, reduction=16):
        super(SEModule, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc1 = nn.Conv2d(channels, channels // reduction, kernel_size=1, padding=0)
        self.relu = nn.ReLU(inplace=True)
        self.fc2 = nn.Conv2d(channels // reduction, channels, kernel_size=1, padding=0)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        module_input = x
        x = self.avg_pool(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return module_input * x # , x

class BasicConv(nn.Module):
    def __init__(self, in_channel, out_channels, use_relu=True, kernel_size=3,
            stride=1, padding=1, bias=True):
        super(BasicConv, self).__init__()
        self.conv = nn.Conv2d(in_channel, out_channels, kernel_size, stride=stride, padding=padding, bias=bias)
        self.bn = nn.BatchNorm2d(out_channels)
        if use_relu:
            self.activation = nn.ReLU(inplace=True)
        self.use_relu = use_relu
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        if self.use_relu:
            x = self.activation(x)
        return x
        
class SOAT(nn.Module):
    def __init__(self, num_classes=3755):
        super(SOAT, self).__init__()
        self.features = nn.Sequential(
                BasicConv(1, 64, bias=False),
                BasicConv(64, 64, bias=False),
                nn.AvgPool2d(kernel_size=3, stride=2, padding=1),
                BasicConv(64, 96, bias=False),
                BasicConv(96, 64, bias=False),
                BasicConv(64, 96, bias=False),
                nn.AvgPool2d(kernel_size=3, stride=2, padding=1),
                BasicConv(96, 128, bias=False),
                BasicConv(128, 96, bias=False),
                BasicConv(96, 128, bias=False),
                nn.AvgPool2d(kernel_size=3, stride=2, padding=1),
                BasicConv(128, 256, bias=False),
                BasicConv(256, 192, bias=False),
                BasicConv(192, 256, bias=False),
                nn.AvgPool2d(kernel_size=3, stride=2, padding=1),
                BasicConv(256, 448, bias=False),
                BasicConv(448, 256, bias=False),
                BasicConv(256, 448, bias=False))


        self.attn1 = nn.Sequential(
                SEModule(448),
                nn.ReLU(inplace=True))
        self.attn2 = nn.Sequential(
                SEModule(448),
                nn.ReLU(inplace=True))
        self.fc1 = nn.Linear(448*6*6, 768)
        self.fc2 = nn.Linear(448*6*6, 768)
        # self.dropout = nn.Dropout(0.5)
        self.classifier = nn.Sequential(
                nn.ReLU(inplace=True),
                nn.Dropout(),
                nn.Linear(768*2, num_classes))

    def forward(self, x):
        x = self.features(x)

        attn1 = self.attn1(x)
        attn2 = self.attn2(x)

        attn1 = attn1.view(x.size(0), -1)
        attn2 = attn2.view(x.size(0), -1)
        # x = self.GAP(x)
        f1 = self.fc1(attn1)
        f2 = self.fc2(attn2)
        x = torch.cat([f1, f2], dim=1)
        x = self.classifier(x)
        return x, f1, f2




if __name__ == '__main__':
    x = torch.randn(10, 1, 96, 96)
    model = SOAT(num_classes=3755)
    print(model)
    y = model(x)
    print(y.size())
