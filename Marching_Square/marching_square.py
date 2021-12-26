# coding:utf-8
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


class PlotDemo:
    def __init__(self, m, n):
        self._net = None
        self.m = m
        self.n = n

    def _set_default_figure(self, m, n):
        ax = subplot(111)  # 注意:一般都在ax中设置,不再plot中设置
        # 设置主刻度标签的位置,标签文本的格式
        xmajorLocator = MultipleLocator(10)  # 将x主刻度标签设置为10的倍数
        xmajorFormatter = FormatStrFormatter('%1.1f')  # 设置x轴标签文本的格式
        xminorLocator = MultipleLocator(1)  # 将x轴次刻度标签设置为1的倍数
        ymajorLocator = MultipleLocator(10)  # 将y轴主刻度标签设置为10的倍数
        ymajorFormatter = FormatStrFormatter('%1.1f')  # 设置y轴标签文本的格式
        yminorLocator = MultipleLocator(1)  # 将y轴次刻度标签设置为1的倍数
        ax.set_xlim(0, m)
        ax.set_ylim(0, n)
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.set_major_formatter(xmajorFormatter)
        ax.yaxis.set_major_locator(ymajorLocator)
        ax.yaxis.set_major_formatter(ymajorFormatter)
        # 显示次刻度标签的位置,没有标签文本
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)
        ax.xaxis.grid(True, which='minor')  # x坐标轴的网格使用主刻度
        ax.yaxis.grid(True, which='minor')  # y坐标轴的网格使用次刻度

    def show_source(self):
        self._set_default_figure(self.m, self.n)

        if self._net is None:
            raise Exception
        net = self._net.net_info
        shape = net.shape
        xlen = shape[0]
        ylen = shape[1]
        for i in range(xlen):
            for j in range(ylen):
                if net[i][j] > 0:
                    plot(i, j, 'g+')
        show()

    def show_contour(self):
        self._set_default_figure(self.m, self.n)
        net = self._net.net_info
        shape = net.shape
        xlen = shape[0]
        ylen = shape[1]
        for i in range(xlen):
            for j in range(ylen):
                if net[i][j] > 0:
                    plot(i, j, 'g+')

        net = self._net
        utils = MarchSquareUtlis(net)
        lines, line_points = utils.trancing_contours()
        for line_point in line_points:
            x1 = line_point[0][0]
            y1 = line_point[0][1]
            x2 = line_point[1][0]
            y2 = line_point[1][1]
            #plot([x1, x2], [y1, y2], 'r-')

        bool_points = np.ones( len(line_points) )
        curve_lines = []
        for i in range(len(line_points)):
            if bool_points[i]:
                cur_curve = []
                cur_point1 = line_points[i][0]
                cur_point2 = line_points[i][1]
                cur_curve.append(cur_point1)
                cur_curve.append(cur_point2)
                bool_points[i] = False
                j = i+1
                while(j < len(line_points)):
                    if bool_points[j]:
                        tmp_point = line_points[j]
                        if cur_point1 in line_points[j]:
                            if cur_point1 == line_points[j][0]:
                                cur_curve.insert(0, line_points[j][1])
                            else:
                                cur_curve.insert(0, line_points[j][0])
                            cur_point1 = cur_curve[0]
                            cur_point2 = cur_curve[-1]
                            bool_points[j] = False
                            j=i+1
                            print("cur_curve:", len(cur_curve))
                            if( len(cur_curve) == 9):
                                print("done")
                            continue

                        if cur_point2 in line_points[j]:
                            if cur_point2 == line_points[j][0]:
                                cur_curve.insert(-1, line_points[j][1])
                            else:
                                cur_curve.insert(-1, line_points[j][0])
                            cur_point1 = cur_curve[0]
                            cur_point2 = cur_curve[-1]
                            bool_points[j] = False
                            j =i+1
                            print("cur_curve:", len(cur_curve))
                            if( len(cur_curve) == 9):
                                print("done")
                            continue
                        j +=1
                    else:
                        j +=1
                curve_lines.append(cur_curve)
        for curve_line in curve_lines:
            cur_line = np.array(curve_line)
            plot(cur_line[:,0], cur_line[:,1], 'r-')
            print(cur_line)
            #break
        #print(curve_lines)






        # width, height = net.net_info.shape
        # arr = net.net_info
        # idx = 0
        # for i in range(width - 1):
        #     for j in range(height - 1):
        #         x, y = i, j
        #         count, v1, v2, v3, v4, v5, v6, v7, v8 = lines[idx]
        #         idx = idx + 1
        #         if count == 0:
        #             continue
        #         if count == 1:
        #             x1 = x + v1
        #             y1 = y + v2
        #             x2 = x + v3
        #             y2 = y + v4
        #             plot([x1, x2],[y1, y2], 'r-')
        #         if count == 2:
        #             x1 = x + v1
        #             y1 = y + v2
        #             x2 = x + v3
        #             y2 = y + v4
        #             plot([x1, x2],[y1, y2], 'r-')
        #             x1 = x + v5
        #             y1 = y + v6
        #             x2 = x + v7
        #             y2 = y + v8
        #             plot([x1, x2],[y1, y2], 'r-')
        show()

    def set_net_info(self, net_info):
        self._net = net_info


