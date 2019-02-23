#Very simple debugger that you can use to check some use case scenarios or read out clock registers.

import DS1307

clock = DS1307.DS1307(1, 0x68)

#==================================
# Midnight 23:59:00
#==================================
#clock._write(clock._REG_HOURS, 0x23)
#clock._write(clock._REG_MINUTES, 0x59)
#clock._write(clock._REG_SECONDS, 0x00)

#==================================
# Stop Oscillator
#==================================
#clock._write(clock._REG_SECONDS, 0x80)

#==========================================================
# Restart Oscillator with 0 seconds written to the register
#==========================================================
#clock._write(clock._REG_SECONDS, 0x00)

#=====================================
# Check 12/24 hour bit (0 for 24 time)
#=====================================
#hourRegisterValue = clock._read(clock._REG_HOURS)
#if not hourRegisterValue >> 6:
#	print 'Clock is in 24 hour mode'
#else:
# 	print 'Clock is in 12 hour mode, 5th bit represents AM/PM'

#==================================
# Read all register values
#==================================
##print('Hour register: ', clock._read(clock._REG_HOURS))
##print('Minute register: ', clock._read(clock._REG_MINUTES))
##print('Seconds register: ', clock._read(clock._REG_SECONDS))
##print('Date register: ', clock._read(clock._REG_DATE))
##print('Day register: ', clock._read(clock._REG_DAY))
##print('Month register: ', clock._read(clock._REG_MONTH))
##print('Year register: ', clock._read(clock._REG_YEAR))
##print('Control register: ', clock._read(clock._REG_CONTROL))

print('Seconds: ', clock._read_seconds())

#==================================
# Print the date and time
#==================================
#print(clock.read_datetime())
print(clock.read_all())
#print(clock.read_str())