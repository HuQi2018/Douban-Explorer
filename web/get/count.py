
import json
from django.http import HttpResponse
from utils.mongodb_model import CollectMovieDB,CollectMovieCommentsDB,CollectMovieReviewsDB,\
    CollectMusicDB,CollectMusicCommentsDB,CollectMusicReviewsDB\
    ,CollectBookDB,CollectBookCommentsDB,CollectBookReviewsDB


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

def main(request):
    movies = CollectMovieDB.objects.count()
    movies_comments = CollectMovieCommentsDB.objects.count()
    movies_reviews = CollectMovieReviewsDB.objects.count()
    music = CollectMusicDB.objects.count()
    music_comments = CollectMusicCommentsDB.objects.count()
    music_reviews = CollectMusicReviewsDB.objects.count()
    book = CollectBookDB.objects.count()
    book_comments = CollectBookCommentsDB.objects.count()
    book_reviews = CollectBookReviewsDB.objects.count()

    data = '{"movies":' + str(movies) + ',"movies_comments":' + str(movies_comments) + ',"movies_reviews":' + str(
        movies_reviews) + ',"music":' + str(music) + ',"music_comments":' + str(music_comments) + ',"music_reviews":' + str(
        music_reviews) + ',"book":' + str(book) + ',"book_comments":' + str(book_comments) + ',"book_reviews":' + str(
        book_reviews) + '}'
    return JsonResponse(json.loads(data))
    # data = '{"movies":79722,"movies_comments":125364,"movies_reviews":493297,"music":222,"music_comments":22048,"music_reviews":9801,"book":232,"book_comments":133971,"book_reviews":71003}'
    # return HttpResponse(data)