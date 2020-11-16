from clock import *

#-------------------- Askisi 1 ----------------------------
class RomanCascadeCounter(CascadeCounter):
    """Metritis CascadeCounter me endei3eis me rwmaikous ari8mous."""
    def __str__(self):
        tens = self.value // 10 #πόσες δεκάδες
        units = self.value % 10 #πόσες μονάδες
        tens_s = 'L' if tens == 5 else tens*'X' #αν οι δεκάδες είναι 5 τότε tens_s = L αλλιώς tens_s = tens * X
        if units < 5: #αν οι μονάδες μικρότερες του 5, units * I
            units_s = units*'I'
        else: # αλλιώς V + units_s - 5* I
            units_s = 'V' + (units-5)*'I'

        sz = len(tens_s + units_s)
        return '-'*(9-sz) + tens_s + units_s #επέστρεψε 9 πα΄ύλες μείον το len(tens_s + units_s),
        #όπου στη θέση τους οι δεκάδες και οι μονάδες μεταφρασμένες σε ρωμαικό σύστημα


class RomanClock(Clock):
    """Roloi me endei3eis me rwmaika noumera.

    >>> c = RomanClock(23, 59, 58)
    >>> str(c)
    '----XXIII:---LVIIII:----LVIII'
    >>> c.advance()
    >>> print(c)
    ----XXIII:---LVIIII:---LVIIII
    >>> c.advance()
    >>> print(c)
    ---------:---------:---------
    >>> c.advance()
    >>> print(c)
    ---------:---------:--------I
    >>> c.advance()
    >>> print(c)
    ---------:---------:-------II
    """
    def __init__(self, h, m, s): #See Clock in clock.py
    #Sends each variable to RomanCascadeCounter. Each variable is calculated and consisted by the previous one.
        self._h = RomanCascadeCounter(None, 24, h)
        self._m = RomanCascadeCounter(self._h, 60, m)
        self._s = RomanCascadeCounter(self._m, 60, s)


#-------------------- Askisi 2 ----------------------------
class DayCounter(CyclicCounter):
    """Metritis hmeras.

    Paradeigmata:
    >>> d = DayCounter()
    >>> str(d)
    'Sunday'
    >>> d.advance()
    >>> print(d)
    Monday
    >>> d2 = DayCounter('Saturday')
    >>> str(d2)
    'Saturday'
    >>> d2.advance()
    >>> str(d2)
    'Sunday'
    >>> d2.advance()
    >>> str(d2)
    'Monday'
    """
    _days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',\
            'Thursday', 'Friday', 'Saturday']
    def __init__(self, day = 'Sunday'):
        CyclicCounter.__init__(self, len(DayCounter._days), DayCounter._days.index(day)) #το len είναι οι 7 ημέρες period, πρ΄ε΄πει να είναι ακέραιος γιατί η CyclicCounter επιστρέφει ακέραιο.

    def __str__(self):
        return DayCounter._days[self.value] #πρέπει να επιστρέφει str, όμως το σημείο μέσα στη λίστα _days που δείχνει την ημέρα μας.


#-------------------- Askisi 3 ----------------------------
class DayClock(Clock):
    """Roloi me endei3h hmeras.

    >>> c = DayClock(23, 59, 58, 'Sunday')
    >>> str(c)
    '23:59:58 Sunday'
    >>> c.advance()
    >>> str(c)
    '23:59:59 Sunday'
    >>> c.advance()
    >>> str(c)
    '00:00:00 Monday'
    >>> c.advance()
    >>> str(c)
    '00:00:01 Monday'

    An paralhf8ei to onoma imeras (teleytaio orisma ston kataskeyasti)
    tote pairnei timi 'Sunday', px.:
    >>> c = DayClock(6, 35, 0)
    >>> print(c)
    06:35:00 Sunday
    """
    def __init__(self, h = 0, m = 0, s = 0, day = 'Sunday'):
        self._d = DayCounter(day)
        self._h = CascadeCounter(self._d, 24, h)
        self._m = CascadeCounter(self._h, 60, m)
        self._s = CascadeCounter(self._m, 60, s)

    def __str__(self):
        return "{0}:{1}:{2} {3}".format(self._h, self._m, self._s, self._d)


#-------------------- Askisi 4 ----------------------------
class Counter_Reversed:
    def __init__(self, start = 59):
        self.value = start

    def advance(self):
        self.value = self.value - 1

    def __str__(self):
        return str(self.value)

class CyclicCounterReversed(Counter_Reversed):
        def __init__(self, period, start = 59):
            """Arxikopoihsh kyklikou metriti.

            period -- dinei tin timi tis self.period
            start -- arxiki timi (an den do8ei einai 0)
            """
            self.period = period
            Counter_Reversed.__init__(self, start)

        def advance(self):
            self.value = (self.value - 1) % self.period

        def __str__(self):
            s = Counter_Reversed.__str__(self)
            return (len(str(self.period-1))-len(s))*'0' + s


class CascadeCounterReversed(CyclicCounterReversed):
    def __init__(self, next, period, start = 59):
        CyclicCounterReversed.__init__(self, period, start)
        self.next = next
    def advance(self):
        CyclicCounterReversed.advance(self)
        if self.next and self.value == 59:
            self.next.advance()

class Timer(Counter_Reversed):
    """Antistrofos xronometritis.

    >>> c = Timer(0, 0, 2)
    >>> str(c)
    '00:00:02'
    >>> c.advance()
    >>> str(c)
    '00:00:01'
    >>> c.advance()
    >>> str(c)
    '00:00:00'
    >>> c.advance()
    >>> str(c)
    'TI DI DI DI'
    >>> c.advance()
    >>> str(c)
    'TI DI DI DI'
    """
    """GRAPSTE TON KWDIKA SAS APO KATW."""

    def __init__(self, h, m, s):
        self._h = CyclicCounterReversed(24, h)
        self._m = CascadeCounterReversed(self._h, 60, m)
        self._s = CascadeCounterReversed(self._m, 60, s)

    def advance(self):
        self._s.advance()

    def __str__(self):
        if "{0}:{1}:{2}".format(self._h, self._m, self._s) == "00:00:00":
            return 'TI DI DI DI'
        return "{0}:{1}:{2}".format(self._h, self._m, self._s)
