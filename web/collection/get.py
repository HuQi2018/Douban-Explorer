from collection import get_music,get_movie,get_book
from django.http import HttpResponse

def main(request):
    id = request.GET.get("id")
    typ = request.GET.get("type")
    if typ == 'movie':
        data = get_movie.get_movie(id)
    elif typ == 'music':
        data = get_music.get_music(id)
    elif typ == 'book':
        data = get_book.get_book(id)
    else:
        data = '{"status": 0, "message": "获取失败！请输入参数！", "data": []}'
    return HttpResponse(data)