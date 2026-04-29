from datetime import datetime


class Spreadsheet:

    def __init__(self):
        self.entries = []   # list of dicts, one per row
        self.headers = []   # column names in order
        self.filename = None
        self.loaded_at = None

    # ------------------------------------------------------------------ #
    #  Loading / Parsing                                                   #
    # ------------------------------------------------------------------ #

    def loadAndParse(self, filename: str, delimiter: str = ',') -> None:
        """
        Load a delimited text file.
        - First non-empty line is treated as the header row.
        - Remaining lines become row entries (dicts keyed by header).
        - Leading/trailing whitespace is stripped from every value.
        """
        self.filename = filename
        self.entries = []
        self.headers = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found.")

        # Skip blank lines at the top
        non_empty = [l for l in lines if l.strip()]
        if not non_empty:
            raise ValueError("File is empty or contains only blank lines.")

        self.headers = [h.strip() for h in non_empty[0].split(delimiter)]

        for line_num, line in enumerate(non_empty[1:], start=2):
            if not line.strip():
                continue
            values = [v.strip() for v in line.split(delimiter)]

            # Pad or trim to match header count
            if len(values) < len(self.headers):
                values += [''] * (len(self.headers) - len(values))
            elif len(values) > len(self.headers):
                values = values[:len(self.headers)]

            row = dict(zip(self.headers, values))
            row['_line'] = line_num   # keep original line number for debugging
            self.entries.append(row)

        self.loaded_at = datetime.now()
        print(f"Loaded {len(self.entries)} rows and {len(self.headers)} columns from '{filename}'.")

    # ------------------------------------------------------------------ #
    #  Filtering                                                           #
    # ------------------------------------------------------------------ #

    def filter(self, condition: list) -> list:
        """
        Filter entries by a condition expressed as a 3-element list:
            [column, operator, value]

        Supported operators:
            '='   / '=='   exact match (case-insensitive for strings)
            '!='           not equal
            '>'            greater than  (numeric or string comparison)
            '<'            less than
            '>='           greater than or equal
            '<='           less than or equal
            'contains'     substring check (case-insensitive)
            'startswith'   prefix check   (case-insensitive)
            'endswith'     suffix check   (case-insensitive)

        Returns a list of matching row dicts (without the internal '_line' key).
        """
        if len(condition) != 3:
            raise ValueError("Condition must be [column, operator, value].")

        col, op, target = condition
        op = op.strip()

        if col not in self.headers:
            raise KeyError(f"Column '{col}' not found. Available: {self.headers}")

        results = []
        for row in self.entries:
            raw = row.get(col, '')
            if self._matches(raw, op, str(target)):
                clean = {k: v for k, v in row.items() if k != '_line'}
                results.append(clean)

        return results

    def _matches(self, cell_value: str, op: str, target: str) -> bool:
        """Apply a single operator between cell_value and target."""
        cv_lower = cell_value.lower()
        tg_lower = target.lower()

        # Try numeric comparison first
        try:
            cv_num = float(cell_value)
            tg_num = float(target)
            numeric = True
        except ValueError:
            numeric = False

        if op in ('=', '=='):
            return cv_lower == tg_lower
        elif op == '!=':
            return cv_lower != tg_lower
        elif op == '>':
            return (cv_num > tg_num) if numeric else (cv_lower > tg_lower)
        elif op == '<':
            return (cv_num < tg_num) if numeric else (cv_lower < tg_lower)
        elif op == '>=':
            return (cv_num >= tg_num) if numeric else (cv_lower >= tg_lower)
        elif op == '<=':
            return (cv_num <= tg_num) if numeric else (cv_lower <= tg_lower)
        elif op == 'contains':
            return tg_lower in cv_lower
        elif op == 'startswith':
            return cv_lower.startswith(tg_lower)
        elif op == 'endswith':
            return cv_lower.endswith(tg_lower)
        else:
            raise ValueError(f"Unsupported operator: '{op}'")

    def multi_filter(self, conditions: list, match: str = 'all') -> list:
        """
        Filter by multiple conditions.
            match='all'  → every condition must be satisfied (AND)
            match='any'  → at least one condition satisfied   (OR)
        Each condition is a [column, operator, value] list.
        """
        if match not in ('all', 'any'):
            raise ValueError("match must be 'all' or 'any'.")

        results = []
        for row in self.entries:
            hits = [self._matches(row.get(c, ''), op, str(v)) for c, op, v in conditions]
            if (match == 'all' and all(hits)) or (match == 'any' and any(hits)):
                clean = {k: v for k, v in row.items() if k != '_line'}
                results.append(clean)

        return results

    # ------------------------------------------------------------------ #
    #  Sorting                                                             #
    # ------------------------------------------------------------------ #

    def sort(self, column: str, reverse: bool = False) -> list:
        """
        Return entries sorted by the given column.
        Attempts numeric sort; falls back to lexicographic.
        """
        if column not in self.headers:
            raise KeyError(f"Column '{column}' not found.")

        def sort_key(row):
            val = row.get(column, '')
            try:
                return (0, float(val))
            except ValueError:
                return (1, val.lower())

        sorted_rows = sorted(self.entries, key=sort_key, reverse=reverse)
        return [{k: v for k, v in r.items() if k != '_line'} for r in sorted_rows]

    # ------------------------------------------------------------------ #
    #  Column operations                                                   #
    # ------------------------------------------------------------------ #

    def get_column(self, column: str) -> list:
        """Return all values in a column as a list."""
        if column not in self.headers:
            raise KeyError(f"Column '{column}' not found.")
        return [row[column] for row in self.entries]

    def unique_values(self, column: str) -> list:
        """Return sorted unique values in a column."""
        return sorted(set(self.get_column(column)))

    def add_column(self, column: str, default: str = '') -> None:
        """Add a new column to all rows with an optional default value."""
        if column in self.headers:
            raise ValueError(f"Column '{column}' already exists.")
        self.headers.append(column)
        for row in self.entries:
            row[column] = default

    def drop_column(self, column: str) -> None:
        """Remove a column from headers and all rows."""
        if column not in self.headers:
            raise KeyError(f"Column '{column}' not found.")
        self.headers.remove(column)
        for row in self.entries:
            row.pop(column, None)

    def rename_column(self, old_name: str, new_name: str) -> None:
        """Rename a column."""
        if old_name not in self.headers:
            raise KeyError(f"Column '{old_name}' not found.")
        if new_name in self.headers:
            raise ValueError(f"Column '{new_name}' already exists.")
        idx = self.headers.index(old_name)
        self.headers[idx] = new_name
        for row in self.entries:
            row[new_name] = row.pop(old_name)

    # ------------------------------------------------------------------ #
    #  Row operations                                                      #
    # ------------------------------------------------------------------ #

    def add_row(self, values: dict) -> None:
        """
        Append a new row. Pass a dict of {column: value}.
        Missing columns default to ''; unknown columns are ignored.
        """
        row = {h: str(values.get(h, '')) for h in self.headers}
        row['_line'] = None
        self.entries.append(row)

    def delete_row(self, index: int) -> dict:
        """Remove and return the row at the given 0-based index."""
        if index < 0 or index >= len(self.entries):
            raise IndexError(f"Row index {index} out of range (0–{len(self.entries)-1}).")
        removed = self.entries.pop(index)
        return {k: v for k, v in removed.items() if k != '_line'}

    def update_row(self, index: int, updates: dict) -> None:
        """Update specific fields of a row at the given 0-based index."""
        if index < 0 or index >= len(self.entries):
            raise IndexError(f"Row index {index} out of range.")
        for col, val in updates.items():
            if col in self.headers:
                self.entries[index][col] = str(val)

    # ------------------------------------------------------------------ #
    #  Aggregations                                                        #
    # ------------------------------------------------------------------ #

    def numeric_column(self, column: str) -> list:
        """Return numeric (float) values in a column, skipping blanks/non-numbers."""
        values = []
        for v in self.get_column(column):
            try:
                values.append(float(v))
            except ValueError:
                pass
        return values

    def sum(self, column: str) -> float:
        return builtins_sum(self.numeric_column(column))

    def average(self, column: str) -> float:
        nums = self.numeric_column(column)
        if not nums:
            raise ValueError(f"No numeric values in column '{column}'.")
        return builtins_sum(nums) / len(nums)

    def min_value(self, column: str) -> float:
        nums = self.numeric_column(column)
        if not nums:
            raise ValueError(f"No numeric values in column '{column}'.")
        return min(nums)

    def max_value(self, column: str) -> float:
        nums = self.numeric_column(column)
        if not nums:
            raise ValueError(f"No numeric values in column '{column}'.")
        return max(nums)

    def count(self, column: str = None) -> int:
        """Count rows (or non-empty values in a column if specified)."""
        if column is None:
            return len(self.entries)
        return sum(1 for v in self.get_column(column) if v.strip())

    def group_by(self, column: str) -> dict:
        """
        Group rows by a column's value.
        Returns {value: [rows]} dict.
        """
        if column not in self.headers:
            raise KeyError(f"Column '{column}' not found.")
        groups: dict = {}
        for row in self.entries:
            key = row[column]
            clean = {k: v for k, v in row.items() if k != '_line'}
            groups.setdefault(key, []).append(clean)
        return groups

    # ------------------------------------------------------------------ #
    #  Export / Display                                                    #
    # ------------------------------------------------------------------ #

    def to_string(self, rows: list = None, max_col_width: int = 20) -> str:
        """
        Pretty-print the spreadsheet (or a subset of rows) as a table.
        """
        data = rows if rows is not None else [{k: v for k, v in r.items() if k != '_line'} for r in self.entries]
        if not data:
            return "(no data)"

        col_widths = {h: min(max_col_width, max(len(h), max((len(str(r.get(h, ''))) for r in data), default=0)))
                      for h in self.headers}

        def fmt_row(r):
            return ' | '.join(str(r.get(h, '')).ljust(col_widths[h])[:col_widths[h]] for h in self.headers)

        sep = '-+-'.join('-' * col_widths[h] for h in self.headers)
        header_line = fmt_row({h: h for h in self.headers})
        lines = [header_line, sep] + [fmt_row(r) for r in data]
        return '\n'.join(lines)

    def save(self, filename: str = None, delimiter: str = ',') -> None:
        """
        Write the spreadsheet back to a delimited file.
        Defaults to the original filename if none provided.
        """
        target = filename or self.filename
        if not target:
            raise ValueError("No filename specified.")
        with open(target, 'w', encoding='utf-8') as f:
            f.write(delimiter.join(self.headers) + '\n')
            for row in self.entries:
                values = [row.get(h, '') for h in self.headers]
                f.write(delimiter.join(values) + '\n')
        print(f"Saved {len(self.entries)} rows to '{target}'.")

    # ------------------------------------------------------------------ #
    #  Info / Debug                                                        #
    # ------------------------------------------------------------------ #

    def info(self) -> None:
        """Print a summary of the spreadsheet."""
        print(f"File     : {self.filename}")
        print(f"Loaded   : {self.loaded_at.strftime('%Y-%m-%d %H:%M:%S') if self.loaded_at else 'N/A'}")
        print(f"Rows     : {len(self.entries)}")
        print(f"Columns  : {len(self.headers)}")
        print(f"Headers  : {', '.join(self.headers)}")

    def __len__(self) -> int:
        return len(self.entries)

    def __repr__(self) -> str:
        return f"Spreadsheet(rows={len(self.entries)}, columns={self.headers})"


