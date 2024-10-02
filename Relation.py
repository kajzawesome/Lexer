from Header import Header
from Row import Row


class Relation:
    def __init__(self, name: str, header: Header, rows = None) -> None:
        self.name = name
        self.header = header
        self.rows = set() if rows is None else rows
    
    def __str__(self) -> str:
        output_str = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue
            sep = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += f"{self.header.values[i]}={row.values[i]}"
                sep = ", "
            output_str += "\n"
        return output_str
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError("Row was not the same length as Header")
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':
        if colIndex < 0 or colIndex >= len(self.header.values):
            raise ValueError("Column index does not fit header")
        new_name = f"{self.name}"
        new_rows = set(row for row in self.rows if row.values[colIndex] == value)
        return Relation(new_name, self.header, new_rows)
    
    def select2(self, index1: int, index2: int) -> 'Relation':
        if index1 < 0 or index1 >= len(self.header.values) or index2 < 0 or index2 >= len(self.header.values):
            raise ValueError("Indexes not found in header")
        new_name = f"{self.name}"
        new_rows = set(row for row in self.rows if row.values[index1] == row.values[index2])
        return Relation(new_name, self.header, new_rows)
    
    def rename(self, new_header: Header) -> 'Relation':
        new_name = f"{self.name}"
        return Relation(new_name, new_header, self.rows)
    
    def project(self, row_indexes: list[int]) -> 'Relation':
        for col_index in row_indexes:
            if col_index < 0 or col_index >= len(self.header.values):
                raise ValueError(f"Column index {col_index} is out of bounds")
        
        new_name = f"{self.name}"
        new_header = Header([self.header.values[i] for i in row_indexes])
        tuples = set(Row([row.values[i] for i in row_indexes]) for row in self.rows)
        return Relation(new_name, new_header, tuples)
    
    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x,y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
            
        return True
        
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        new_row_values: list[str] = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])
        new_row_values.extend(row2.values)
        return Row(new_row_values)
        
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        new_header_values: list[str] = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])
        new_header_values.extend(header2.values)
        return Row(new_header_values)
    
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        for x in range(len(r1.header.values)):
            is_unique: bool = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)
                    
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)

        result: Relation = Relation(r1.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1,t2, overlap):
                    result_row = self.join_rows(t1,t2, unique_cols_1)
                    result.add_row(result_row)

        return result