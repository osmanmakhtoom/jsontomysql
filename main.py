# Python dependencies
import concurrent.futures, os

# Custom libraries
from lib import fromJson


json_files = [
    'tblproducts.json',
    'tblartproducts.json',
    'tbldgproducts.json',
]


def transfer(json_file):

    if not os.path.isfile(json_file):
        return False

    basename = os.path.basename(json_file).split('.')[0]
    result = fromJson.read_json(json_file, basename)

    return result


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

    proccess_transfer = {executor.submit(transfer, (os.path.join(os.getcwd(), 'json_files', json_file))): json_file for json_file in json_files}
    for future in concurrent.futures.as_completed(proccess_transfer):
        task = proccess_transfer[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (task, exc))
        else:
            print(data)