# Alias so our method named `sum` doesn't shadow the built-in
import builtins
builtins_sum = builtins.sum


# ------------------------------------------------------------------ #
#  Sample data file (a.txt)                                           #
# ------------------------------------------------------------------ #

SAMPLE_DATA = """\
name,color,quantity,price,in_stock
Apple,green,120,0.99,yes
Grapes,green,45,2.49,yes
Banana,yellow,80,0.59,yes
Lime,green,30,0.79,yes
Lemon,yellow,60,0.89,no
Blueberry,blue,200,3.99,yes
Watermelon,green,10,5.99,yes
Strawberry,red,150,4.49,yes
Plum,purple,55,1.29,no
Kiwi,green,90,1.09,yes
Orange,orange,100,1.19,yes
Mango,yellow,70,1.99,yes
"""

def create_sample_file(path: str = 'a.txt') -> None:
    with open(path, 'w') as f:
        f.write(SAMPLE_DATA)
    print(f"Created sample file: {path}")


# ------------------------------------------------------------------ #
#  Main / Demo                                                         #
# ------------------------------------------------------------------ #

if __name__ == '__main__':
    # Create the test file
    create_sample_file('a.txt')

    sheet = Spreadsheet()
    sheet.loadAndParse('a.txt')

    print()
    sheet.info()

    print('\n--- Full table ---')
    print(sheet.to_string())

    # Basic filter (from original stub)
    res = sheet.filter(['color', '=', 'green'])
    print(f"\nFinal filtered answer: {res}")

    print('\n--- Green items (pretty) ---')
    print(sheet.to_string(res))

    # More operator demos
    print('\n--- Price > 1.50 ---')
    expensive = sheet.filter(['price', '>', '1.50'])
    print(sheet.to_string(expensive))

    print('\n--- Name contains "an" ---')
    an_items = sheet.filter(['name', 'contains', 'an'])
    print(sheet.to_string(an_items))

    # Multi-filter
    print('\n--- Green AND in_stock=yes (AND) ---')
    green_in_stock = sheet.multi_filter(
        [['color', '=', 'green'], ['in_stock', '=', 'yes']],
        match='all'
    )
    print(sheet.to_string(green_in_stock))

    # Sort
    print('\n--- All items sorted by price (ascending) ---')
    print(sheet.to_string(sheet.sort('price')))

    # Aggregations
    print('\n--- Aggregations on price ---')
    print(f"  Sum     : {sheet.sum('price'):.2f}")
    print(f"  Average : {sheet.average('price'):.2f}")
    print(f"  Min     : {sheet.min_value('price'):.2f}")
    print(f"  Max     : {sheet.max_value('price'):.2f}")
    print(f"  Count   : {sheet.count()}")

    # Group by
    print('\n--- Group by color ---')
    groups = sheet.group_by('color')
    for color, rows in sorted(groups.items()):
        names = ', '.join(r['name'] for r in rows)
        print(f"  {color:10s}: {names}")

    # Unique values
    print(f"\n--- Unique colors: {sheet.unique_values('color')}")

    # Add / update / delete row
    sheet.add_row({'name': 'Pear', 'color': 'green', 'quantity': '40', 'price': '1.39', 'in_stock': 'yes'})
    print(f"\nAfter add_row → row count: {len(sheet)}")

    sheet.update_row(0, {'price': '1.05'})
    print(f"After update_row(0) → Apple price: {sheet.entries[0]['price']}")

    removed = sheet.delete_row(len(sheet) - 1)
    print(f"After delete_row (last) → removed: {removed['name']}, row count: {len(sheet)}")

    # Add / rename / drop column
    sheet.add_column('discount', default='0')
    print(f"\nAfter add_column → headers: {sheet.headers}")

    sheet.rename_column('discount', 'sale_pct')
    print(f"After rename_column → headers: {sheet.headers}")

    sheet.drop_column('sale_pct')
    print(f"After drop_column → headers: {sheet.headers}")

    # Save
    sheet.save('a_modified.txt')
    print("\nDone.")