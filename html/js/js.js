
function search(){
    var txt = $('#get_search').val();
    var url = BASE_URL + "/searchPoint/?q="+txt;
    
    var html = '<ul id="search_result">';
    
    $.ajax({
        type: "GET",
        url: url,
        dataType: 'json',
        success: function (result) {//8次循环
			
            var x;
            var id = '';
            var name = '';
            var type = '';
            var star = '';
            var score = '';
            var author = '';
            var reviews_count = '';
            var brief = '';
            var img = '';
            var x = result.data.data;
            console.log(x.length);
            for (i=0;i<x.length;i++) {
                id = x[i]['id'];
                if(!id){
                    continue;
                }
                console.log(id);
                name =x[i]['name'];
                type = x[i]['type']=='movie'?'电影':x[i]['type']=='book'?'书籍':x[i]['type']=='music'?'音乐':'其它';
                star = x[i]['star'];
                score = x[i]['score'];
                author = x[i]['author'];
                reviews_count = x[i]['reviews_count'];
                brief = x[i]['brief'];
                img = x[i]['img'];
                
                html = html + '<li class="search_result_li"><img src="'+img+'"><h3><span>['+type+']</span>&nbsp;<a href="content.html?id='+id+'&type='+x[i]['type']+'" target="_blank" >'+name+'</a></h3><div class="rating-info"><span class="allstar'+star+' star"></span><span class="rating_nums">'+score+'</span><span>'+reviews_count+'</span><span class="subject-cast">'+author+'</span></div><p style="overflow: hidden;text-overflow: ellipsis;display: -webkit-box;-webkit-line-clamp: 2;-webkit-box-orient: vertical;">'+brief+'</p></li>';
            }
            html = html + '</ul>';
            $('#search_contain').html(html);
        }
    });
}