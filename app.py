from archus import Archus
from archus.response import Response
from concurrent.futures import ThreadPoolExecutor
import time
from archus.status import HTTPStatus
from archus.middleware import LoggingMiddleware, SecurityHeadersMiddleware,CORSMiddleware,ThrottleMiddleWare
from archus.exceptions import ArchusException
from archus.file_handlers import FileHandler

app = Archus()
app.add_middleware(ThrottleMiddleWare)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)

@app.route('/', ['POST'])
def index(request):
    f=FileHandler(request)
    files=f.get_files()
    # print(files)
    f.write_file(file=files[1])
    # with open('a.jpg','wb') as f:
    #     f.write(file)
    data={
        "message":"hello"
    }
    return Response(HTTPStatus.CREATED, 
                    data,content_type="application/json"
                    )


@app.route('/test', ['GET'])
def test(request):
    data={
        "message":"hello"
    }
    # raise ArchusException(message="user not exists!",status=HTTPStatus.NOT_FOUND)
    return Response(HTTPStatus.OK, data,content_type="application/json")

@app.route('/home', ['GET','POST'])
def home_handler(request):
    if request.method=='GET':
        context = {
            'title': 'Home Page',
            'heading': 'Welcome to my Framework!',
            'items': ['Item 1', 'Item 2', 'Item 3']
        }
        return {'template': 'index.html', 'context': context}
    elif request.method=='POST':
        name = request.form.get('name', 'Default Name')
        context = {
        'title': 'Home Page',
        'heading': 'Welcome to my Framework!',
        'items': ['Item 1', 'Item 2', 'Item 3'],
        'name':name
        }
        return {'template': 'index.html', 'context': context}

@app.route('/about', ['GET'])
def about(request):
    return {'template': 'about.html'}

@app.route('/submit', ['POST'])
def submit_handler(request):
    return app.redirect('/about')

@app.route(r'/products/<product>/<user>', ['GET'])
def get_product(request,product,user):
    # http://127.0.0.1:8000/products/123/utsav?product=yy7yy
    product_id = request.query_params.get('product')
    if product_id:
        product_id=product_id[0]
    # product = request.path_params.get('product')
    print(product)

    # user = request.path_params.get('user')
    print(user)
    data={
        "prodcut":product_id
    }
    return Response(HTTPStatus.OK, data)

if __name__ == '__main__':
   app.run()

