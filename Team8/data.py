import csv
import xlrd

folder_name = "Input data/"
coord_file_name = folder_name + "alt_az_radial"
vel_file_name = folder_name + "asteroid_vel"


def main():
    convert_data_files()
    data = read_data()
    return data


def read_data():
    data = {}
    coord_file = coord_file_name + ".csv"
    vel_file = vel_file_name + ".csv"
    fin1 = open(coord_file, 'rt')
    fin2 = open(vel_file, 'rt')
    reader1 = csv.reader(fin1)
    reader2 = csv.reader(fin2)
    for row in reader1:
        break
    for row in reader2:
        break
    for row in reader1:
        data[row[0]] = {}
        data[row[0]]["az"] = float(row[1])
        data[row[0]]["alt"] = float(row[2])
        data[row[0]]["r"] = float(row[3])
    for row in reader2:
        data[row[0]]["vx"] = float(row[1])
        data[row[0]]["vy"] = float(row[2])
        data[row[0]]["vz"] = float(row[3])
    fin1.close()
    fin2.close()
    return data


def store_output(state):
    csv_out = "output.csv"
    fout = open(csv_out, 'wt')
    writer = csv.writer(fout)
    header = ["id", "px", "py", "pz", "vx", "vy", "vz", "time", "min distance"]
    writer.writerow(header)
    for row in state:
        writer.writerow(row)
    fout.close()


def convert_data_files():
    coord_file_in = coord_file_name + ".xlsx"
    coord_file_out = coord_file_name + ".csv"
    vel_file_in = vel_file_name + ".xlsx"
    vel_file_out = vel_file_name + ".csv"
    convertXLStoCSV(coord_file_in, coord_file_out)
    convertXLStoCSV(vel_file_in, vel_file_out)


def convertXLStoCSV(in_file, out_file, sheet_name="Sheet1"):
    try:
        wb = xlrd.open_workbook(in_file)
        sh = wb.sheet_by_name(sheet_name)
        csv_file = open(out_file,'w')
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        csv_file.close()
    except:
        pass
