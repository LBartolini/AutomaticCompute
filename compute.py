

class Formula(object):
    def __init__(self, formula):
        self.formula = formula
        self.res = self.compute(self.formula, 0)

    def result(self):
        return self.res

    def computeAtomicOp(self, operation):
        splitted = []
        for op in ['*', '/', '+', '-']:
            temp = operation.split(op)
            if len(temp) == 2:
                temp.append(op)
                splitted = temp

        if len(splitted) >= 2:
            if splitted[2] == '+':
                return str(float(splitted[0]) + float(splitted[1]))
            elif splitted[2] == '-':
                return str(float(splitted[0]) - float(splitted[1]))
            elif splitted[2] == '*':
                return str(float(splitted[0]) * float(splitted[1]))
            elif splitted[2] == '/':
                if float(splitted[1]) == 0:
                    return str(1e1000)
                return str(float(splitted[0]) / float(splitted[1]))
        else:
            return str(operation)

    def separeBrackets(self, formula):
        temp = ""
        operations = []
        inOp = 0

        for char in formula:
            if char == "(":
                if inOp > 0:
                    temp += char
                elif inOp == 0:
                    if temp != "":
                        operations.append(temp)
                        temp = ""
                inOp += 1
            elif char == ")":
                inOp -= 1
                if inOp <= 0:
                    if temp != "":
                        operations.append(temp)
                        temp = ""
                    inOp = 0
                else:
                    temp += char
            else:
                if char in ['*', '/', '+', '-'] and inOp == 0:
                    if temp != "":
                        operations.append(temp)
                        temp = ""
                    operations.append(char)
                else:
                    temp += char
        if temp != "":
            operations.append(temp)

        return operations

    def compute(self, formula, iter):
        operations = self.separeBrackets(formula)

        if len(operations) == 1:
            result = self.computeAtomicOp(operations[0])
            return result

        for i, op in enumerate(operations):
            if ('(' not in op or ')' not in op) and len(op) != 1:
                operations[i] = self.computeAtomicOp(op)

            elif ('(' in op or ')' in op) and len(op) != 1:
                operations[i] = self.compute(op, iter+1)

        for i, op in enumerate(operations):
            if op in ['*', '/', '+', '-']:
                if self.computeAtomicOp(operations[i-1]) == operations[i-1] and self.computeAtomicOp(operations[i+1]) == operations[i+1]:
                    temp = self.computeAtomicOp(operations[i-1]+op+operations[i+1])
                    operations.insert(i-1, temp)
                    for _ in range(3):
                        operations.pop(i)

        if len(operations) == 1:
            result = self.computeAtomicOp(operations[0])
            return result
