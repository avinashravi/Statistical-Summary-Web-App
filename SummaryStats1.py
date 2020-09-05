# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 22:49:16 2020

@author: v-avravi
"""

from flask import Flask, request, render_template, session
import csv 
from datetime import datetime

#Functions
def find_median(sorted_list):
        indices = []
    
        list_size = len(sorted_list)
        median = 0
    
        if list_size % 2 == 0:
            indices.append(int(list_size / 2) - 1)  # -1 because index starts from 0
            indices.append(int(list_size / 2))
    
            median = (sorted_list[indices[0]] + sorted_list[indices[1]]) / 2
            pass
        else:
            indices.append(int(list_size / 2))
    
            median = sorted_list[indices[0]]
            pass
    
        return median, indices
        pass

def Min(data):
    return min(data)    
    
def Quartile1(data):
    samples = sorted(data) 
    median, median_indices = find_median(samples)
    Q1, Q1_indices = find_median(samples[:median_indices[0]])
    Q2, Q2_indices = find_median(samples[median_indices[-1] + 1:])
    return Q1
    
def Median(data):
    data = sorted(data)
    if len(data)%2==1:
        return data[len(data)/2]
    else:
        return (data[(len(data)/2)-1]+data[len(data)/2])/2.0
    
def Mean(data):
    return sum(data)/len(data)
    
def Quartile3(data):
    samples = sorted(data)
    median, median_indices = find_median(samples)
    Q1, Q1_indices = find_median(samples[:median_indices[0]])
    Q2, Q2_indices = find_median(samples[median_indices[-1] + 1:])
    return Q2
    
def Max(data):
    return max(data)    


def to_integer(dt_time):
    return [int(100000000*ele.year + 1000000*ele.month + 10000*ele.day + 100*ele.hour + 1*ele.minute) for ele in dt_time]

def dMin(data):
    d = min(data)    
    return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
    
def dQuartile1(data):
    samples = sorted(data) 
    median, median_indices = find_median(samples)
    Q1, Q1_indices = find_median(samples[:median_indices[0]])
    Q2, Q2_indices = find_median(samples[median_indices[-1] + 1:])
    d = Q1
    return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
    
def dMedian(data):
    data = sorted(data)
    if len(data)%2==1:
        d = data[len(data)/2]
        return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
    else:
        d = (data[(len(data)/2)-1]+data[len(data)/2])/2.0
        return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
    
def dMean(data):
    d = sum(data)/len(data)
    return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))

def dQuartile3(data):
    samples = sorted(data) 
    median, median_indices = find_median(samples)
    Q1, Q1_indices = find_median(samples[:median_indices[0]])
    Q2, Q2_indices = find_median(samples[median_indices[-1] + 1:])
    d = Q2
    return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
    
def dMax(data):
    d = max(data)    
    return (''.join(list(str(d))[0:4])+'-'+''.join(list(str(d))[4:6])+'-'+''.join(list(str(d))[6:8])+' '+''.join(list(str(d))[8:10])+':'+''.join(list(str(d))[10:12]))
 

app = Flask(__name__)

# =============================================================================
# @app.route('/dropdown', methods=['POST','GET'])
# def dropdown(header):
#     return render_template('SummaryStats2.html', fields=header)
# =============================================================================

@app.route('/summarystats.com', methods=['GET'])
def my_form():
    return render_template("SummaryStats1.html")

#data = [[]]
#header = list()
#csv_file = None
header = None
data = None

@app.route('/summarystats.com/schemadefinition', methods=['POST','GET'])
def my_form_post():
    #global csv_file
    csv_file = request.form['file']    
    print(csv_file)
    #return csv_file

    with open(csv_file) as file:        
        global data
        data = list(csv.reader(file, delimiter=','))
        global header
        header = data[0]
        data.pop(0)
        data = zip(*data)
        datatypes = ['str','int','float','bool','dateTime']
        length = len(datatypes)
        return render_template('SummaryStats2.html', fields=header, datatypes=datatypes, length=length)
        #data_type=[]
        #dropdown(header)
 
#data_type = []
@app.route('/summarystats.com/summary', methods=['POST'])
def my_form_types():
    global header
    global data
    global length
    data_type = []
    for i in range(0,len(header)):
        data_type.append(request.form.get(header[i]))
        print data_type[i] 
        if data_type[i]=='float':
            data[i] = [float(ele) for ele in data[i]] 
        if data_type[i]=='int':
            data[i] = [int(ele) for ele in data[i]] 
        if data_type[i]=='dateTime':
            data[i] = [datetime.strptime(ele, '%m/%d/%Y %H:%M') for ele in data[i]]
            data[i] = to_integer(data[i])             
    
    summary = []
    
    for i in range(0,len(data_type)):
        print("\n"+header[i])
        summary_measure = []
        summary_measure.append(header[i])
        FALSE=0
        TRUE=0
        if data_type[i]=="str":
            print("Length:"+str(len(data[i])))
            print("Class:character")
            print("Mode:character")
            summary_measure.append("Length:"+str(len(data[i])))
            summary_measure.append("Class:character")
            summary_measure.append("Mode:character")
        elif data_type[i]=="bool":
            print("Mode:logical")
            summary_measure.append("Mode:logical")
            for j in data[i]:
                if j in ("FALSE,0"):
                    FALSE+=1
                else:
                    TRUE+=1
            if FALSE>0:
                print("FALSE:"+str(FALSE))
                summary_measure.append("FALSE:"+str(FALSE))
            if TRUE>0:
                print("TRUE:"+str(TRUE))
                summary_measure.append("TRUE:"+str(TRUE))
        elif data_type[i]=="dateTime":
            print("Min.:"+str(dMin(data[i])))
            print("1st Qu.:"+str(dQuartile1(data[i])))
            print("Median:"+str(dMedian(data[i])))
            print("Mean:"+str(dMean(data[i])))
            print("3rd Qu.:"+str(dQuartile3(data[i])))
            print("Max.:"+str(dMax(data[i])))
            summary_measure.append("Min.:"+str(dMin(data[i])))
            summary_measure.append("1st Qu.:"+str(dQuartile1(data[i])))
            summary_measure.append("Median:"+str(dMedian(data[i])))
            summary_measure.append("Mean:"+str(dMean(data[i])))
            summary_measure.append("3rd Qu.:"+str(dQuartile3(data[i])))
            summary_measure.append("Max.:"+str(dMax(data[i])))
        else:
            print("Min.:"+str(Min(data[i])))
            print("1st Qu.:"+str(Quartile1(data[i])))
            print("Median:"+str(Median(data[i])))
            print("Mean:"+str(Mean(data[i])))
            print("3rd Qu.:"+str(Quartile3(data[i])))
            print("Max.:"+str(Max(data[i])))    
            summary_measure.append("Min.:"+str(Min(data[i])))
            summary_measure.append("1st Qu.:"+str(Quartile1(data[i])))
            summary_measure.append("Median:"+str(Median(data[i])))
            summary_measure.append("Mean:"+str(Mean(data[i])))
            summary_measure.append("3rd Qu.:"+str(Quartile3(data[i])))
            summary_measure.append("Max.:"+str(Max(data[i])))    
        summary_measure.append("")
        summary.append(summary_measure)    
    return render_template('SummaryStats3.html', summary=summary, fields=header)
        
        
# =============================================================================
# @app.route('/', methods=['POST','GET'])
# def dropdown():    
#     return render_template('SummaryStats2.html', fields=header, datatypes=datatypes)            
# 
# =============================================================================
        
# =============================================================================
#         for i in range(0,len(header)):
#             #print("enter data type of "+header[column]+": ")
#             #"<p>enter datatype of {}:</p>".format(header[i])
#             data_type.append(str(request.form["number"]))#("<p>{!r} is not a number.</p>\n".format(request.form["number"]))(raw_input(<p>enter data type of {header[i]}:</p>))#"+header[i]+": "))
#             if data_type[i]=='float':
#                 data[i] = [float(ele) for ele in data[i]] 
#             if data_type[i]=='int':
#                 data[i] = [int(ele) for ele in data[i]] 
#             if data_type[i]=='dateTime':
#                 data[i] = [datetime.strptime(ele, '%m/%d/%Y %H:%M') for ele in data[i]]
#                 data[i] = to_integer(data[i])             
#              
#         for i in range(0,len(data_type)):
#             print("\n"+header[i])
#             FALSE=0
#             TRUE=0
#             if data_type[i]=="str":
#                 print("Length:"+str(len(data[i])))
#                 print("Class:character")
#                 print("Mode:character")
#             elif data_type[i]=="bool":
#                 print("Mode:logical")
#                 for j in data[i]:
#                     if j in ("FALSE,0"):
#                         FALSE+=1
#                     else:
#                         TRUE+=1
#                 if FALSE>0:
#                     print("FALSE:"+str(FALSE))
#                 if TRUE>0:
#                     print("TRUE:"+str(TRUE))
#             elif data_type[i]=="dateTime":
#                 print("Min.:"+str(dMin(data[i])))
#                 print("1st Qu.:"+str(dQuartile1(data[i])))
#                 print("Median:"+str(dMedian(data[i])))
#                 print("Mean:"+str(dMean(data[i])))
#                 print("3rd Qu.:"+str(dQuartile3(data[i])))
#                 print("Max.:"+str(dMax(data[i])))
#             else:
#                 print("Min.:"+str(Min(data[i])))
#                 print("1st Qu.:"+str(Quartile1(data[i])))
#                 print("Median:"+str(Median(data[i])))
#                 print("Mean:"+str(Mean(data[i])))
#                 print("3rd Qu.:"+str(Quartile3(data[i])))
#                 print("Max.:"+str(Max(data[i])))
#     
#     
#     
#     
#     summary = file_name.summaryCalc()
#     return summary
# =============================================================================

if __name__ == "__main__":
    app.run()
    
    