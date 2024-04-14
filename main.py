import dcel.dcel as dcel

if __name__ == '__main__':
    
    file_path = input("Enter file path: ")

    dcel = dcel.DCEL()

    with open(file_path, 'r') as sites_file:
        for line in sites_file:
            line = line.replace('(', '').replace(')', '').replace(',', '').split()
            
            for i in range(0, len(line), 2):
                x, y = map(int, line[i:i+2])
                dcel.add_vertex(x, y)
    
    for vertex in dcel.vertices_list:
        print("({}, {})".format(vertex.x, vertex.y))
    