class RandomGenNet(object):

    def __init__(self):
        self.arr = self._gen_random()

    def __init__(self, m, n):
        self.arr = self._gen_random(m, n)

    @property
    def net_info(self):
        return self.arr

    def _gen_random(self, m=100, n=100):
        return np.zeros((m, n), dtype='double')

    def add_circle(self, center_x, center_y, radius, val):
        r = int(radius + 0.5)
        for x in range(center_x - r, center_x + r):
            rx = np.abs(center_x - x)
            ry = int(np.sqrt(radius * radius - rx * rx))
            for y in range(ry):
                self.arr[x][center_y - y] = val
                self.arr[x][center_y + y] = val
        return

    def add_retangle(self, lf_up_x, lf_up_y, width, height, val):
        for i in range(width):
            for j in range(height):
                self.arr[lf_up_x + i][lf_up_y + j] = val


# clock-wise, top-left|top-right|bottom-right|bottom_left
def get_retangle_bit(v1, v2, v3, v4):
    return v1 << 3 | v2 << 2 | v3 << 1 | v4


# shift relative to top-left
def get_retangle_shift(bitval):
    if bitval == 0 or bitval == 15:
        return (0, None, None, None, None, None, None, None, None)
    if bitval == 1 or bitval == 14:
        return (1, 0, 0.5, 0.5, 1, None, None, None, None)
    if bitval == 2 or bitval == 13:
        return (1, 0.5, 1, 1, 0.5, None, None, None, None)
    if bitval == 3 or bitval == 12:
        return (1, 0, 0.5, 1, 0.5, None, None, None, None)
    if bitval == 4 or bitval == 11:
        return (1, 0.5, 0, 1, 0.5, None, None, None, None)
    if bitval == 5:
        return (2, 0, 0.5, 0.5, 0, 0.5, 1, 1, 0.5)
    if bitval == 6 or bitval == 9:
        return (1, 0.5, 0, 0.5, 1, None, None, None, None)
    if bitval == 7 or bitval == 8:
        return (1, 0, 0.5, 0.5, 0, None, None, None, None)
    if bitval == 10:
        return (2, 0, 0.5, 0.5, 1, 0.5, 0, 1, 0.5)


class MarchSquareUtlis(object):

    def __init__(self, net):
        self.net = net

    def trancing_contours(self):
        lines = []
        ret = []
        width, height = self.net.net_info.shape
        arr = self.net.net_info
        for i in range(width - 1):
            for j in range(height - 1):
                v1 = int(arr[i][j])
                v2 = int(arr[i + 1][j])
                v3 = int(arr[i + 1][j + 1])
                v4 = int(arr[i][j + 1])
                bitv = get_retangle_bit(v1, v2, v3, v4)
                net_shift = get_retangle_shift(bitv)

                count, v1, v2, v3, v4, v5, v6, v7, v8 = net_shift


                if count == 1:
                    x1 = i + v1
                    y1 = j + v2
                    x2 = i + v3
                    y2 = j + v4
                    lines.append([[x1, y1], [x2, y2]])
                if count == 2:
                    x1 = i + v1
                    y1 = j + v2
                    x2 = i + v3
                    y2 = j + v4
                    lines.append([[x1, y1], [x2, y2]])

                    x1 = i + v5
                    y1 = j + v6
                    x2 = i + v7
                    y2 = j + v8
                    lines.append([[x1, y1], [x2, y2]])

                ret.append(net_shift)
        return ret, lines


demo = PlotDemo(100, 100)
netinfo = RandomGenNet(100, 100)
netinfo.add_circle(20, 20, 10, 1)
netinfo.add_circle(70, 50, 20, 1)
netinfo.add_retangle(20, 45, 40, 20, 1)
#netinfo.add_retangle(70, 50, 10, 10, 1)

demo.set_net_info(netinfo)
#demo.show_source()
demo.show_contour()
# print(get_retangle_bit(1, 1, 1, 0))