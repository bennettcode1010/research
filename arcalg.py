from newcorridordata import start,end

def make_square_hex_arcs(k):
    arc_list = []
    for j in range(0, k-1):
        if j % 2 == 0:
            for i in range(1+j*k,k+1+j*k):
                arc_list.append((i,i+k))
                if i != k+j*k:
                    arc_list.append((i,i+1))
                if i != k*j+1:
                    arc_list.append((i,i+k-1))
        else:
            for i in range(1+j*k,k+1+j*k):
                arc_list.append((i,i+k))
                if i != k+j*k:
                    arc_list.append((i,i+1))
                    arc_list.append((i,i+k+1))
                    
    for i in range((k-1)*k+1,k**2):
        arc_list.append((i,i+1))
    if j not in end:    
        reversed_arcs = [(j, i) for (i, j) in arc_list]
    arc_list.extend(reversed_arcs)
    for j in start:
        arc_list.append((0, j))

    return arc_list


arcs = make_square_hex_arcs(8)
print(arcs)

            
    
