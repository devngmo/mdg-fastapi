books = []
for i in range(10):
    books += [{'id': f'book{i}', 'title': f'Book {i}', 'author_id': 'peter_pan', 'author_name': 'Peter Pan'}]
print(f'Script generated {len(books)} books')

global response
response = books