from statistics import LinearRegression

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def define_dataset(df):
    print(df.shape)
    print(df.info())
    print(df.head(40))
    print(df.describe())
    return df['id'].value_counts().head(20)  # определение


# индексов - дубликатов
# Функция
# get_dummies
# # Формируем наборы признаков и вектор целевого признака для всех трех
# локаций, одинакого
# исключая
# из
# списка
# признаков
# # идентификатор (индекс) месторождения - он никак не может влиять на объем
# добытой
# нефти

features_1 = df_1.drop(['id', 'product'], axis=1)
features_ohe_1 = pd.get_dummies(features_1, drop_first=True)
target_1 = df_1['product']

features_2 = df_2.drop(['id', 'product'], axis=1)
features_ohe_2 = pd.get_dummies(features_2, drop_first=True)
target_2 = df_2['product']

features_3 = df_3.drop(['id', 'product'], axis=1)
features_ohe_3 = pd.get_dummies(features_3, drop_first=True)
target_3 = df_3['product']

# Разбиваем данные на обучающую и валидационную выборки в соотношении 75:25.
features_train_1, features_valid_1, target_train_1, target_valid_1 =
train_test_split(features_ohe_1, target_1, test_size=0.25,
                 random_state=12345)
features_train_2, features_valid_2, target_train_2, target_valid_2 =
train_test_split(features_ohe_2, target_2, test_size=0.25,
                 random_state=12345)
features_train_3, features_valid_3, target_train_3, target_valid_3 =
train_test_split(features_ohe_3, target_3, test_size=0.25,
                 random_state=12345)
model = LinearRegression()  # Применяем модель линейной регрессии

# Признаки кодируем во избежание доминирования одного из них
numeric = ['f0', 'f1', 'f2']
scaler = StandardScaler()


def scale(features_train, features_valid, numeric):
    scaler.fit(features_train_1[numeric])
    features_train[numeric] = scaler.transform(features_train[numeric])
    features_valid[numeric] = scaler.transform(features_valid[numeric])
    return


# Обучаем модель и проводим предсказания на первой валидационной выборке.
def study(features_train, features_valid, target_train, target_valid,
          number_location):
    model.fit(features_train, target_train)  # обучите модель на первой


# тренировочной
# выборке
# predictions_valid = model.predict(features_valid)  # получите
# предсказания
# модели
# на
# первой
# валидационной
# выборке
# # Выводим на печать средний запас предсказанного сырья и RMSE модели для
# первой
# локации.
mse = mean_squared_error(target_valid, predictions_valid)

# < извлекаем корень из MSE >
result = mse ** 0.5
print("Средний запас предсказанного на валидационной выборке",
      number_location, "сырья:", predictions_valid.mean(), '(тыс. баррелей)')
print("RMSE модели линейной регрессии на валидационной выборке",
      number_location, ":", result)
return predictions_valid