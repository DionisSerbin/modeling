import math
import pandas as pd

class StatFunc:
    def count_column(self, column):
        return len(column)

    def mean_column(self, column):
        return sum(column) / len(column)

    def median(self, column):
        sorted_data = sorted(column)
        data_len = len(sorted_data)
        middle = (data_len - 1) // 2
        if middle % 2:
            return sorted_data[middle]
        else:
            return (sorted_data[middle] + sorted_data[middle + 1]) / 2.0

    def var_column(self, column):
        mean = self.mean_column(column)
        return sum(pow(x-mean,2) for x in column) / len(column)

    def std_column(self, column):
        return math.sqrt(self.var_column(column))

    def max_column(self, column):
        return max(column)

    def min_value(self, column):
        return min(column)

    def quntile(self, column, q):
        data_sorted = sorted(column)

        index = math.ceil(q / 100 * len(data_sorted))

        return data_sorted[index]

    def iqr(self, column):
        return self.quntile(column, 75) - self.quntile(column, 25)

    def print(self, f, column):
        print(f"{f.__name__}: {f(column)}")

    def print_quant(self, f, column, percent):
        print(f"{f.__name__}({percent}): {f(column, percent)}")

    def remove_from_column(self, df, column):
        q1 = self.quntile(column, 25)
        q3 = self.quntile(column, 75)
        iqr = self.iqr(column)
        ret = df[~((df[column] < (q1 - 1.5 * iqr)) | (df[column] > (q3 + 1.5 * iqr)))]
        return df[~((df[column] < (q1 - 1.5 * iqr)) | (df[column] > (q3 + 1.5 * iqr)))]

    def remove_rubbish(self, df):
        for column in df.columns:
            if column != 'id':
                col = df[column]
                df = self.remove_from_column(df, col)
        return df

    def drop_dublicate(self, df):
        # set_df = set()
        # for index, row in df.iterrows():
        #     set_df.add(row.values)
        return df.drop_duplicates()

    def dropna(self, df):
        # for index, row in df.iterrows():
        #     if row.contain(None):
        #         df = df.drop(rows=[row])
        return df.dropna()

    def describe(self, df):
        for column in df.columns:
            if column != 'id':
                col = df[column]
                print("_"*10)
                print(column)
                self.print(self.count_column, col)
                self.print(self.mean_column, col)
                self.print(self.median, col)
                self.print(self.var_column, col)
                self.print(self.std_column, col)
                self.print(self.min_value, col)
                self.print(self.max_column, col)
                self.print_quant(self.quntile, col, 25)
                self.print_quant(self.quntile, col, 50)
                self.print_quant(self.quntile, col, 75)
                self.print(self.iqr, col)

pd.set_option('display.max_columns', None, 'display.width', -1)
df = pd.read_csv("place1.csv")
df = df.drop(columns=['Unnamed: 5'])

statFunc = StatFunc()

df = statFunc.remove_rubbish(df)