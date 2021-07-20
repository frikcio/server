def image_sizes(request):
    BIG_IMAGE_SIZE = 200
    MEDIUM_IMAGE_SIZE = 150
    SMALL_IMAGE_SIZE = 40
    return {'big_size':BIG_IMAGE_SIZE, 'medium_size': MEDIUM_IMAGE_SIZE, 'small_size': SMALL_IMAGE_SIZE}