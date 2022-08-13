from flask import Flask, jsonify,abort, request
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gmnxvjqerskryb:8de2d4546d118d08906b33e23505bc0bea221ef9bb4ba6175b56cef0ca4f927a@ec2-44-208-88-195.compute-1.amazonaws.com:5432/d4fip5q3587fbf'
# app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)


class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False) 
    author=db.Column(db.String(100),nullable=False)  
    stock=db.Column(db.Integer,nullable=False)
    shippable=db.Column(db.Boolean, default=True)
    rate=db.Column(db.Float,nullable=True)

    def __repr__(self):
        return self.title

    
    def as_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "author":self.author,
            "stock":self.stock,
            "shippable":self.shippable,
            "rate":self.rate,
        }
   


# Read : GET
   
@app.get("/books")
def book_list(): 
    query=Book.query.all() 
    books=[]

    for book in query:
        books.append(book.as_dict())

    return jsonify(books)



@app.get("/top-books")
def top_books():
    query=Book.query.filter(Book.rate>=4) 
    books=[]

    for book in query:
        books.append(book.as_dict())

    return jsonify(books)



@app.get("/books/<int:id>")
def book_detail(id):
    query=Book.query.get(id)

    if query:
         return jsonify(query.as_dict())
   
    return abort(404,description="there is no book with that id")


# Create : POST

@app.post("/books")
def add_books():
    book=Book(
        title=request.json["title"],
        author=request.json["author"],
        stock=request.json["stock"],
        shippable=request.json["shippable"],
        rate=request.json["rate"],
    
    )

    db.session.add(book)
    db.session.commit()

    query=Book.query.all() 
    books=[]

    for book in query:
        books.append(book.as_dict())


    return jsonify(books),201




# Update : PUT

@app.put("/books/<int:id>")
def update_book(id):
    book=Book.query.get(id)

    if book:
        book.title=request.json["title"]
        book.author=request.json["author"]
        book.stock=request.json["stock"]
        book.shippable=request.json["shippable"]
        book.rate=request.json["rate"]
        db.session.commit()


        return jsonify(book.as_dict())

    return abort(404,description="there is no book with that id")


# Delete : DELETE

@app.delete("/books/<int:id>")
def delete_book(id):
    book=Book.query.get(id)

    if book:
        db.session.delete(book)
        db.session.commit()
        return "",204

    return abort(404,description="there is no book with that id")


