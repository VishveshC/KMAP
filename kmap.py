def main():
    print("---Karnaugh Map Minimiser---")

    print("Number of variables: ")
    order = int(input().strip())

    print("Minterm Function to be minimised: ")
    fn = list(map(int, input().split(',')))
    
    print("Don't care conditions, press enter if none: ")
    dc_input = input().strip()
    if dc_input:
        dc = list(map(int, dc_input.split(',')))
    else:
        dc = []
    
    num_rows = 2 ** (order // 2)
    num_cols = 2 ** (order - (order // 2))

    kmap = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    print(f"Created a {num_rows}x{num_cols} grid for order {order}.")

    for i in fn:
        r, c = return_coordinates(i, order)
        kmap[r][c] = 1
    for i in dc:
        r, c = return_coordinates(i, order)
        kmap[r][c] = 2      # 2 is X
    
    print("The K-map is: ")
    
    for row in kmap:
        print(row)

    shapes = get_shapes(num_rows, num_cols)

    groups = []

    for h, w in shapes:
        for r in range(num_rows):
            for c in range(num_cols):
                is_valid, cells = check_group(kmap, r, c, h, w)
                
                if is_valid:
                    cell_values = [kmap[x][y] for x, y in cells]
                    if 1 not in cell_values:
                        continue # All Don't Cares, skip

                    current_set = set(cells)
                    
                    is_redundant = False
                    for i in groups:
                        # check if current_set is a SUBSET of existing_group (i) of groups
                        if current_set.issubset(i):
                            is_redundant = True
                            break
                    
                    if not is_redundant:
                        groups.append(current_set)
    
    unique_groups = []
    seen = set()
    for g in groups:
        f_group = tuple(sorted(list(g)))
        if f_group not in seen:
            seen.add(f_group)
            unique_groups.append(g)

    answer = []
    
    for group in groups:
        term = solve_group(group, order)
        answer.append(term)

    final_equation = " + ".join(answer)
    
    print(f"Final Equation: F = {final_equation}")



def solve_group(group_cells, order):
    if order == 2:  # 2x2 Grid
        row_vars, col_vars = ['A'], ['B']
        row_headers = ["0", "1"]
        col_headers = ["0", "1"]
        
    elif order == 3: # 2x4 Grid
        row_vars, col_vars = ['A'], ['B', 'C']
        row_headers = ["0", "1"]
        col_headers = ["00", "01", "11", "10"]
        
    elif order == 4: # 4x4 Grid
        row_vars, col_vars = ['A', 'B'], ['C', 'D']
        row_headers = ["00", "01", "11", "10"]
        col_headers = ["00", "01", "11", "10"]

    unique_rows = set(r for r, c in group_cells)
    unique_cols = set(c for r, c in group_cells)

    final_string = ""
    
    if len(unique_rows) < len(row_headers):
        current_headers = [row_headers[r] for r in unique_rows]
        final_string += compare_bits(current_headers, row_vars)

    if len(unique_cols) < len(col_headers):
        current_headers = [col_headers[c] for c in unique_cols]
        final_string += compare_bits(current_headers, col_vars)
        
    if final_string == "": return "1"
    return final_string



def compare_bits(headers, var_names):
    res = ""
    num_bits = len(headers[0]) 
    
    for i in range(num_bits):
        first_bit = headers[0][i]
        
        is_constant = True
        for h in headers:
            if h[i] != first_bit:
                is_constant = False
                break
        
        if is_constant:
            letter = var_names[i]
            if first_bit == '0':
                res += letter + "'" # 0 - (A')
            else:
                res += letter       # 1 - (A)
    return res



def get_shapes(num_rows, num_cols):
    shapes = []
    powers = [1, 2, 4] 
    
    for h in powers:
        for w in powers:
            if h <= num_rows and w <= num_cols:
                shapes.append((h, w))
    
    shapes.sort(key=lambda x: x[0] * x[1], reverse=True)
    
    return shapes



def check_group(kmap, start_row, start_col, height, width):
    num_rows = len(kmap)
    num_cols = len(kmap[0])
    covered_cells = []
    
    for i in range(height):
        for j in range(width):
            r = (start_row + i) % num_rows
            c = (start_col + j) % num_cols
            
            if kmap[r][c] == 0:
                return False, []
            
            covered_cells.append((r, c))
            
    return True, covered_cells



def return_coordinates(n, order=None):
    coords_small = [[0,0], [0,1], [1,0], [1,1]]
    coords_big = [[0,0], [0,1], [0,3], [0,2],
              [1,0], [1,1], [1,3], [1,2],
              [3,0], [3,1], [3,3], [3,2],
              [2,0], [2,1], [2,3], [2,2]]
    
    return coords_small[n] if order == 2 else coords_big[n]



if __name__ == "__main__":
    main()