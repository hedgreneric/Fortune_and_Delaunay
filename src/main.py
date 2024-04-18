import dcel as dcel

if __name__ == '__main__':
    
    in_file_path = input("Enter input file path: ")
    
    num_sites = 1

    dcel = dcel.DCEL()

    with open(in_file_path, 'r') as sites_file:
        for line in sites_file:
            line = line.replace('(', '').replace(')', '').replace(',', '').split()
            
            for i in range(0, len(line), 2):
                x, y = map(int, line[i:i+2])
                dcel.add_vertex(x, y, num_sites)
                num_sites += 1

        dcel.add_edge(dcel.vertices_list[0], dcel.vertices_list[1])
        dcel.add_edge(dcel.vertices_list[1], dcel.vertices_list[2])
        dcel.add_edge(dcel.vertices_list[2], dcel.vertices_list[3])
        dcel.add_edge(dcel.vertices_list[3], dcel.vertices_list[0])
        dcel.add_edge(dcel.vertices_list[0], dcel.vertices_list[2])

        


    dcel.print_vertices()
    

