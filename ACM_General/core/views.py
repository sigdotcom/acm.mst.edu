# Django
from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.
def handler404(request):
    """
    View rendered upon request of a non-existent url.

    :param request: A request directed to the function after attempting
                    to be resolved within the urls file.
    :type request: HttpRequest
    :rtype: HttpResponse
    :return: An HttpResponse containing the 404.html template, the
             current context of the response, and a 404 status code.
    """
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    """
    View rendered upon result of an internal error.

    :param request: A request directed to the function after attempting
                    to be resolved within the urls file.
    :type request: HttpRequest
    :rtype: HttpResponse
    :return: An HttpResponse containing the 500.html template, the
              current context of the resonse, and a 500 status code.
    """
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
