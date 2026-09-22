
def join_path(elems, filename):
    elems.append(filename)
    all_together = "/".join(elems)
    folders = all_together.split("/")
    final_directory = []
    for folder in folders:
        slug_folder = folder.strip().replace(" ", "_")
        if slug_folder not in final_directory:
            final_directory.append(slug_folder)
    return "/".join(final_directory)


def join_path_simple(elems, filename):
    elems.append(filename)
    all_together = "/".join(elems)
    folders = all_together.split("/")
    return "/".join(folders)


def stored_file_response(request, field_file):
    """Entrega un archivo guardado por redirección, no por proxy.

    Con S3 privado, `.url` ya es una URL firmada y efímera; en disco es
    la ruta /files/. `?redirect=false` la devuelve como JSON para el
    frontend autenticado, que no puede seguir un 302 con su token.
    """
    from django.http import HttpResponseRedirect
    from rest_framework.response import Response

    url = field_file.url
    if request.query_params.get('redirect') in ('false', '0'):
        return Response({'url': url})
    return HttpResponseRedirect(url)
