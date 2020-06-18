import time
import re


def trans(n):
    if n % 10 == 1:
        return str(n) + 'st'
    elif n % 10 == 2:
        return str(n) + 'nd'
    elif n % 10 == 3:
        return str(n) + 'rd'
    else:
        return str(n) + 'th'


ap = ['am', 'pm']
ordinal = [trans(i) for i in range(367)]
mmm = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
mmmm = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
        'November',
        'December']
we = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
wee = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday']
formats = {
    "M": '{p.mon}', "Mo": "{Mo}", "MM": "{p.mon:02d}", "MMM": "{Mon}", "MMMM": "{Month}",
    "D": "{p.day}", "DD": '{p.day:02d}', "Do": "{Do}", "DDD": "{p.yeday}", "DDDo": "{DDDo}", "DDDD": "{p.yeday:03d}",
    "d": '{p.weekday}', "do": '{do}', "dd": '{dd}', "ddd": '{ddd}', "dddd": '{dddd}',
    "YY": '{YY}', "YYYY": "{p.year}",
    "H": "{p.hour}", "HH": "{p.hour:02d}",
    "h": "{h}", "hh": "{h:02d}",
    "m": "{p.min}", "mm": "{p.min:02d}",
    "s": "{p.sec}", "ss": "{p.sec:02d}",
    "a": "{a}", "A": "{A}"
}


class TimeTool:
    def __init__(self, time_list=[]):
        if len(time_list) == 0:
            self.year, self.mon, self.day, self.hour, self.min, self.sec, self.weekday, self.yeday, _ = time.localtime(
                time.time())
        else:
            if len(time_list) == 6:
                self.year, self.mon, self.day, self.hour, self.min, self.sec = time_list
                self.weekday, self.yeday, _ = time.localtime(time.time())[6:]
            elif len(time_list) == 5:
                self.year, self.mon, self.day, self.hour, self.min = time_list
                self.sec, self.weekday, self.yeday, _ = time.localtime(time.time())[5:]
            elif len(time_list) == 4:
                self.year, self.mon, self.day, self.hour = time_list
                self.min, self.sec, self.weekday, self.yeday, _ = time.localtime(time.time())[4:]
            elif len(time_list) == 3:
                self.year, self.mon, self.day = time_list
                self.hour, self.min, self.sec, self.weekday, self.yeday, _ = time.localtime(time.time())[3:]
            elif len(time_list) == 2:
                self.year, self.mon = time_list
                self.day, self.hour, self.min, self.sec, self.weekday, self.yeday, _ = time.localtime(time.time())[2:]
            elif len(time_list) == 1:
                self.year == time_list
                self.mon, self.day, self.hour, self.min, self.sec, self.weekday, self.yeday, _ = time.localtime(
                    time.time())[1:]

    def iter(self):
        return [self.year, self.mon, self.day, self.hour, self.min, self.sec, self.weekday, self.yeday]

    def iso(self, format_spec='YYYY-MM-DD, HH:mm:ss'):
        li = re.split('[-: ]', format_spec)
        date = ''
        # print(li)
        for i in li:
            try:
                date += formats[i.strip(',')].format(p=self, Mo=ordinal[self.mon], Mon=mmm[self.mon],
                                                     Month=mmmm[self.mon],
                                                     Do=ordinal[self.day],
                                                     DDDo=ordinal[self.yeday], do=ordinal[self.weekday],
                                                     dd=we[self.weekday], ddd=wee[self.weekday],
                                                     dddd=weekdays[self.weekday], YY=str(self.year)[2:],
                                                     h=self.hour % 12, a=ap[self.hour > 12],
                                                     A=ap[self.hour > 12].upper())
            except KeyError:
                return 'Invalid Form'
            else:
                if ',' in i:
                    date += ', '
                elif ':' in format_spec or '-' in format_spec:
                    if (('h' in i.lower() and 'm' in format_spec) or ('m' in i
                                                                      and 's' in format_spec)):
                        date += ':'
                    elif ('Y' in i and 'M' in format_spec) or ('M' in i and 'D' in format_spec):
                        date += '-'
                    else:
                        date += ' '
                else:
                    date += ' '
        return date

    def diff(self, other, mode):
        Diff = [self.year - other.year, self.mon - other.mon, self.day - other.day, self.hour - other.hour,
                self.min - other.min, self.sec - other.sec]

        if mode == 's':
            return abs(
                Diff[0] * 365 * 24 * 3600 + Diff[1] * 30 * 24 * 3600 + Diff[2] * 24 * 3600 + Diff[3] * 3600 + Diff[
                    4] * 60 + Diff[5])
        elif mode == 'm':
            return abs(Diff[0] * 365 * 24 * 60 + Diff[1] * 30 * 24 * 60 + Diff[2] * 24 * 60 + Diff[3] * 60 + Diff[4])
        elif mode == 'h':
            return abs(Diff[0] * 365 * 24 + Diff[1] * 30 * 24 + Diff[2] * 24 + Diff[3])
        elif mode == 'd':
            return abs(Diff[0] * 365 + Diff[1] * 30 + Diff[2])
        elif mode == 'm':
            return abs(Diff[0] * 12 + Diff[1])
        elif mode == 'y':
            return abs(Diff[0])


t = TimeTool([2013, 3, 4, 12, 23, 12])
t2 = TimeTool([2012, 4, 5, 24, 13, 15])
s = 'ymdhms'

for mode in s:
    print(str(t.diff(t2, mode))+mode)
