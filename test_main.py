import pytest

from main import BooksCollector

class TestBooksCollector:

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

    def test_set_book_genre_for_add_book(self, collector, genre, expected_result):
        
        book_name = 'Анна Коренина'
        collector.add_new_book(book_name)  
        
        collector.set_book_genre(book_name, genre)
        
        assert collector.get_book_genre(book_name) == expected_result 

    def test_set_book_genre_for_nonexistent_book(self, collector):

        collector.set_book_genre('Герой нашего времени', 'Фантастика')
        result = collector.get_book_genre('Герой нашего времени')

        assert result is None

    def test_get_book_genre_for_add_book(self, collector):
        book_name = 'Тайна девятой планеты'
        expected_genre = 'Фантастика'

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, expected_genre)

        actual_genre = collector.get_book_genre(book_name)

        assert actual_genre == expected_genre

    def test_get_book_genre_new_book_has_no_genre(self, collector):
        book_name = 'Гарри Поттер'

        collector.add_new_book(book_name)

        assert collector.get_book_genre(book_name) == ''

    def test_get_book_genre_nonexistent_book(self, collector):

        assert collector.get_book_genre('Оно') is None
 
    @pytest.mark.parametrize(
        'books, genre_to_search, expected_result',
        [
            ([('Тайна девятой планеты', 'Фантастика'), ('Понедельник начинается в субботу', 'Фантастика')], 'Фантастика', ['Тайна девятой планеты', 'Понедельник начинается в субботу']),
            ([('Тайна девятой планеты', 'Фантастика'), ('Оно', 'Ужасы')], 'Фантастика', ['Тайна девятой планеты'])
        ]
    )

    def test_get_books_with_specific_genre_for_add_books(self, collector, books, genre_to_search, expected_result):
        for name, genre in books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        
        result = collector.get_books_with_specific_genre(genre_to_search)

        assert result == expected_result
 
    def test_get_books_with_specific_genre_for_book_without_genre(self, collector):
        book_name = 'Гарри Поттер'

        collector.add_new_book(book_name)

        assert collector.get_books_with_specific_genre(book_name) == []

    @pytest.mark.parametrize(
        'books_data, expected_output',
        [
            ([], {}),
            ([('Гарри Поттер', '')], {'Гарри Поттер': ''}),
            ([('Тайна девятой планеты', 'Фантастика')], {'Тайна девятой планеты': 'Фантастика'}),
            (
                [('Тайна девятой планеты', 'Фантастика'), ('Шерлок Холмс', 'Детектив'), ('Маша и медведь', '')],
                {'Тайна девятой планеты': 'Фантастика', 'Шерлок Холмс': 'Детектив', 'Маша и медведь': ''}
            )
        ]
    )
    def test_get_books_genre_actual_dict_books_genre(self, collector, books_data, expected_output):
        for name, genre in books_data:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        result = collector.get_books_genre()
        assert sorted(result) == sorted(expected_output)

    @pytest.mark.parametrize(
        'books, expected_result',
        [
            ([('Маша и Медведь', 'Мультфильмы'), ('Винни-Пух', 'Комедии')], ['Маша и Медведь', 'Винни-Пух']),
            ([('Оно', 'Ужасы'), ('Твин Пикс', 'Детективы')], []),
            ([('Маша и Медведь', 'Мультфильмы'), ('Оно', 'Ужасы')], ['Маша и Медведь'])
        ]
    )

    def test_get_books_for_children_only_books_for_children(self, collector, books, expected_result):
        for name, genre in books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        
        result = collector.get_books_for_children() 

        assert result == expected_result

    @pytest.mark.parametrize(
        'books_to_add, expected_favorites',
        [
            (['Оно'], ['Оно']),  
            (['Анна Коренина', 'Евгений Онегин'], ['Анна Коренина', 'Евгений Онегин']), 
            (['Оно', 'Оно'], ['Оно']),  
            ([], [])
        ]  
    )

    def test_add_book_in_favorites_add_book_in_list(self, collector, books_to_add, expected_favorites):
        for book in set(books_to_add):  
            collector.add_new_book(book)
    
        for book in books_to_add:
            collector.add_book_in_favorites(book)
  
        result = collector.get_list_of_favorites_books()

        assert result == expected_favorites
 
    @pytest.mark.parametrize(
    'in_favorites, books_to_remove, expected_favorites',
    [
        (['Оно', 'Анна Коренина'], ['Оно'], ['Анна Коренина']),  
        (['Оно', 'Анна Коренина'], ['Оно', 'Анна Коренина'], []),
        (['Оно'], [], ['Оно']),  
        ([], ['Оно'], [])
    ]
)
    def test_delete_book_from_favorites_to_remove_from_list_success(self, collector, in_favorites, books_to_remove, expected_favorites):
        for book in in_favorites: 
            collector.add_new_book(book)
    
        for book in in_favorites:
            collector.add_book_in_favorites(book)
    
        for book in books_to_remove:
            collector.delete_book_from_favorites(book)

        result = collector.get_list_of_favorites_books()

        assert result == expected_favorites

    @pytest.mark.parametrize(
        'initial_books, favorites_to_add, expected_result',
        [
            (['Гарри Поттер', 'Анна Коренина'], [], []),
            (['Гарри Поттер', 'Анна Коренина'], ['Анна Коренина'], ['Анна Коренина']),
            (
                ['Гарри Поттер', 'Анна Коренина', 'Маша и Медведь', 'Шерлок Холмс'], 
                ['Гарри Поттер', 'Маша и Медведь'], 
                ['Гарри Поттер', 'Маша и Медведь']
            ),
            (
                ['Гарри Поттер', 'Маша и Медведь'], 
                ['Гарри Поттер', 'Маша и Медведь'], 
                ['Гарри Поттер', 'Маша и Медведь']
            )
        ]
    )

    def test_get_list_of_favorites_books_actual_favorites_list(self, collector, initial_books, favorites_to_add, expected_result):
        for book in initial_books:
            collector.add_new_book(book)

        for book in favorites_to_add:
            collector.add_book_in_favorites(book)

        result = collector.get_list_of_favorites_books()
        
        assert sorted(result) == sorted(expected_result)