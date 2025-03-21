def serialize_get_books(results):
    books = []
    for i in results:
        d = {}
        d['id'] = i.id
        d['name'] = i.name
        d['content'] = i.content
        d['aurthor_id'] = i.aurthor_id
        books.append(d)
    return books

def serialize_book(resp):
    d = {}
    d['id'] = resp.id
    d['name'] = resp.name
    d['content'] = resp.content
    d['aurthor_id'] = resp.aurthor_id
    return d

def serialize_get_borrowings(resp):
    borrowings = []
    for i in resp:
        d= {}
        d["id"] = i.id
        d["user_id"] = i.user_id
        d["book_id"] = i.book_id
        d["is_returned"] = i.is_returned
        borrowings.append(d)
    return borrowings

def serialize_borrowing(i):
    d= {}
    d["id"] = i.id
    d["user_id"] = i.user_id
    d["book_id"] = i.book_id
    d["is_returned"] = i.is_returned

    return d