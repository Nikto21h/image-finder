import requests
import argparse
import os

searchUrl = 'http://www.google.com/searchbyimage/upload'

# parse the given arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Search image on Google')
    parser.add_argument('-i', '--image', help='Image to search', required=True)
    parser.add_argument('-a', '--advanced', help='Advanced search', action='store_true')
    return parser.parse_args()

# save image as a temporary file
def save_image(url):
    if is_image_url(url):
        response = requests.get(url)
        file_name = url.split('/')[-1]
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return os.path.abspath(file_name)
    else:
        return EnvironmentError('Not a valid image url')

# get image from url
def search_image(Path, isurl = False):
    if isurl == True:
        Path = save_image(Path)
        multipart = {'encoded_image': (Path, open(Path, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        final_url = response.headers['Location']
        return final_url
    elif isurl == False:
        multipart = {'encoded_image': (Path, open(Path, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        final_url = response.headers['Location']
        return final_url
    else:
        return EnvironmentError('Failed to search image')

# main function
def main():
    args = parse_arguments()
    if args.advanced:
        print(search_image(args.image, True))
    else:
        print(search_image(args.image))


main()