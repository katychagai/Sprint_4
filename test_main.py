import pytest

from main import BooksCollector

class TestBooksCollector:

    # 1. Параметризованные тесты для add_new_book - проверка добалвения книг с разными тестовыми данными (в т.ч. граничные значения)
    @pytest.mark.parametrize(
        'name, to_be_added',
        [
            ('Гарри Поттер', True),  
            ('Очень длинное название книги, которое превышает 40 символов', False),  
            ('', False),  
            ('    ', True),   
            ('Книга с названием ровно 40 символов-----', True),  
            ('Книга с названием 41 символ--------------', False)
        ]
    )

    def test_add_new_book_name_validation(self, collector, name, to_be_added):
        collector.add_new_book(name)

        assert (name in collector.books_genre) == to_be_added
    
    # 2. Проверка, что у добавленной книги нет жанра 
    def test_newly_added_book_has_no_genre(self, collector):
    
        collector.test_books = 'Гарри Поттер'
    
        for book_name in collector.test_books:
            collector.add_new_book(book_name)
            
            assert collector.get_book_genre(book_name) == ''

    # 3. Параметризованные тесты для set_book_genre - проверка установки жанра для книги (валидные, не валидные жанры)
    @pytest.mark.parametrize(
        'genre, expected_result',
        [
            ('Фантастика', 'Фантастика'),
            ('Ужасы', 'Ужасы'),
            ('', ''),
            (None, ''),
            ('История', ''),
            ('ФАНТАСТИКА', '')
        ]
    )

    def test_set_book_genre(self, collector, genre, expected_result):
        
        # Добавление новой книги
        book_name = 'Анна Коренина'
        collector.add_new_book(book_name)  
        
        # Установка жанра для новой книги
        collector.set_book_genre(book_name, genre)
        
        # Проверка установки жанра для книги
        assert collector.get_book_genre(book_name) == expected_result

    # 4. Проверка, что для несуществующей книги не добавляется жанр, не обновляется словарь с книгами
    def test_set_genre_for_nonexistent_book(self, collector):
        initial_state = dict(collector.books_genre)

        collector.set_book_genre('Герой нашего времени', 'Фантастика')

        assert 'Герой нашего времени' not in collector.books_genre
        assert collector.books_genre == initial_state

    # 5. Параметризованные тесты для get_books_with_specific_genre - проверка фильтрации книг по жанрам (валидные, невалидные случаи)
    @pytest.mark.parametrize(
        'books, genre_to_search, expected_result',
        [
            ([('Тайна девятой планеты', 'Фантастика'), ('Понедельник начинается в субботу', 'Фантастика')], 'Фантастика', ['Тайна девятой планеты', 'Понедельник начинается в субботу']),
            ([('Тайна девятой планеты', 'Фантастика'), ('Оно', 'Ужасы')], 'Фантастика', ['Тайна девятой планеты']),
            ([('Понедельник начинается в субботу', 'Фантастика')], 'Ужасы', []),
            ([], 'Фантастика', []),  
            ([('Оно', '')], 'Фантастика', [])
        ]
    )

    def test_get_books_with_specific_genre(self, collector, books, genre_to_search, expected_result):
        for name, genre in books:
            collector.add_new_book(name)
            if genre:  
                collector.set_book_genre(name, genre)
        
        result = collector.get_books_with_specific_genre(genre_to_search)

        assert sorted(result) == sorted(expected_result)

    # 6. Параметризованные тесты для get_books_for_children - проверка, что в список книг для детей не попалдают книги с возрастным рейтингом
    @pytest.mark.parametrize(
        'books, expected_result',
        [
            ([('Маша и Медведь', 'Мультфильмы'), ('Винни-Пух', 'Комедии')], ['Маша и Медведь', 'Винни-Пух']),
            ([('Оно', 'Ужасы'), ('Твин Пикс', 'Детективы')], []),
            ([('Маша и Медведь', 'Мультфильмы'), ('Оно', 'Ужасы')], ['Маша и Медведь']),
            ([('Без жанра', '')], []),  
            ([], [])
        ]
    )

    def test_get_books_for_children(self, collector, books, expected_result):
        for name, genre in books:
            collector.add_new_book(name)
            if genre:
                collector.set_book_genre(name, genre)
        
        result = collector.get_books_for_children() 

        assert result == expected_result

    # 7. Параметризованные тесты для add_to_favorites - проверка добавления книг в избранное (валидные и не валидные случаи)
    @pytest.mark.parametrize(
        'books_to_add, expected_favorites',
        [
            (['Оно'], ['Оно']),  
            (['Анна Коренина', 'Евгений Онегин'], ['Анна Коренина', 'Евгений Онегин']), 
            (['Оно', 'Оно'], ['Оно']),  
            ([], []), 
            (['Тайна девятой планеты'], []),  
        ]  
    )

    def test_add_to_favorites(self, collector, books_to_add, expected_favorites):
    # Добавляем все существующие книги
        for book in set(books_to_add):
            if book != 'Тайна девятой планеты':  
                collector.add_new_book(book)
    
    # Добавляем книги в избранное
        for book in books_to_add:
            collector.add_book_in_favorites(book)
    
    # Провереряем, что валидные книги добавились в избранное
        result = collector.get_list_of_favorites_books()

        assert result == expected_favorites
    
    # 8. Параметризованные тесты для remove_from_favorites - проверка удаления книг из избранного (валидные и не валидные случаи)
    @pytest.mark.parametrize(
    'in_favorites, books_to_remove, expected_favorites',
    [
        (['Оно', 'Анна Коренина'], ['Оно'], ['Анна Коренина']),  
        (['Оно', 'Анна Коренина'], ['Оно', 'Анна Коренина'], []),  
        (['Оно'], ['Алиса в стране чудес'], ['Оно']),  
        (['Оно'], [], ['Оно']),  
        ([], ['Оно'], [])
    ]
)
    def test_remove_from_favorites(self, collector, in_favorites, books_to_remove, expected_favorites):
        # Добавляем книги и заполняем избранное
        for book in set(in_favorites + books_to_remove):
            if book != 'Алиса в стране чудес':  
                collector.add_new_book(book)
    
        for book in in_favorites:
            collector.add_book_in_favorites(book)
    
        # Удаляем из избранного
        for book in books_to_remove:
            collector.delete_book_from_favorites(book)
    
        # Проверяем, что в списке избранного нет удаленной книги
        result = collector.get_list_of_favorites_books()

        assert result == expected_favorites

    # 9. Проверка вывода жанра несуществующей книги
    def test_get_book_genre_nonexistent_book(self, collector):

        assert collector.get_book_genre('Оно') is None
    