import argparse, glob, math, os, re
from operator import itemgetter

# EXTRACT DATA FROM DIRECTORY OF SUBJECT DATA FILES
parser = argparse.ArgumentParser("Parse a directory of files")

# Command line control of file locations
parser.add_argument('directory', type=str, help='File locations')

# Command line control of accuracy cutoff
parser.add_argument('accuracy', type=float, help='Accuracy cutoff')

args = parser.parse_args()

filenames = glob.glob(args.directory + '/*.txt')
for filename in filenames:
    with open(filename, 'r') as file:
        try:
            lines = file.readlines()
            srch_lines = []
            for i in range(len(lines)):
                srch = re.findall(r'\b[R,L]H*', lines[i])
                if srch:
                    srch_lines.append(i)

            image = []
            color1 = []
            color2 = []
            response = []
            rt = []
            pd_correct = []

            for i in range(srch_lines[0], srch_lines[-1]):
                fields = lines[i].split(',')
                if 'BREAK' in fields:
                    continue
                elif '99' in fields:
                    continue
                elif '' in fields:
                    continue
                image.append(fields[0])
                color1.append(fields[1])
                color2.append(fields[2])
                response.append(fields[3])
                rt.append(fields[4])
            if not len(image) == len(color1) and len(color1) == len(color2) and len(color2) == len(response) and len(response) == len(rt):
                print('Inspect this file: ' + filename)

            for i in range(len(rt)):
                if color2[i] == '1' and response[i] == 'same':
                    pd_correct.append((image[i],rt[i].rstrip()))
                elif color2[i] == '2' and response[i] == 'diff':
                    pd_correct.append((image[i],rt[i].rstrip()))

            accuracy = len(pd_correct) / len(rt)

            pos1c = []
            pos2c = []
            pos3c = []
            pos4c = []
            pos5c = []
            pos6c = []
            for img,rtm in pd_correct:
                s = img[8]
                if s == '1':
                    pos1c.append(int(rtm))
                elif s == '2':
                    pos2c.append(int(rtm))
                elif s == '3':
                    pos3c.append(int(rtm))
                elif s == '4':
                    pos4c.append(int(rtm))
                elif s == '5':
                    pos5c.append(int(rtm))
                elif s == '6':
                    pos6c.append(int(rtm))
            #if len(pd_correct) != (len(pos1c)+len(pos2c)+len(pos3c)+len(pos4c)+len(pos5c)+ len(pos6c)):
                #print('Check math.')


            if float(accuracy) > args.accuracy:
                print(filename)
                print(accuracy)
                base1 = 0
                for i in range(len(pos1c)):
                    base1 += pos1c[i]
                avg1 = float(base1/len(pos1c))
                print(avg1)

                base2 = 0
                for i in range(len(pos2c)):
                    base2 += pos2c[i]
                avg2 = float(base2 / len(pos2c))
                print(avg2)

                base3 = 0
                for i in range(len(pos3c)):
                    base3 += pos3c[i]
                avg3 = float(base3 / len(pos3c))
                print(avg3)

                base4 = 0
                for i in range(len(pos4c)):
                    base4 += pos4c[i]
                avg4 = float(base4 / len(pos4c))
                print(avg4)

                base5 = 0
                for i in range(len(pos5c)):
                    base5 += pos5c[i]
                avg5 = float(base5 / len(pos5c))
                print(avg5)

                base6 = 0
                for i in range(len(pos6c)):
                    base6 += pos6c[i]
                avg6 = float(base6 / len(pos6c))
                print(avg6)



# # ANALYSIS OF EXTRACTED DATA
#     # AVERAGE - calculated if greater than or equal to cutoff value
#             if accuracy >= args.accuracy:
#                 base = 0
#                 for i in range(len(correct)):
#                     base += int(correct[i])
#                 avg = base / len(correct)
#
#     #STANDARD DEVIATION
#                 instance = []
#                 for i in range(len(correct)):
#                     x = (i - avg)**2
#                     instance.append(x)
#                 std_dev = math.sqrt(sum(instance) / len(instance))
#
#             # Create new file in separate directory containing:
#                 # Accuracy
#                 # Avg RT
#                 if not os.path.exists('Indiv_AVG'):
#                     os.mkdir('Indiv_AVG')
#                 new_dir = os.path.join(os.path.dirname(filename), 'Indiv_AVG')
#                 new_file = os.path.join(new_dir, 'avg_' + os.path.basename(filename))
#                 avg_file = open(new_file,'w')
#                 avg_file.write(str(accuracy) + '\n')
#                 avg_file.write(str(avg) + '\n')
#                 avg_file.write(str(std_dev))
#                 avg_file.close()
#                 print(avg)
            file.close()
        except IndexError:
            print('FILE ' + filename.upper() + ' NEEDS INSPECTION.')






