import incidence_matrix

def running_example():
    I = incidence_matrix.IncidenceMatrix(["A", "B", "C", "D", "E", "F", "G"])
    I.appendRow("C", ["E", "F"])
    I.appendRow("A", ["D", "G"])
    I.appendRow("B", ["C", "F"])
    I.appendRow("A", ["D"])
    I.appendRow("B", ["G"])
    I.appendRow("D", ["E", "G"])
    return I

def AllowOutsideHole(c):
    if c not in [[3,3],[3,4],[4,3],[4,4]]:
        return True
    else:
        return False

def scott_example():
    names = ["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"]
    for i in range(8):
        for j in range(8):
            if AllowOutsideHole([i,j]):
                names.append(str(i)+str(j))
    return incidence_matrix.IncidenceMatrix(names)

def little_example():
    names = ["L","U","V","Y"]
    for i in range(5):
        for j in range(4):
            names.append(str(i)+str(j))
    return incidence_matrix.IncidenceMatrix(names)

def little_quadratic_example():
    names = ["I","L","U","V","Y"]
    for i in range(5):
        for j in range(5):
            names.append(str(i)+str(j))
    return incidence_matrix.IncidenceMatrix(names)

