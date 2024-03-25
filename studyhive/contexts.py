
def hq_thumbnail(input_string):
    try:
        return input_string.replace("default", "hqdefault")
    
    except:
        return input_string

def custom_context(request):
    return {'hq_thumbnail': hq_thumbnail}