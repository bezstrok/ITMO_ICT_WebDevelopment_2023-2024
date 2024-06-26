# Описание компонента обзора торгов (`Tradesvue`)

## Основные элементы интерфейса

### Таблица торговых операций

- **`v-data-table`**: Динамически отображает список торговых операций с использованием предоставленных данных. Каждая
  строка таблицы содержит информацию о конкретной торговой операции, такую как ID, время начала и окончания, статус,
  общая сумма, брокер, продукт и количество.

### Цветовое кодирование статусов

- **`v-chip`**: Используется для отображения статуса торговой операции, где цвет чипа указывает на текущий статус (
  открыто, закрыто и т.д.).

## Логика и методы

- **Загрузка данных о торгах**: При создании компонента выполняется асинхронный запрос к API для получения списка всех
  торговых операций.

- **Навигация к деталям торгов**: Предоставляется возможность перехода к детальной странице торговой операции при клике
  на соответствующую строку таблицы.

- **Определение цвета статуса**: Метод `statusColor` возвращает соответствующий цвет для разных статусов торговой
  операции, улучшая визуальное восприятие таблицы.

## Взаимодействие с API

- Компонент делает запрос к серверу для получения актуального списка торговых операций, что позволяет пользователям
  всегда иметь доступ к последней информации.