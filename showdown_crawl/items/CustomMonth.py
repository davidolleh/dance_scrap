from enum import Enum


class CustomMonth(Enum):
    January = ("January", 1)
    February = ("February", 2)
    March = ("March", 3)
    April = ("April", 4)
    May = ("May", 5)
    June = ("June", 6)
    July = ("July", 7)
    August = ("August", 8)
    September = ("September", 9)
    October = ("October", 10)
    November = ("November", 11)
    December = ("December", 12)

    @classmethod
    def getEnumMonth(cls, month: str):
        J1 = "January"
        F2: str = "February"
        M3: str = "March"
        A4: str = "April"
        M5: str = "May"
        J6: str = "June"
        J7: str = "July"
        A8: str = "August"
        S9: str = "September"
        O10: str = "October"
        N11: str = "November"
        D12: str = "December"

        if month == J1 or month == J1.upper() or month == J1.lower() or month == "01":
            return cls.January
        elif month == F2 or month == F2.upper() or month == F2.lower() or month == "02":
            return cls.February
        elif month == M3 or month == M3.upper() or month == M3.lower() or month == "03":
            return cls.March
        elif month == A4 or month == A4.upper() or month == A4.lower() or month == "04":
            return cls.April
        elif month == M5 or month == M5.upper() or month == M5.lower() or month == "05":
            return cls.May
        elif month == J6 or month == J6.upper() or month == J6.lower() or month == "06":
            return cls.June
        elif month == J7 or month == J7.upper() or month == J7.lower() or month == "07":
            return cls.July
        elif month == A8 or month == A8.upper() or month == A8.lower() or month == "08":
            return cls.August
        elif month == S9 or month == S9.upper() or month == S9.lower() or month == "09":
            return cls.September
        elif month == O10 or month == O10.upper() or month == O10.lower() or month == "10":
            return cls.October
        elif month == N11 or month == N11.upper() or month == N11.lower() or month == "11":
            return cls.November
        elif month == D12 or month == D12.upper() or month == D12.lower() or month == "12":
            return cls.December

