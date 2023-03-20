import csv
from matplotlib import pyplot as plt

# Count the number of 0V readings in a given window of the dataset (inclusive)
def rotations_slide(left, right, list):
    rotations = 0
    for i in range(left, right):
	# Can't convert the empty string to a number so do a shitty guard
        if list[i] != '' and float(list[i]) == 0:
            rotations = rotations + 1
    return rotations

# Import cleaned CSV and isolate voltage readings
# Note that I used a file with just two columns - ticks and analog
file = open("rpm_test.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
voltages = [row[1] for row in data[1:]]

# Collect RPM approximations and their respective times by a moving average ish thing
rpms = []
times = []
window = 5000
for i in range(0, len(voltages) - window - 1, 50):
    rotations = rotations_slide(i, i + window - 1, voltages)
    rpms.append(rotations * (float(60000)/window))
    times.append(float(i + window - 1)/2/1000)

# Make and save plot
plt.plot(times, rpms)
plt.ylabel("RPM")
plt.xlabel("Seconds")
plt.title("Rear Wheel Stationary Test RPM Time Dependence")
plt.savefig("test.pdf")
