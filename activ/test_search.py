from django.shortcuts import render
# Create your views here.
import json
from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpResponse,JsonResponse
from haystack.forms import  ModelSearchForm
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from .models import Activity

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)



def basic_search(request, load_all=True):
    results_per_page = None
    extra_context = None
    form_class = ModelSearchForm
    query = ''
    results = EmptySearchQuerySet()
    if request.GET.get('q'):
        form = form_class(request.GET, load_all=load_all)
        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=None, load_all=load_all)

        print('进来了')
    res_model = SearchQuerySet().models(Activity).filter(content=form).load_all()
    print('-------++++++++++++----------')
    total_results = res_model.count()
    print(total_results)
    print(results)
    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)
    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        result = {"code": 404, "msg": 'No file found！', "data": []}
        return HttpResponse(json.dumps(result), content_type="application/json")

    context = {
        'form': form.as_ul(),
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }
    print('=====================')
    print(context)
    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)


    jsondata = []
    print(len(page.object_list))
    for result in page.object_list:
        data = {
            'pk': result.object.subject,
            'title': result.object.content,
            'content': result.object.id,

        }
        jsondata.append(data)
    print('=====================')
    print(jsondata)
    result = {"code": 200, "msg": 'Search successfully！', "data": jsondata}
    return JsonResponse(result, content_type="application/json")