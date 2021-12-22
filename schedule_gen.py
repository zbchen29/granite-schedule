import calendar
import datetime
from reportlab.lib import colors, pagesizes as ps
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.doctemplate import SimpleDocTemplate

def main():
    while True:
        year_input = input("Input the schedule year: ")
        try:
            year = stringToYear(year_input)
        except:
            print("Invalid year input!")
        else:
            filename = "schedule_" + year_input + ".pdf"
            create_calendar(year, filename)
            print("Calendar schedule saved to: " + filename)
            break

def stringToYear(year_input):
    '''Converts string to year integer while checking validity'''
    year = int(year_input)
    if (year <= 0):
        raise ValueError()
    return year

def create_calendar(year, filename):
    '''Creates and saves the calendar for the given year to the filename'''
    doc = create_doc(filename)
    doc_elements = [create_table(create_data(year, week), shaded=True) for week in range(week_count(year))]
    doc.build(doc_elements)

def week_count(year):
    '''Number of Monday-Sunday weeks that a given year spans (53 or 54)'''
    # There are 54 weeks only when the year starts on Sunday and is a leap year
    return 54 if calendar.isleap(year) and datetime.date(year, 1, 1).weekday() == 6 else 53

def create_doc(filename):
    '''Return a SimpleDocTemplate to be saved with specified filename'''
    return SimpleDocTemplate(
        filename,
        pagesize=ps.landscape(ps.letter),
        leftMargin=0.25*ps.inch,
        rightMargin=0.25*ps.inch,
        bottomMargin=0.1*ps.inch,
        topMargin=0.75*ps.inch)

def create_data(year, week):
    '''Return nested array of table entries for schedule based on year and week'''
    data = []

    # Table contents
    data.append([year, "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"])
    data.append(get_week_header(year, week))
    data.extend([["View Granite"] + 7 * [""] for _ in range(3)])
    current_time = datetime.datetime(1,1,1,hour=10)
    for i in range(8):
        data.append([current_time.strftime("%#I:%M %p")] + 7 * [""])
        data.append(8 * [""])
        current_time += datetime.timedelta(hours=1)

    return data

def get_week_header(year, week):
    '''Return a list of string dates corresponding to the year and zero-indexed week'''
    new_year_date = datetime.date(year, 1, 1)
    year_start_date = new_year_date - datetime.timedelta(days=new_year_date.weekday())
    week_start_date = year_start_date + datetime.timedelta(days=7*week)
    return ["WEEK " + str(week + 1)] + [(week_start_date + datetime.timedelta(days=i)).strftime("%#m/%#d") for i in range(7)]

def lunarDateToString(lunar_date):
    return str(lunar_date.month) + "-" + str(lunar_date.day) + ""

def create_table(data, shaded=False):
    '''Return a table with proper style from data array'''
    # Style with no shading
    schedule_style = [
        ("INNERGRID",       (0,0), (-1,-1), 1, colors.gainsboro),
        ("OUTLINE",         (0,0), (-1,-1), 2, colors.black),
        ("LINEBELOW",       (0,1), (-1,1),  2, colors.black),
        ("LINEBELOW",       (0,4), (-1,4),  2, colors.black),
        ("LINEAFTER",       (0,0), (0,-1),  2, colors.black),
        ("ALIGN",           (0,0), (-1,-1), "CENTER"),
        ("VALIGN",          (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS",  (0,0), (-1,-1), [colors.white, (0.96, 0.96, 0.96)]),
        ("FONT",            (0,0), (0,0),   "Helvetica-Bold", 14),
        ("FONT",            (1,0), (-1,0),  "Helvetica-Bold", 12),
        ("FONT",            (0,1), (0,-1),  "Helvetica-Bold", 12),
        ("FONT",            (1,1), (-1,-1), "Helvetica", 12),
        ("TEXTCOLOR",       (1,0), (1,0),   colors.crimson),
        ("TEXTCOLOR",       (2,0), (2,0),   colors.royalblue),
        ("TEXTCOLOR",       (3,0), (3,0),   colors.turquoise),
        ("TEXTCOLOR",       (4,0), (4,0),   colors.darkorange),
        ("TEXTCOLOR",       (5,0), (5,0),   colors.purple),
        ("TEXTCOLOR",       (6,0), (6,0),   colors.gold),
        ("TEXTCOLOR",       (7,0), (7,0),   colors.green)
        ]

    # Style with shaded Monday, Wednesday, and Sunday cells
    if shaded:
        schedule_style.extend([
            ("BACKGROUND", (7,5), (7,-1), colors.silver)
        ])

    cols = 8
    rows = 21
    widths = cols * [10.5 / cols * ps.inch]
    heights = rows * [7.25 / rows * ps.inch]
    table = Table(data, widths, heights)
    table.setStyle(TableStyle(schedule_style))
    return table

if __name__ == "__main__":
    main()
    