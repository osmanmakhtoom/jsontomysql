import json, time, datetime, string, random
import jdatetime
from . import toMysql


faToEn = str.maketrans({"۰":"0","۱":"1","۲":"2","۳":"3","۴":"4","۵":"5","۶":"6","۷":"7","۸":"8","۹":"9","،":","})
enToFa = str.maketrans({"0":"۰","1":"۱","2":"۲","3":"۳","4":"۴","5":"۵","6":"۶","7":"۷","8":"۸","9":"۹",",":"،"})

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

def shamsiToGregorian(shamsi_date, shamsi_time):
    shamsi_date = shamsi_date.translate(faToEn)
    shamsi_time = shamsi_time.translate(faToEn)
    shamsi_date_parts = shamsi_date.split('/')
    shamsi_time_parts = shamsi_time.split(':')
    fa_datetime = jdatetime.datetime(int(shamsi_date_parts[0]), int(shamsi_date_parts[1]), int(shamsi_date_parts[2]), int(shamsi_time_parts[0]), int(shamsi_time_parts[1]), int(shamsi_time_parts[2]), locale='fa_IR').togregorian()
    return fa_datetime

def slugify(title):
    word_list = []
    for word in title.split():
        if word not in word_list:
            word_list.append(word)
    slug = "-".join(word_list)
    return slug

def read_json(json_file, basename):

    categories_fields = {
        'title': ' ',
        'slug': ' ',
        'keywords': ' ',
        'description': ' ',
        'father_id': 0,
        'picture': ' ',
        'status': 0,
        'is_bold': 0,
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    products_fields = {
        'title': ' ',
        'slug': ' ',
        'body': ' ',
        'keywords': ' ',
        'description': ' ',
        'view_times': 0,
        'product_code': ' ',
        'category_id': 0,
        'father_id': 0,
        'status': 0,
        'product_type': 1,
        'picture': ' ',
        'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dgkala_url': ' ',
    }

    with open(json_file, encoding='utf-8') as json_file:

        content = json.load(json_file)
        for field in content:
            if 'tblcategory' == basename:
                categories_fields['id'] = field['id']
                categories_fields['title'] = field['title_category']
                categories_fields['slug'] = slugify(field['title_category'])
                categories_fields['picture'] = field['img']
                categories_fields['created_at'] = datetime.datetime.strptime(str(shamsiToGregorian('۱۴۰۰/۰۱/۲۲', '۱۲:۱۶:۵۵')),"%Y-%m-%d %H:%M:%S")

                result = toMysql.assign_data('categories', categories_fields)
                if not result:
                    print(f'Error {result} occurred while assigning categories to the database:\s\s', categories_fields)

            elif 'tblproducts' == basename:
                products_fields['title'] = field['product_title']
                products_fields['slug'] = slugify(rand_slug() + '-' + field['product_title'])
                products_fields['picture'] = field['product_img']
                products_fields['category_id'] = field['id_category']
                products_fields['description'] = field['meta']
                products_fields['keywords'] = field['keywords']
                products_fields['body'] = field['description']
                products_fields['product_code'] = field['product_code']
                products_fields['created_at'] = datetime.datetime.strptime(str(shamsiToGregorian(field['create_at'], field['times'])),"%Y-%m-%d %H:%M:%S")
                products_fields['status'] = field['confirm']

                result = toMysql.assign_data('products', products_fields)
                if not result:
                    print(f'Error {result} occurred while assigning categories to the database:\s\s', products_fields)

            elif 'tblartproducts' == basename:
                products_fields['title'] = field['product_title']
                products_fields['slug'] = slugify(rand_slug() + '-' + field['product_title'])
                products_fields['picture'] = field['product_img']
                products_fields['father_id'] = field['id_art']
                products_fields['description'] = field['meta']
                products_fields['keywords'] = field['keywords']
                products_fields['body'] = field['description']
                products_fields['product_code'] = field['product_code']
                products_fields['product_type'] = 2
                products_fields['created_at'] = datetime.datetime.strptime(str(shamsiToGregorian(field['create_at'], field['times'])),"%Y-%m-%d %H:%M:%S")
                products_fields['status'] = field['confirm']

                result = toMysql.assign_data('products', products_fields)
                if not result:
                    print(f'Error {result} occurred while assigning categories to the database:\s\s', products_fields)

            elif 'tbldgproducts' == basename:
                products_fields['title'] = field['title_dgp']
                products_fields['slug'] = slugify(rand_slug() + '-' + field['title_dgp'])
                products_fields['picture'] = field['img']
                products_fields['father_id'] = field['id_product']
                products_fields['dgkala_url'] = field['dg_link']
                products_fields['product_code'] = field['product_code']
                products_fields['product_type'] = 3
                products_fields['created_at'] = datetime.datetime.strptime(str(shamsiToGregorian(field['create_at'], field['times'])),"%Y-%m-%d %H:%M:%S")
                products_fields['status'] = field['confirm']

                result = toMysql.assign_data('products', products_fields)
                if not result:
                    print(f'Error {result} occurred while assigning categories to the database:\s\s', products_fields)

            else:
                pass

        return 'Data was assigned successfully!'



