# Интернет магазин

### Структура проекта:
+ 1. Главная страница
    * 1.1. Список категорий товаров
    * 1.2. Топ товаров по каждой категории из списка
    * 1.3. Добавление товаров к избранное. Если пользователь не авторизован, то уведомление о необходимости авторизации.
    * 1.4. Прелоадер страницы
2. Каталог товаров
    * 2.1. Список товаров
    * 2.2. Прогрузка товаров при промотке страницы
    * 2.3. Фильтрация товаров
    * 2.4. Сортировка товаров
    * 2.5. Список выбранных фильтров
    * 2.6. Возможность удалять выбранные фильтры
    * 2.7. Прелоадер страницы
3. Избранное
    * 3.1. Доступ только авторизованным пользователям, иначе загружает пустую страницу
    * 3.3. Список избранных товаров пользователя
    * 3.4. Изменение списка избранного в рил тайм
    * 3.5. Прелоадер страницы
    * 3.6. При изменении списка избранного соответствующе изменять товары в корзине и наоборот.
4. Поиск
    * При вводе в поисковик должны появляться подсказки из БД с названиями товаров, брендов.
5. Аккаунт
    * 5.1. Список заказов пользователя.
    * 5.2. Прелоадер страницы.
6. Регистрация
    * 6.1. Ввод имени, фамилии, телефона, почты и пароля.
    * 6.2. Отправка письма на почту для подтверждения регистрации.
    * 6.3. После нажатия на кнопку отправки данных появляется лоадер и запрещается доступ к кнопке.
    * 6.4. Валидация всех полей с помощью JS перед отправкой на сервер. В случае неверно введенных данных доступ к кнопке закрыт.
7. Логин
    * 7.1. Ввод почты и пароля.
    * 7.2. В случае введения неверных данных, отображается сообщение о некорректности введенных данных.
    * 7.3. После нажатия на кнопку отправки данных появляется лоадер и запрещается доступ к кнопке.
8. Изменение пароля
9. Сброс пароля
    * 9.1. Отправка письма на почту.
10. Оформление заказа
    * 10.1. Сохранение последнего введенного адреса пользователя, если он авторизован.
    * 10.2. Выбор способа доставки заказа.
    * 10.3. При неверном оформлении заказа всплывающее уведомление.
11. Детали заказа
    * 11.1. Доступно всем по ссылке, поэтому не должно быть Конфиденциальных данных.
12. Админ панель
    * 12.1. Список товаров.
    * 12.1.1. Добавление товаров.
    * 12.1.2. Изменение товаров.
    * 12.2. Список пользователей.
13. Другое
    * 13.1. Всплывающие уведомления.
    * 13.2. Кастомное письмо при регистрации.
14. Корзина
    * 14.1. Список товаров пользователя
    * 14.2. Изменение содержимого корзины в рил тайм: добавление, изменение, удаление.
    * 14.3. Изменение состояния избранности товара в корзине в рил тайм.
    * 14.4. Если коризна пустая, то кнопка на страницу каталога.
    * 14.5. Если корзина не пустая, то есть кнопка оформить заказ.
15. Настройки
    * 15.1. Включает возможность изменения ПД и обновление пароля.
