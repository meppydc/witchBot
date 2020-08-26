from functools import reduce

def file_to_array(name, keep_new_line):
    file = open(name,"r")
    result = file.readlines()
    file.close()
    print(f"Read array {name}")
    return result if keep_new_line else [line[:-2] for line in result]

def array_to_file(name, a):
    file = open(name,"w")
    file.writelines(a)
    file.close()
    print(f"Wrote array to {name}")


def file_to_dict(name):
    file = open(name,"r")
    lines = file.readlines()
    file.close()
    result = {}
    for line in lines:
        split = line.split(" ")
        result[split[0]] = split[1:]
        print(f"Ready dict {name}")
    return result

def dict_to_file(name, d):
    lines = []
    for key, value in d:
        lines.append(f"{key}{reduce(lambda s,a: s + ' ' + str(a), value, '')}")
    file = open(name,'w')
    file.writelines(lines)
    file.close
    print(f"Wrote dict to {name}")

if __name__ == "__main__":
    #status = file_to_array('status.txt')
    #print(status[-1])
    #status[-1] = "Tax Fraud!"
    #array_to_file("status.txt", status)
    pass