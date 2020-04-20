import re

def sentences_regex() -> str:
  return '([\.\?!][\'\"\u2018\u2019\u201c\u201d\)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)\s+)'

def date_regex() -> str:
  hari = r"([[Ss]enin|[Ss]elasa|[Rr]abu|[Kk]amis|[Jj]umat|[Ss]abtu|[Mm]inggu])"
  comma = "(\,*\s*)"
  dayMonthYear = "([\d]{1,2}\s*[jfmasond]\w*\s*\d{4})"
  dateWord = "((\({0,1}[\d]{1,2}(\.|-|\/)[\d]{1,2}(\.|-|\/)[\d]{2,4}\){0,1}))"
  time = "\s([0-9]|0[0-9]|1[0-9]|2[0-3])(\:|\.)[0-5][0-9]\s([W]\w{2}){0,1}"
  pukul = "([Pp]ukul){0,1}"
  haricomma = hari + comma
  pukulTime = "\s*" + pukul + time 
  fullPosible = [
    haricomma + dateWord + dayMonthYear + pukulTime,
    haricomma + dayMonthYear + pukulTime,
    haricomma + dateWord + dayMonthYear,
    haricomma + dateWord + pukulTime,
    haricomma + dayMonthYear,
    haricomma + dateWord,
    dayMonthYear + pukulTime,
    dateWord + pukulTime,
    hari + pukulTime,
    dayMonthYear,
    dateWord,
    hari,
    pukul + time
  ]

  return "|".join(fullPosible)

def numbers_regex()->str:
  return "(^(\d+((\.|\,)(\d+)){0,1})|\s(\d+((\.|\,)(\d+)){0,1}))\s(([^w](\w+)))";
