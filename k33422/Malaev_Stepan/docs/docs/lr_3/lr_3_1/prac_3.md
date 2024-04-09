### Агрегация и Аннотация Запросов в Django

#### 1. **Дата Выдачи Самого Старшего Водительского Удостоверения:**

<br>Находим дату выдачи самого старого водительского удостоверения в базе.
<br>**Листинг кода**

```python
from django.db.models import Min

DriverLicense.objects.aggregate(Min('date_of_issue'))
```

**Результат**
<br>
![img_6.png](img_6.png)

#### 2. **Самая Поздняя Дата Владения Машиной:**

<br>Определяем самую позднюю дату владения машиной среди всех записей.
<br>**Листинг кода**

```python
from django.db.models import Max

Owning.objects.aggregate(Max('end_date'))
```

**Результат**
<br>
![img_7.png](img_7.png)

#### 3. **Количество Машин для Каждого Водителя:**

<br>Подсчитываем количество машин, принадлежащих каждому водителю.
<br>**Листинг кода**

```python
from django.db.models import Count

Driver.objects.annotate(num_cars=Count('cars')).values('username', 'num_cars')
```

**Результат**
<br>
![img_8.png](img_8.png)

#### 4. **Количество Машин Каждой Марки:**

<br>Вычисляем количество машин для каждой марки автомобиля.
<br>**Листинг кода**

```python
Car.objects.values('brand').annotate(total=Count('id_car')).order_by('brand')
```

**Результат**
<br>
![img_9.png](img_9.png)

#### 5. **Сортировка Автовладельцев По Дате Выдачи Удостоверения:**

<br>Сортируем автовладельцев по дате выдачи их первого водительского удостоверения.
<br>**Листинг кода**

```python
Driver.objects.annotate(earliest_license_date=Min('driverlicense__date_of_issue')).order_by(
    'earliest_license_date'
).distinct()
```

**Результат**
<br>
![img_10.png](img_10.png)