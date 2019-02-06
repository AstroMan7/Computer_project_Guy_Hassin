from matplotlib import pyplot
import numpy as np
UNCERTAINTIES = ["dy", "dx"]

def read_colums(lines):
    graph = {}
    header = lines[0].lower().split()               #take the 1st line,put it in a list name header
    for i in header:
        graph[i] = []                                #for each argument, create a key and a list for the upcoming values
    for line in lines[1:]:
        values = line.split()                        #take each line of data and put it in a list named values
        if len(values) == 0:
            return graph                             #after all data entered the graph return it
        if len(header) == len(values):
            for column in range(len(header)):
                graph[header[column]] += [float(values[column])]     #add to each key (header) the values and return the dict
        else:
            print('Input file error: Data lists are not the same lenth.')
            return False
    return graph

def row_formula(lines):
    a = cal_a(graph)
    b = cal_b(graph)
    i = 0
    while i < len(graph['x']):
        for value in (graph['x']):
            formula = a * value + b
        i += 1
        print('hhhhhhh')
def read_rows(lines):
    graph = {}
    x= []
    for line in lines:
        values = line.split()           #create a list with the lines(title and data)
        if len(values) == 0:  #empty line
            return graph
        graph[values[0].lower()] = [float(value) for value in values[1:]] #put title in key, put values in value????????להבין טוב יותר
    return graph

def create_graph(file_name):
    file = open(file_name,'r')
    lines = file.readlines()
    if is_colums_input(lines):          # run this if title is in columns, get the output - dict
        if read_colums(lines):
            graph = read_colums(lines)
        else:
            return None
    else:                               # run this if title is in rows
        graph = read_rows(lines)
    if is_valid_graph(graph):
        return graph                      # return True or False
    else:
        return None
        #raise Exception ("Input file error: Data lists are not the same length")

def check_length(graph):
    graph_items  = [len(value) for key, value in graph.items()] # create a list with the length of each key-values///???????/
    return len(set(graph_items)) == 1                           #return true if all arguments in list of values-count for each key is the same (uniqe)

def check_uncertainties(graph):            # for each UNCERT call the func to check if valid
    for uncertainty in UNCERTAINTIES:
        if not check_uncertainty(graph, uncertainty):
            return False
    return True


def check_uncertainty(graph, uncertainty):
    for value in graph[uncertainty]:        #run over uncertain values and check if <=0.
        if value <= 0:
            return False
    return True

def is_valid_graph(graph):
    if not check_length(graph):
        print("Data lists are not the same length")
        return False
    if not check_uncertainties(graph):
        print("Not all uncertainties are positive")
        return False
    return True



def is_colums_input(lines):                                    # check if the title is in columns
    clean_header = lines[0].replace(" ", "").replace("\n","")
    return clean_header.isalpha()                                  # return true or false



def numerator_avg_x(graph):
    for key in graph:
        if key == 'x':          # find the x values
            i = 0
            sum_ = 0
            while i < len(graph[key]):
                sum_ += graph[key][i]/(_dy(graph)[i])**2
                i+=1
            return sum_

def _dy(graph):
    for key in graph:
        if key == 'dy':
            return graph[key]

def numerator_avg_y(graph):
    for key in graph:
        if key == 'y':
            i = 0
            sum_ = 0
            while i < len(graph[key]):
                sum_ += graph[key][i]/_dy(graph)[i]**2
                i+=1
            return sum_

def numerator_avg_xy(graph):
    i = 0
    sum = 0
    while i < (len(graph['x'])):
        xi_yi = graph['x'][i]*graph['y'][i]
        numerator = xi_yi/_dy(graph)[i]**2
        sum += numerator
        i += 1
    return sum

def denominator_z(graph):
    for key in graph:
        sum_dy2 = 0
        if key == 'dy':
            i = 0
            while i <len(graph[key]):
                sum_dy2 += 1/graph[key][i]**2
                i += 1
            return sum_dy2

def numerator_x_square_avg(graph):
    for key in graph:
        if key == 'x':          #find the x values
            i = 0
            sum_ = 0
            while i < len(graph[key]):
                sum_ +=(graph[key][i])**2/_dy(graph)[i]**2
                i+=1
            return sum_

def cal_a(graph):
    xy_avg = numerator_avg_xy(graph)/denominator_z(graph)
    x_avg = numerator_avg_x(graph)/denominator_z(graph)
    y_avg = numerator_avg_y(graph)/denominator_z(graph)
    x_square_avg = numerator_x_square_avg(graph)/denominator_z(graph)
    x_avg_square = (numerator_avg_x(graph)/denominator_z(graph))**2
    numerator_a = xy_avg - x_avg*y_avg
    denominator_a = x_square_avg - x_avg_square
    a = numerator_a/denominator_a
    return a

def cal_dy_square_avg(graph):
    for key in graph:
        if key == 'dy':
            i = 0
            sum_numerator = 0
            while i < len(graph[key]):
                numerator_dy2_avg = graph[key][i]**2 / graph['dy'][i]**2
                sum_numerator += numerator_dy2_avg
                dy_square_avg = sum_numerator/denominator_z(graph)
                i += 1
            return dy_square_avg

def cal_da_square(graph):
    N = len(graph['x'])            # just checking the length..
    x_square_avg = numerator_x_square_avg(graph)/denominator_z(graph)  #(X^2)avg
    x_avg_square = (numerator_avg_x(graph)/denominator_z(graph))**2    #(X_avg)^2
    da_square = cal_dy_square_avg(graph)/(N*(x_square_avg - x_avg_square))
    return da_square

def cal_b(graph):
    y_avg = numerator_avg_y(graph)/denominator_z(graph)
    x_avg = numerator_avg_x(graph)/ denominator_z(graph)
    b = y_avg - cal_a(graph)*x_avg
    return b

def db_square(graph):
    db_square = cal_da_square(graph)*numerator_x_square_avg(graph)/denominator_z(graph) # Take da^2 and multiply it with (x^2)avg
    return db_square

def cal_chi_square(graph):
    i = 0
    N = len(graph['x'])
    chi_square = 0
    while i < N:
        numerator = (graph['y'][i] - (cal_a(graph)*graph['x'][i] + cal_b(graph)))
        chi = (numerator/graph['dy'][i])**2
        chi_square += chi
        i += 1
    return chi_square

def chi_2_red(graph):
    N = len(graph['x'])
    chi_2red = cal_chi_square(graph)/(N - 2)
    return chi_2red

def main():
    graph=create_graph(r"C:\Users\guy\Desktop\קורס מחשבים\inputOutputExamples\inputOutputExamples\workingcols\input.txt")
    if graph is None:
        return graph

    a = cal_a(graph)
    da  = cal_da_square(graph)**0.5
    b = cal_b(graph)
    db = db_square(graph)**0.5
    print("avg_x" + " " + str(numerator_avg_x(graph)/denominator_z(graph)))
    print("avg_y" + " " + str(numerator_avg_y(graph)/denominator_z(graph)))
    print("da_square" + " " + str(cal_da_square(graph)))

    print("a = " + "" + str(a) + " +- " + str(da))
    print("b = " + "" + str(b) + " +- " + str(db))
    print("chi2 = " + "" + str(cal_chi_square(graph)))
    print("chi2_reduced = " + "" + str(chi_2_red(graph)))

    xerr = np.array(graph['dx'])
    yerr = np.array(graph['dy'])
    x = np.array(graph['x'])
    y = a * x + b
    pyplot.plot(x, y, 'r')
    pyplot.errorbar(x, np.array(graph['y']), yerr=yerr, xerr=xerr, fmt='none', ecolor='b')
    pyplot.ylabel('some label')
    pyplot.show()
    pyplot.savefig("linear_fit.svg")
if __name__ == '__main__':
    main()


# def cal_db(graph)  #calculate dX2/db

# def fun_db(x, dy):  # b פונקציה שמחשבת את השגיאה של
#    dy_power_avg = 0
#    s_dy = 0
#    N = 0
#    for i in range(0, len(dy)):
#        dy_power_avg = dy_power_avg + ((dy[i] ** 2) / dy[i] ** 2)
#        s_dy = s_dy + (1 / (dy[i] ** 2))
#        N = N + 1
#    dy_power_avg = dy_power_avg / (s_dy)
#    x_avarage = 0
#    power_x_avarage = 0
#      for i in range(0, len(x)):
#        x_avarage = x_avarage + (x[i] / (dy[i] ** 2))
#        power_x_avarage = power_x_avarage + (x[i] ** 2 / (dy[i] ** 2))
#    x_avarage = x_avarage / (s_dy)
#    power_x_avarage = power_x_avarage / (s_dy)

#        return np.sqrt((dy_power_avg) * (power_x_avarage) / (N * (power_x_avarage - (x_avarage ** 2))))
# transpose
